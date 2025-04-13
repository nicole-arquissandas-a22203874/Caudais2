from django.shortcuts import render
from django.http import HttpResponse
from .models import Regiao, PontoMedida, Serie, Medicao
from .forms import RegiaoForm, PontoMedidaForm, ArquivoExcelForm
from.loader import carregar_excel
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Sum, Count, Avg
import pandas as pd
from .funcoes import normalize
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects


R_SCRIPT_PATH = 'C:\Users\nicol\Documents\a22203874-projeto-pw\caudais\r_scripts\reconstruction_script.R'





def upload_medicoes(request):
    if request.method == 'POST':
        regiao_form = RegiaoForm(request.POST)
        ponto_form = PontoMedidaForm(request.POST)
        arquivo_form = ArquivoExcelForm(request.POST, request.FILES)

        if regiao_form.is_valid() and ponto_form.is_valid() and arquivo_form.is_valid():

            regiao_nome = regiao_form.cleaned_data['regiao_nome']
            regiao_localidade = regiao_form.cleaned_data['regiao_localidade']
            tipo_medidor = ponto_form.cleaned_data['tipo_medidor']
            latitude = ponto_form.cleaned_data['latitude']
            longitude = ponto_form.cleaned_data['longitude']
            arquivo_excel = arquivo_form.cleaned_data['arquivo_excel']

            regiao, _ = Regiao.objects.get_or_create(nome=regiao_nome, localidade=regiao_localidade)


            ponto_medida, _ = PontoMedida.objects.get_or_create(
                regiao=regiao,
                tipoMedidor=tipo_medidor,
                defaults={'latitude': latitude, 'longitude': longitude}
            )

            serie = Serie.objects.create(ponto_medida=ponto_medida)

            # Carregar o arquivo Excel e criar Medicoes associadas

            mensagem=carregar_excel(arquivo_excel,serie)

            return HttpResponse(mensagem)
    else:
        regiao_form = RegiaoForm()
        ponto_form = PontoMedidaForm()
        arquivo_form = ArquivoExcelForm()

    return render(request, 'caudais/upload_medicoes.html', {
        'regiao_form': regiao_form,
        'ponto_form': ponto_form,
        'arquivo_form': arquivo_form
    })


def dashboard(request):
    # Get query parameters
    selected_year = request.GET.get('year')
    selected_ponto_medicao_id = request.GET.get('ponto_medicao')
    data_type = request.GET.get('data_type', 'raw')  # default to raw if not provided

    # Fetch all PontoMedida for the dropdown
    pontos_medicao = PontoMedida.objects.all()

    # Convert the selected_ponto_medicao_id to integer if it is present
    if selected_ponto_medicao_id:
        selected_ponto_medicao = PontoMedida.objects.get(id=selected_ponto_medicao_id)
    else:
        selected_ponto_medicao = None


    # Initialize empty variables for charts
    years, counts, totals, avg_values = [], [], [], []
    month_labels, month_counts, month_totals, month_avg = [], [], [], []

    # Branch for data_type == 'raw'
    if data_type == 'raw':
        # Query yearly data from raw Medicao records
        yearly_data = Medicao.objects.filter(serie__ponto_medida=selected_ponto_medicao).annotate(
            year=ExtractYear('timestamp')
        ).values('year').annotate(
            total_valor=Sum('valor'), count=Count('id'), avg_valor=Avg('valor')
        ).order_by('year')

        years = [entry['year'] for entry in yearly_data]
        counts = [entry['count'] for entry in yearly_data]
        totals = [entry['total_valor'] for entry in yearly_data]
        avg_values = [round(entry['avg_valor'], 2) for entry in yearly_data]

         # Set default year if none is provided
        if selected_year:
            try:
                selected_year = int(selected_year)
            except ValueError:
                selected_year = None
        else:
            selected_year = years[-1] if years else None

        # Query monthly raw data for the selected year
        if selected_year:
            monthly_data = Medicao.objects.filter(
                serie__ponto_medida=selected_ponto_medicao, timestamp__year=selected_year
            ).annotate(
                month=ExtractMonth('timestamp')
            ).values('month').annotate(
                total_valor=Sum('valor'), count=Count('id'), avg_valor=Avg('valor')
            ).order_by('month')

            monthly_lookup = {entry['month']: entry for entry in monthly_data}
            for m in range(1, 13):
                month_labels.append(m)
                if m in monthly_lookup:
                    entry = monthly_lookup[m]
                    month_counts.append(entry['count'])
                    month_totals.append(entry['total_valor'])
                    month_avg.append(round(entry['avg_valor'], 2))
                else:
                    month_counts.append(0)
                    month_totals.append(0)
                    month_avg.append(0)

    # Branch for data_type == 'normalized'
    if data_type == 'normalized':
        # Query the raw Medicao data for the selected PontoMedicao and year
        dadosRaw = Medicao.objects.filter(serie__ponto_medida=selected_ponto_medicao)
        df = pd.DataFrame(list(dadosRaw.values('timestamp', 'valor')))

        if not df.empty:
            # Convert to DataFrame and normalize
            df['timestamp'] = pd.to_datetime(df['timestamp'])#transforma o timestamp em datetime do pandas
            df.set_index('timestamp', inplace=True)
            #tranforma a serie cuma serie continuam de intrevalos fixos 15 minutos,se nao existir valor em alguns dos intrevalos e colocado NaN
            resampled_df = df.resample('15T').asfreq()
            normalize(df,resampled_df, 15)  # aplicacao de funcao de normalizacao dos leandro

            ## Query yearly data dos dados normalizados
            yearly_normalized = resampled_df.groupby(resampled_df.index.year).agg(
            total_valor=('valor', 'sum'),
            count=('valor', 'count'),
            avg_valor=('valor', 'mean'))

            years = yearly_normalized.index.tolist()
            totals = yearly_normalized['total_valor'].tolist()
            counts = yearly_normalized['count'].tolist()
            avg_values = [round(x, 2) for x in yearly_normalized['avg_valor'].tolist()]
            if selected_year:
                try:
                    selected_year = int(selected_year)
                except ValueError:
                    selected_year = None
            else:
                selected_year = years[-1] if years else None


            if selected_year:
                # Recalculate monthly statistics from normalized data
                resampled_df_selected_year = resampled_df[resampled_df.index.year == selected_year]
                monthly_normalized = resampled_df_selected_year.groupby(resampled_df_selected_year.index.month).agg(
                    count=('valor', 'count'),
                    total_valor=('valor', 'sum'),
                    avg_valor=('valor', 'mean')
                ).reindex(range(1, 13), fill_value=0)

                # Assign monthly values for charts
                month_counts = monthly_normalized['count'].tolist()
                month_totals = monthly_normalized['total_valor'].tolist()
                month_avg = [round(x, 2) for x in monthly_normalized['avg_valor'].tolist()]

                month_labels = [i for i in range(1, 13)]

    # Branch for data_type == 'reconstruido' (use the Tbats function)
    if data_type == 'reconstruido':
        # Load your R script
        robjects.r.source(R_SCRIPT_PATH)
        # Reference your Tbats function from the R script
        tbats_function = robjects.globalenv['TBATS.reconstruct']
        # Query the raw Medicao data for the selected PontoMedicao and year
        dados_raw = Medicao.objects.filter(serie__ponto_medida=selected_ponto_medicao)
        df = pd.DataFrame(list(dados_raw.values('timestamp', 'valor')))

        if not df.empty:
            # Convert the data to a pandas DataFrame
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)

            # Resample the data to 15-minute intervals (fill NaN for missing intervals)
            resampled_df = df.resample('15T').asfreq()
            start_date = pd.Timestamp(f"{df.index.min().year}-{df.index.min().month}-01")  # Start from January 1st of the first year
            end_date = pd.Timestamp(f"{df.index.max().year}-{df.index.max().month}-30 23:45:00")  # End at the last day of the final year

