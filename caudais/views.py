from django.shortcuts import render
from django.http import HttpResponse
from .models import Regiao, PontoMedida, Serie, Medicao, MedicaoProcessada,EstatisticaMensal,EstatisticaAnual
from .forms import RegiaoForm, PontoMedidaForm, ArquivoExcelForm
from.funcoes import carregar_excel,guardaProcessados,guardaEstatisticaAnual,guardaEstatisticaMensal
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Sum, Count, Avg
import pandas as pd
import calendar
import math
from .funcoes import normalize
from rpy2.robjects import pandas2ri
import rpy2.robjects as robjects
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import default_converter
from rpy2.robjects import conversion
conversion.set_conversion(default_converter + pandas2ri.converter)
R_SCRIPT_PATH = 'C:\\Users\\nicol\\Documents\\a22203874-projeto-pw\\caudais\\r_scripts\\reconstruction_script.R'

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
    conversion.set_conversion(default_converter + pandas2ri.converter)
    # Get query parameters
    selected_year = request.GET.get('year')
    selected_ponto_medicao_id = request.GET.get('ponto_medicao')
    data_type = request.GET.get('data_type', 'raw')  # default para raw 
    recon_method = request.GET.get('recon_method', 'jq') 

    # buscar todos PontoMedida para dropdown
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
        # Tenta carregar estatísticas do banco
        estatisticas_anuais = EstatisticaAnual.objects.filter(
        ponto_medida=selected_ponto_medicao,
        metodo=data_type
        )

        if estatisticas_anuais.exists():
            for e in estatisticas_anuais:
                years.append(e.ano)
                totals.append(e.total)
                counts.append(e.contagem)
                avg_values.append(e.media)
        else:       
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
            guardaEstatisticaAnual(zip(years, totals, counts, avg_values),data_type,selected_ponto_medicao)
        # Set default year if none is provided
        if selected_year:
            try:
                selected_year = int(selected_year)
            except ValueError:
                selected_year = None
        else:
            selected_year = years[-1] if years else None
        # Tenta carregar estatísticas do banco
        estatisticas_mensais= EstatisticaMensal.objects.filter(
        ponto_medida=selected_ponto_medicao,
        ano=selected_year,
        metodo=data_type

        )
        if estatisticas_mensais.exists():
            for e in estatisticas_mensais:
                month_labels.append(e.mes)
                month_totals.append(e.total)
                month_counts.append(e.contagem)
                month_avg.append(e.media)       

        else:
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
                guardaEstatisticaMensal(zip(month_labels, month_totals, month_counts, month_avg),data_type,selected_ponto_medicao,selected_year)
                

    # Branch for data_type == 'normalized'
    if data_type == 'normalized':
        # Query the raw Medicao data for the selected PontoMedicao and year
        dadosRaw = Medicao.objects.filter(serie__ponto_medida=selected_ponto_medicao)
        df = pd.DataFrame(list(dadosRaw.values('timestamp', 'valor')))
        dados_guardados = MedicaoProcessada.objects.filter(
        ponto_medida=selected_ponto_medicao,
        metodo=recon_method if data_type == 'reconstruido' else 'normalized'
         ).order_by('timestamp')

        if dados_guardados.exists():
            df = pd.DataFrame(list(dados_guardados.values('timestamp', 'valor')))
            df.set_index('timestamp', inplace=True)
            resampled_df = df 
        else:
            if not df.empty:
                # Convert to DataFrame and normalize
                df['timestamp'] = pd.to_datetime(df['timestamp'])#transforma o timestamp em datetime do pandas
                df.set_index('timestamp', inplace=True)
                df.index = df.index.tz_localize(None)
                #tranforma a serie cuma serie continuam de intrevalos fixos 15 minutos,se nao existir valor em alguns dos intrevalos e colocado NaN
                resampled_df = df.resample('15T').asfreq()
                year_end = df.index.max().year
                month_end = df.index.max().month
                last_day = calendar.monthrange(year_end, month_end)[1] # Use calendar.monthrange to get the last day of the month

                start_date = pd.Timestamp(f"{df.index.min().year}-{df.index.min().month}-01")  # Start from January 1st of the first year
                end_date = pd.Timestamp(f"{year_end}-{month_end}-{last_day} 23:45:00") # End at the last day of the final year
                # Create a new date range with 15-minute intervals for the entire period
                full_range = pd.date_range(start=start_date, end=end_date, freq='15T')
                #Resample and apply frequency (asfreq will generate NaNs for missing intervals)
                resampled_df = df.resample('15T').asfreq()
                #Reindex the DataFrame to include the full date range, filling missing periods with NaN
                resampled_df = resampled_df.reindex(full_range)
                normalize(df,resampled_df, 15)  # aplicacao de funcao de normalizacao dos leandro
                guardaProcessados(resampled_df['valor'].items(),'normalized',selected_ponto_medicao)
            ## Query yearly data dos dados normalizados

        # Tenta carregar estatísticas do banco
        estatisticas_anuais = EstatisticaAnual.objects.filter(
        ponto_medida=selected_ponto_medicao,
        metodo=data_type
        )

        if estatisticas_anuais.exists():
            for e in estatisticas_anuais:
                years.append(e.ano)
                totals.append(e.total)
                counts.append(e.contagem)
                avg_values.append(e.media)
        else:

            yearly_normalized = resampled_df.groupby(resampled_df.index.year).agg(
            total_valor=('valor', 'sum'),
            count=('valor', 'count'),
            avg_valor=('valor', 'mean'))

            years = yearly_normalized.index.tolist()
            totals = yearly_normalized['total_valor'].tolist()
            counts = yearly_normalized['count'].tolist()
            avg_values = [round(x, 2) for x in yearly_normalized['avg_valor'].tolist()]
            guardaEstatisticaAnual(zip(years, totals, counts, avg_values),data_type,selected_ponto_medicao)

        if selected_year:
            try:
                selected_year = int(selected_year)
            except ValueError:
                selected_year = None
        else:
            selected_year = years[-1] if years else None

        # Tenta carregar estatísticas do banco
        estatisticas_mensais= EstatisticaMensal.objects.filter(
        ponto_medida=selected_ponto_medicao,
        ano=selected_year,
        metodo=data_type

        )
        if estatisticas_mensais.exists():
            for e in estatisticas_mensais:
                month_labels.append(e.mes)
                month_totals.append(e.total)
                month_counts.append(e.contagem)
                month_avg.append(e.media)
        else:
            if selected_year:
                # Recalculate monthly statistics from normalized data
                resampled_df_selected_year = resampled_df[resampled_df.index.year == selected_year]
                monthly_normalized = resampled_df_selected_year.groupby(resampled_df_selected_year.index.month).agg(
                    count=('valor', 'count'),
                    total_valor=('valor', 'sum'),
                    avg_valor=('valor', 'mean')
                ).reindex(range(1, 13), fill_value=0)

                # Assign monthly values for charts
                # Assign monthly values for charts
                month_counts = [int(x) if pd.notnull(x) and not math.isnan(x) else 0
                               for x in monthly_normalized['count'].tolist()
                               ]

                month_totals = [float(x) if pd.notnull(x) and not math.isnan(x) else 0.0
                                for x in monthly_normalized['total_valor'].tolist()
                                ]

                month_avg = [round(x, 2) if pd.notnull(x) and not math.isnan(x) else 0.0
                             for x in monthly_normalized['avg_valor'].tolist()
                            ]

                month_labels = [i for i in range(1, 13)]
                guardaEstatisticaMensal(zip(month_labels, month_totals, month_counts, month_avg),data_type,selected_ponto_medicao,selected_year)

    # Branch for data_type == 'reconstruido' (use the Tbats function)
    if data_type == 'reconstruido':
        # Load your R script
        with localconverter(default_converter + pandas2ri.converter):
            robjects.r.source(R_SCRIPT_PATH)
        
        # Query the raw Medicao data for the selected PontoMedicao and year
        dados_raw = Medicao.objects.filter(serie__ponto_medida=selected_ponto_medicao)
        df = pd.DataFrame(list(dados_raw.values('timestamp', 'valor')))
        dados_guardados = MedicaoProcessada.objects.filter(
        ponto_medida=selected_ponto_medicao,
        metodo=recon_method if data_type == 'reconstruido' else 'normalized'
         ).order_by('timestamp')

        if dados_guardados.exists():
            df = pd.DataFrame(list(dados_guardados.values('timestamp', 'valor')))
            df.set_index('timestamp', inplace=True)
            resampled_df = df
                
        else:
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.set_index('timestamp', inplace=True)
                df.index = df.index.tz_localize(None)
               # Resample the data to 15-minute intervals (fill NaN for missing intervals)
                resampled_df = df.resample('15T').asfreq()
                year_end = df.index.max().year
                month_end = df.index.max().month
                last_day = calendar.monthrange(year_end, month_end)[1] # Use calendar.monthrange to get the last day of the month

                start_date = pd.Timestamp(f"{df.index.min().year}-{df.index.min().month}-01")  # Start from January 1st of the first year
                end_date = pd.Timestamp(f"{year_end}-{month_end}-{last_day} 23:45:00") # End at the last day of the final year
                #Create a new date range with 15-minute intervals for the entire period
                full_range = pd.date_range(start=start_date, end=end_date, freq='15T')
                #Resample and apply frequency (asfreq will generate NaNs for missing intervals)
                resampled_df = df.resample('15T').asfreq()
                #Reindex the DataFrame to include the full date range, filling missing periods with NaN
                resampled_df = resampled_df.reindex(full_range)
                resampled_df.index.name = 'Date'#Isto porque a matrix tem que ter uma coluna Date por causa do dma
                #original,resampled
                normalize(df,resampled_df, 15)
                # Since 'Data' is now the index, we use the index to create 'Date' and 'Time' columns
                resampled_df['Date'] = resampled_df.index.strftime('%Y/%m/%d')  # Extract date as YYYY/MM/DD
                resampled_df['Time'] = resampled_df.index.strftime('%H:%M')     # Extract time as HH:MM
            
                matrix_df = resampled_df.pivot(index='Date', columns='Time', values='valor')
                # Reset the index to make 'Date' the first column
                matrix_df.reset_index()
            
                matrix_df.columns.name = None  # This removes the 'Time' label from the columns
                matrix_pronta =matrix_df.reset_index()
                #passa a variavel do python matrixpront para o R environment
                with localconverter(default_converter + pandas2ri.converter):
                    robjects.globalenv['matrix_pronta'] = pandas2ri.py2rpy(matrix_pronta)

                reconstructed_values_list=[]
                if recon_method == 'jq':
                    JQ_function = robjects.globalenv['JQ.function']
                    reconstructedValues = JQ_function()
                    reconstructed_values_list = reconstructedValues.tolist()

                else:
                # Call the TBATS function from R to reconstruct the missing values
                    TBATS_function = robjects.globalenv['TBATS.function']
                    reconstructedValues = TBATS_function()
                    reconstructed_values_list = reconstructedValues.tolist()
             
            
                resampled_df['valor']=reconstructed_values_list
                guardaProcessados(resampled_df['valor'].items(),recon_method,selected_ponto_medicao)
        
         # Tenta carregar estatísticas do banco
        estatisticas_anuais = EstatisticaAnual.objects.filter(
        ponto_medida=selected_ponto_medicao,
        metodo=recon_method
        )

        if estatisticas_anuais.exists():
            for e in estatisticas_anuais:
                years.append(e.ano)
                totals.append(e.total)
                counts.append(e.contagem)
                avg_values.append(e.media)
        else:       
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

        # Tenta carregar estatísticas do banco
        estatisticas_mensais= EstatisticaMensal.objects.filter(
        ponto_medida=selected_ponto_medicao,
        ano=selected_year,
        metodo=recon_method

        )
        if estatisticas_mensais.exists():
            for e in estatisticas_mensais:
                month_labels.append(e.mes)
                month_totals.append(e.total)
                month_counts.append(e.contagem)
                month_avg.append(e.media)
        else:
            # Recalculate monthly statistics for the selected year
            if selected_year:
                resampled_df_selected_year = resampled_df[resampled_df.index.year == selected_year]
                monthly_reconstructed = resampled_df_selected_year.groupby(resampled_df_selected_year.index.month).agg(
                    count=('valor', 'count'),
                    total_valor=('valor', 'sum'),
                    avg_valor=('valor', 'mean')
                    ).reindex(range(1, 13), fill_value=0)

                # Assign monthly values for charts
                month_counts = [int(x) if pd.notnull(x) and not math.isnan(x) else 0
                               for x in monthly_reconstructed['count'].tolist()
                               ]

                month_totals = [float(x) if pd.notnull(x) and not math.isnan(x) else 0.0
                                for x in monthly_reconstructed['total_valor'].tolist()
                                ]

                month_avg = [round(x, 2) if pd.notnull(x) and not math.isnan(x) else 0.0
                             for x in monthly_reconstructed['avg_valor'].tolist()
                            ]
                month_labels = [i for i in range(1, 13)]
                guardaEstatisticaMensal(zip(month_labels, month_totals, month_counts, month_avg),recon_method,selected_ponto_medicao,selected_year)

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
        'recon_method': recon_method,
    }

    return render(request, 'caudais/dashboard.html', context)