# Step 2: Create a new date range with 15-minute intervals for the entire period
            full_range = pd.date_range(start=start_date, end=end_date, freq='15T')

# Step 3: Resample and apply frequency (asfreq will generate NaNs for missing intervals)
            resampled_df = df.resample('15T').asfreq()


# Step 5: Reindex the DataFrame to include the full date range, filling missing periods with NaN
            resampled_df = resampled_df.reindex(full_range)
            resampled_df.index.name = 'Date'
            #original,resampled
            normalize(df,resampled_df, 15)
            
            matrix_df = resampled_df.pivot(index='Date', columns='Time', values='valor')
            # Reset the index to make 'Date' the first column
            matrix_df.reset_index()

            # Rename the index column to 'Date' and remove any other labels for clarity
            matrix_df.columns.name = None  # This removes the 'Time' label from the columns
            matrix_pronta =matrix_df.reset_index()
            #passa a variavel do python matrixpront para o R environment
            pandas2ri.activate()
            robjects.globalenv['matrix_pronta'] = pandas2ri.py2rpy(matrix_pronta)
             
             # Call the JQ function from R to reconstruct the missing values
            JQ_function= robjects.globalenv['JQ.function']
            recontructedValues=JQ_function()
            reconstructed_values_list = recontructedValues.tolist()
            resampled_df['valor']=reconstructed_values_list
            

            # Recalculate yearly statistics
            yearly_reconstructed = resampled_df.groupby(resampled_df.index.year).agg(
                total_valor=('valor', 'sum'),
                count=('valor', 'count'),
                avg_valor=('valor', 'mean')
            )

            years = yearly_reconstructed.index.tolist()
            totals = yearly_reconstructed['total_valor'].tolist()
            counts = yearly_reconstructed['count'].tolist()
            avg_values = [round(x, 2) for x in yearly_reconstructed['avg_valor'].tolist()]
            if selected_year:
                try:
                    selected_year = int(selected_year)
                except ValueError:
                    selected_year = None
            else:
                selected_year = years[-1] if years else None

            # Recalculate monthly statistics for the selected year
            if selected_year:
                resampled_df_selected_year = resampled_df[resampled_df.index.year == selected_year]
                monthly_reconstructed = resampled_df_selected_year.groupby(resampled_df_selected_year.index.month).agg(
                    count=('valor', 'count'),
                    total_valor=('valor', 'sum'),
                    avg_valor=('valor', 'mean')
                ).reindex(range(1, 13), fill_value=0)

                # Assign monthly values for charts
                month_counts = monthly_reconstructed['count'].tolist()
                month_totals = monthly_reconstructed['total_valor'].tolist()
                month_avg = [round(x, 2) for x in monthly_reconstructed['avg_valor'].tolist()]

                month_labels = [i for i in range(1, 13)]

    # Fallback logic if no valid data_type provided
    else:
        # Handle unexpected data_type
        pass
    month_names=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
    # Prepare context for charts
    context = {
        'pontos_medicao': pontos_medicao,
        'selected_ponto_medicao': selected_ponto_medicao,
        'years': years,
        'counts': counts,
        'totals': totals,
        'avg_values': avg_values,
        'selected_year': selected_year,
        'month_labels': month_labels,
        'month_counts': month_counts,
        'month_totals': month_totals,
        'month_avg': month_avg,
        'data_type': data_type,  # So template can reflect the selected option
        'month_names': month_names,
    }

    return render(request, 'caudais/dashboard.html', context)