def exportar_excel(request):
    ponto_id = request.GET.get('ponto_medicao')
    data_type = request.GET.get('data_type', 'raw')
    metodo = request.GET.get('recon_method', 'jq')

    if not ponto_id:
        return HttpResponse("Ponto de medição não especificado.", status=400)

    try:
        ponto = PontoMedida.objects.get(id=ponto_id)
    except PontoMedida.DoesNotExist:
        return HttpResponse("Ponto de medição inválido.", status=404)

    if data_type == 'raw':
        queryset = Medicao.objects.filter(serie__ponto_medida=ponto).values('timestamp', 'valor')
    elif data_type == 'normalized':
        queryset = MedicaoProcessada.objects.filter(ponto_medida=ponto, metodo='normalized').values('timestamp', 'valor')
    elif data_type == 'reconstruido':
        queryset = MedicaoProcessada.objects.filter(ponto_medida=ponto, metodo=metodo).values('timestamp', 'valor')
    else:
        return HttpResponse("Tipo de dado inválido.", status=400)

    df = pd.DataFrame(list(queryset))
    if df.empty:
        return HttpResponse("Sem dados para exportar.", status=204)

    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)

    df = df.sort_values(by='timestamp')
    df.rename(columns={'timestamp': 'Data', 'valor': 'Caudal'}, inplace=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    if data_type=="normalized":
        nome_arquivo = f"medicoes_{data_type}_{ponto.id}.xlsx"
    if data_type=="raw":
        nome_arquivo = f"medicoes_{data_type}_{ponto.id}.xlsx"
    if data_type=='reconstruido':
        nome_arquivo = f"medicoes_{data_type}_{metodo}_{ponto.id}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'


    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Medições')

    return response
