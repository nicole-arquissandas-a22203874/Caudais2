import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import calendar


"""# Análise Exploratória

## Tratamento de dados
"""

def is_leap_year(year):
    return calendar.isleap(year)

def num_rows(df):
  return len(df)

def num_columns(df):
  return len(df.columns)

def date_and_time(df):
  df['Data'] = pd.to_datetime(df['Data'])

  df['Date'] = df['Data'].dt.date
  df['Time'] = df['Data'].dt.time

def duplicates(df):
  return df['Data'].duplicated()

def mean_time_difference(df):
  return (time_diff(df)).mean()

def time_diff(df):
  time_diff = df['Data'].diff()
  return time_diff[time_diff > pd.Timedelta(0)]

def mean_time_difference_per_year(df):
  df_copy = df.copy()
  df_copy['TimeDiff'] = df_copy['Data'].diff()
  df_copy['TimeDiff'] = df_copy['TimeDiff'][df_copy['TimeDiff'] > pd.Timedelta(0)]

  df_copy['Year'] = df_copy['Data'].dt.year

  return df_copy.groupby('Year')['TimeDiff'].mean()

def mean_time_difference_per_month(df):
  df_copy = df.copy()

  df_copy['TimeDiff'] = df['Data'].diff()

  df_copy['TimeDiff'] = df_copy['TimeDiff'][df_copy['TimeDiff'] > pd.Timedelta(0)]

  df_copy['Year'] = df_copy['Data'].dt.year
  df_copy['Month'] = df_copy['Data'].dt.month

  return df_copy.groupby(['Year', 'Month'])['TimeDiff'].mean()

def format(df):
  formato = ['Date', 'Time', 'Caudal']
  return df[formato]

def has_seconds(df):
  df['Time'] = df['Time'].apply(lambda x: x.strftime('%H:%M:%S'))
  return any(':00' not in str_time for str_time in df['Time'])

def num_unique_dates(df):
  return df['Date'].nunique()

def date_datetime(df):
  df['Date'] = pd.to_datetime(df['Date'])

def unique_years(df):
  return df['Date'].dt.year.unique()

def is_ordered_ascending(df):
  return df['Date'].is_monotonic_increasing

def date_date_format(df):
  df['Date'] = df['Date'].dt.date

def sort_date(df):
  return df.sort_values(by='Date')

def year_month_day(df):
  df['Year'] = df['Date'].dt.year
  df['Month'] = df['Date'].dt.month
  df['Day'] = df['Date'].dt.day

  return df

def average_measurements_per_day(df):
  return df.groupby('Date').size().mean()

def average_measurements_per_year(df):
  return df.groupby(['Year', 'Date']).size().groupby('Year').mean()

def average_measurements_per_year_month(df):
   return df.groupby(['Year', 'Month', 'Date']).size().groupby(['Year', 'Month']).mean()

def measurements_per_year_month_boxplot(df):
  daily_measurements_count = df.groupby(['Year', 'Month', 'Date']).size()

  plot_data = daily_measurements_count.reset_index(name='Measurements')

  for year in unique_years(df):
      year_data = plot_data[plot_data['Year'] == year]

      plt.figure(figsize=(8, 6))
      sns.boxplot(x='Month', y='Measurements', data=year_data, whis=3, palette="Paired")
      plt.title(f'Número de medições diárias em {year}')
      plt.xlabel('Month')
      plt.ylabel('Número de medições')
      plt.show()

def unique_month_counts(df):
  return df.drop_duplicates(subset=['Year', 'Month']).groupby('Year').size().reset_index(name='Número de meses')

def unique_days_counts(df):
  return df.drop_duplicates(subset=['Year', 'Month','Day']).groupby('Year').size().reset_index(name='Número de dias')

def expected_days_print(df):
  for year, num_days in zip((unique_days_counts(df))['Year'], (unique_days_counts(df))['Número de dias']):

    expected_days = 366 if pd.Timestamp(f'{year}-12-31').is_leap_year else 365
    expected_days -= (12 - len(df[df['Year'] == year]['Month'].unique())) * 30

    print(f"Existem medições de {num_days} dias distintos em {year}. Esperava-se que existissem {expected_days}.")

def caudal_values_chart(df):
    plt.figure(figsize=(10, 6))

    for year in unique_years(df):
        year_data = df[df['Year'] == year]
        plt.plot(year_data['Date'], year_data['Caudal'], label=str(year))

    plt.xlabel('Data')
    plt.ylabel('Caudal')
    plt.title('Valores de Caudal')
    plt.legend(title='Ano')
    plt.show()

def caudal_values_chart_yearly(df):
  for year in unique_years(df):
    year_data = df[df['Year'] == year]

    plt.figure(figsize=(10, 6))
    plt.plot(year_data['Date'], year_data['Caudal'])
    plt.xlabel('Data')
    plt.ylabel('Caudal')
    plt.title(f'Valores de Caudal em {year}')
    plt.show()

def time_datetime(df):
  df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

def invalid_time_values(df):
  return df[df['Time'].isna()]

def time_time(df):
  df['Time'] = df['Time'].dt.time

def correct_caudal(df):
  df['Caudal'] = pd.to_numeric(df['Caudal'], errors='coerce')

def fails(df):
  return df[df['Caudal'].isna()]

def total_fails(df):
  return len(fails(df))

def non_integer_counts(df):
  non_integer_mask = df['Caudal'].isna()
  return df[non_integer_mask].groupby('Year').size().reset_index(name='Número de Falhas')

def days_with_no_data(df):
  return df.groupby('Date').filter(lambda x: x['Caudal'].notna().any()).groupby('Date').filter(lambda x: x['Caudal'].isna().all())['Date'].unique()

def entrys_per_year(df):
  return df.groupby('Year')['Caudal'].count().reset_index(name='Número Total de medições')

def entries_without_errors_per_year(entrys_per_year_df, non_integer_counts_df):
  entries_without_fails_per_year = entrys_per_year_df.copy()
  entries_without_fails_per_year['Medições sem Falhas'] = entrys_per_year_df['Número Total de medições'] - non_integer_counts_df['Número de Falhas']
  return entries_without_fails_per_year

def entries_without_errors_per_year_percent(df):
  df['Medições sem falhas (%)'] = ((df['Medições sem Falhas'] / df['Número Total de medições']) * 100)

  entries_without_errors_per_year_percent = df.copy()
  entries_without_errors_per_year_percent.drop('Medições sem Falhas', axis=1, inplace=True)

  return entries_without_errors_per_year_percent

def entries_with_errors_per_year_percent(df):
  entries_with_errors_per_year_percent = df.copy()

  entries_with_errors_per_year_percent['Medições com falhas (%)'] = (
    (100 - df['Medições sem falhas (%)'])
  )

  entries_with_errors_per_year_percent.drop('Medições sem falhas (%)', axis=1, inplace=True)

  return entries_with_errors_per_year_percent

def unique_years_no_error(df):
  return (df_no_errors(df))['Year'].unique()

def df_no_errors(df):
  return df[~df['Caudal'].isna()]

def mean_results(df, no_errors_df):
  return no_errors_df.groupby(['Year', 'Month'], as_index=False).agg(
    Average=('Caudal', 'mean'),
  ).reset_index()

def mean_results_yearly(df, no_errors_df):
  return no_errors_df.groupby('Year', as_index=False).agg(
    Average=('Caudal', 'mean'),
  ).reset_index()

def means_caudal_yearly(df):

  no_errors_df = df_no_errors(df)

  result = mean_results(df, no_errors_df)

  result_yearly = mean_results_yearly(df, no_errors_df)

  for year in unique_years_no_error(df):
    year_data = result[result['Year'] == year]

    plt.figure(figsize=(10, 6))
    plt.plot(year_data['Month'] , year_data['Average'], label='Média', marker='o', linestyle='-')

    plt.axhline(result_yearly.loc[result_yearly['Year'] == year, 'Average'].values[0], linestyle='dashed', color='blue',
                label= f'Média anual : {result_yearly.loc[result_yearly["Year"] == year, "Average"].values[0]:.2f}')

    for i, avg in enumerate(year_data['Average']):
      plt.text(year_data['Month'].iloc[i] , avg, f'{avg:.2f}', ha='center', va='bottom', color='blue')

    plt.xlabel('Mês')
    plt.ylabel('Caudal')
    plt.title(f'Média das medições de Caudal do ano {year}')
    plt.xticks(range(1, 13), [str(month) for month in range(1, 13)])
    plt.legend()
    plt.show()

def means_caudal(df):

  no_errors_df = df_no_errors(df)

  result = mean_results(df, no_errors_df)

  result_yearly = mean_results_yearly(df, no_errors_df)

  plt.figure(figsize=(10, 6))
  for year in unique_years_no_error(df):
    year_data = result[result['Year'] == year]
    plt.plot(year_data['Month'], year_data['Average'], label=f'Ano {year}')

  overall_monthly_average = result.groupby('Month')['Average'].mean()

  plt.plot(overall_monthly_average.index, overall_monthly_average.values, label='Média Geral', linestyle='--', color='black')

  plt.xlabel('Mês')
  plt.ylabel('Caudal')
  plt.title('Médias de medições de Caudal')
  plt.xticks(range(1, 13), [str(month) for month in range(1, 13)])
  plt.legend()
  plt.show()

def std_monthly(df):
  return df.groupby(['Year', 'Month'], as_index=False).agg(
    Desvio_Padrao=('Caudal', 'std')
).reset_index()

def std_yearly(df):
  return df.groupby('Year', as_index=False).agg(
    Desvio_Padrao=('Caudal', 'std')
).reset_index()

def caudal_boxplots(df):
  for year in unique_years_no_error(df):
    plt.figure(figsize=(12, 8))
    year_data = df[df['Year'] == year]

    ax = sns.boxplot(x='Month', y='Caudal', data=year_data, whis=3, palette="Set3")

    plt.title(f'Boxplot das medições de Caudal em {year}')
    plt.xlabel('Mês')
    plt.ylabel('Medição do Caudal')
    plt.show()

def caudal_statistics(df_no_errors):
  dfs = []

  for year in df_no_errors['Year'].unique():
    for month in df_no_errors['Month'].unique():
        subset_data = df_no_errors[(df_no_errors['Year'] == year) & (df_no_errors['Month'] == month)]

        if not subset_data.empty:
            min_value = subset_data['Caudal'].min()
            q1_value = np.percentile(subset_data['Caudal'], 25)
            median_value = np.median(subset_data['Caudal'])
            q3_value = np.percentile(subset_data['Caudal'], 75)
            max_value = subset_data['Caudal'].max()

            dfs.append(pd.DataFrame({
                'Year': [year],
                'Month': [month],
                'Min_Value': [min_value],
                'Q1_Value': [q1_value],
                'Median': [median_value],
                'Q3_Value': [q3_value],
                'Max_Value': [max_value]
            }))

  summary_df = pd.concat(dfs, ignore_index=True)

  summary_df_sorted = summary_df.sort_values(by=['Year', 'Month'])
  return summary_df_sorted

def resultados(df):

  print(f"Existem {num_rows(df)} medições de Caudal. \n")

  print(f"A DataFrame tem {num_columns(df)} colunas \n")

  date_and_time(df)

  if (duplicates(df)).any():
    print("Linhas duplicadas:")
    print(df[duplicates])
    df = df.drop_duplicates(subset=['Data'])
  else:
    print("Não existem duplicados.\n")

  print("Média de tempo entre medições:", mean_time_difference(df), "\n")

  print("Média de tempo entre medições por ano:")
  print(mean_time_difference_per_year(df))

  print("\nMédia de tempo entre medições por ano e mês:")
  print(mean_time_difference_per_month(df))


  df.drop('Data', axis=1, inplace=True)

  df = format(df)

  if has_seconds(df):
    subset = df[df['Time'].apply(lambda x: ':00' not in x)]
    print("\n Os dados com valor nos segundos:")
    print(subset)
  else:
    print("\n O valor dos segundos está sempre a 00.\n")


  print(f"Existem medições de {num_unique_dates(df)} dias distintos.\n")

  date_datetime(df)

  print("Temos dados dos seguintes anos:")
  print(unique_years(df))

  if is_ordered_ascending(df):
    print("\n Os dados estão organizados de forma cronológica.\n")
  else:
    print("\n Os dados não estão organizados de forma cronológica.\n")
    df = sort_date(df)

  date_date_format(df)
  print(f"A primeira medição foi feita em: {df['Date'][0]}\n")
  print(f"A ultima medição foi feita em: {df['Date'][len(df)-1]}\n")

  date_datetime(df)
  df = year_month_day(df)

  print(f"Valor médio de medições diárias: {average_measurements_per_day(df)} \n")

  print("Valor médio de medições diárias por ano:")
  print(average_measurements_per_year(df))

  print("\nValor médio de medições diárias por ano e mês:")
  print(average_measurements_per_year_month(df))

  measurements_per_year_month_boxplot(df)

  print("\n Quantos meses tiveram medições naquele ano:")
  print(unique_month_counts(df))

  print("\n Quantos dias tiveram medições naquele ano:")
  print(unique_days_counts(df))
  print('\n')

  expected_days_print(df)

  caudal_values_chart(df)
  caudal_values_chart_yearly(df)

  time_datetime(df)

  if not invalid_time_values(df).empty:
    print("\n Existem falhas no tempo das seguintes leituras:")
    print(invalid_time_values(df))
  else:
    print("\n Não existem falhas nos tempos")

  time_time(df)

  if not fails(df).empty:
    print("\n Existem as seguintes falhas nos dados:")
    print(format(fails(df)))
  else:
    print("\n Não existem falhas nos dados.")

  print(f"\n Existem {total_fails(df)} falhas de leituras \n")

  correct_caudal(df)

  fails_count = non_integer_counts(df)
  print("Número de falhas por ano:")
  print(fails_count)

  days_without_data = days_with_no_data(df)
  if len(days_without_data) > 0:
    print("\n Existem dias inteiros sem valores.")
    print("Dias sem valores:", days_without_data)
  else:
    print("\n Todos os dias tem pelo menos uma medição sem falhas.")

  entrys_year = entrys_per_year(df)
  print('\n Número de medições por ano:')
  print(entrys_year)

  entries_without_fails_per_year = entries_without_errors_per_year(entrys_year, fails_count)
  print("\n Número de medições sem falhas:")
  print(entries_without_fails_per_year)

  entries_without_fails_per_year_percent = entries_without_errors_per_year_percent(entries_without_fails_per_year)
  print("\n Percentagem de medições sem falhas:")
  print(entries_without_fails_per_year_percent)

  print("\n Percentagem de medições com falhas:")
  print(entries_with_errors_per_year_percent(entries_without_fails_per_year_percent))

  print('\n')
  means_caudal_yearly(df)
  means_caudal(df)

  print("\n", (std_monthly(df_no_errors(df)))[['Year', 'Month', 'Desvio_Padrao']])
  print("\n", (std_yearly(df_no_errors(df)))[['Year', 'Desvio_Padrao']])

  print('\n')
  caudal_boxplots(df)
  print('\n')
  print(caudal_statistics(df_no_errors(df)))
#Funcoes Normalizacao


def normalize(resampled_df, time):
    for col in resampled_df.columns:

        missing_mask = resampled_df[col].isnull()

        for idx, value in resampled_df[col][missing_mask].items():

            before_idx = None
            for i in reversed(range(resampled_df.index.get_loc(idx))):
                if not pd.isnull(resampled_df.at[resampled_df.index[i], col]):
                    before_idx = resampled_df.index[i]
                    break
            after_idx = None
            for i in range(resampled_df.index.get_loc(idx), len(resampled_df.index)):
                if not pd.isnull(resampled_df.at[resampled_df.index[i], col]):
                    after_idx = resampled_df.index[i]
                    break

            if before_idx is not None and after_idx is not None and (after_idx - before_idx).total_seconds() <= pd.Timedelta(minutes=time).total_seconds():
                resampled_df.at[idx, col] = resampled_df[col][before_idx] + \
                                            ((resampled_df[col][after_idx] - resampled_df[col][before_idx]) /
                                            (after_idx - before_idx).total_seconds()) * \
                                            (idx - before_idx).total_seconds()

def years(df):
  return df.index.year.unique()

def normalizedPlot(df, time):

  plt.figure(figsize=(10, 6))


  for year in years(df):

      year_data = df[df.index.year == year]

      plt.plot(year_data.index, year_data['Caudal'], label=str(year))

  plt.xlabel('Data')
  plt.ylabel('Caudal')
  plt.title(f'Valores normalizados com intervalo máximo de {time} minutos')
  plt.legend(title='Ano')
  plt.show()

def calculate_mean_area(df):
    mean_areas = {}
    for date, data in df.groupby(df.index.date):
        times = data.index.time
        values = data['Caudal']
        areas = []
        for i in range(len(values) - 1):
            if not pd.isnull(values[i]) and not pd.isnull(values[i + 1]):
                x = np.array([times[i].hour * 3600 + times[i].minute * 60 + times[i].second,
                              times[i + 1].hour * 3600 + times[i + 1].minute * 60 + times[i + 1].second])
                y = np.array([values[i], values[i + 1]])
                areas.append(np.trapz(y, x))
        if areas:
            mean_areas[date] = np.mean(areas)
    return mean_areas

def diference(df, column1, column2):
  plt.figure(figsize=(10, 6))
  plt.plot(df['Date'], df[f'{column1}'] - df[f'{column2}'], marker='o')
  plt.xlabel('Date')
  plt.ylabel('Difference in Area')
  plt.title('Difference in Daily Mean Area between Old and New DataFrames')
  plt.xticks(rotation=45)
  plt.grid(True)
  plt.tight_layout()
  plt.show()

def comparison(df, column1, column2):
  df.plot(kind='scatter', x=column1, y=column2, s=32, alpha=.8)
  plt.gca().spines[['top', 'right',]].set_visible(False)

def remove_outliers_iqr(df, column):
    df['Year'] = df['Data'].dt.year
    df['Month'] = df['Data'].dt.month
    grouped = df.groupby(['Year', 'Month'])

    df_filtered = pd.DataFrame()
    outliers_above = pd.DataFrame()
    outliers_below = pd.DataFrame()

    for (year, month), group in grouped:
        Q1 = group[column].quantile(0.25)
        Q3 = group[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 3 * IQR
        upper_bound = Q3 + 3 * IQR

        group_filtered = group[(group[column] >= lower_bound) & (group[column] <= upper_bound)]
        outliers_above_group = group[group[column] > upper_bound]
        outliers_below_group = group[group[column] < lower_bound]

        df_filtered = pd.concat([df_filtered, group_filtered])
        outliers_above = pd.concat([outliers_above, outliers_above_group])
        outliers_below = pd.concat([outliers_below, outliers_below_group])

    return df_filtered, outliers_above, outliers_below

def boxplot_outliers(df):
  df['Data'] = pd.to_datetime(df['Data'])

  plt.figure(figsize=(10, 6))
  plt.boxplot(df['Caudal'], whis=100)
  plt.title('Diagrama de Caixas dos Outliers')
  plt.ylabel('Caudal')
  plt.xticks([1], ['Caudal'])
  plt.grid(True)
  plt.show()

def statistics(df_no_errors):
    dfs = []

    df_no_errors['Year'] = df_no_errors['Data'].dt.year
    df_no_errors['Month'] = df_no_errors['Data'].dt.month

    for year in df_no_errors['Year'].unique():
        for month in df_no_errors['Month'].unique():
            subset_data = df_no_errors[(df_no_errors['Year'] == year) & (df_no_errors['Month'] == month)]

            if not subset_data.empty:
                min_value = subset_data['Caudal'].min()
                max_value = subset_data['Caudal'].max()
                count = len(subset_data)

                dfs.append(pd.DataFrame({
                    'Year': [year],
                    'Month': [month],
                    'Min_Value': [min_value],
                    'Max_Value': [max_value],
                    'Count': [count]
                }))

    summary_df = pd.concat(dfs, ignore_index=True)

    summary_df_sorted = summary_df.sort_values(by=['Year', 'Month'])
    return summary_df_sorted

def missings_study(df):
  df['TimeDiff'] = df['Data'].diff()

  group_start = df.iloc[0]['Data']
  group_count = 1

  result_dates = []
  result_consecutive_points = []
  result_time = []

  for i in range(1, len(df)):
      if df.iloc[i]['Data'] - df.iloc[i - 1]['Data'] > pd.Timedelta(minutes=15):
          result_dates.append(group_start)
          result_consecutive_points.append(group_count)
          duration_minutes = group_count * 15
          days = duration_minutes // (24 * 60)
          remaining_minutes = duration_minutes % (24 * 60)
          hours = remaining_minutes // 60
          minutes = remaining_minutes % 60
          time_str = f"{days} days {hours:02d}:{minutes:02d}:00"
          result_time.append(time_str)
          group_start = df.iloc[i]['Data']
          group_count = 1
      else:
          group_count += 1

  result_dates.append(group_start)
  result_consecutive_points.append(group_count)
  duration_minutes = (group_count - 1) * 15
  days = duration_minutes // (24 * 60)
  remaining_minutes = duration_minutes % (24 * 60)
  hours = remaining_minutes // 60
  minutes = remaining_minutes % 60
  time_str = f"{days} days {hours:02d}:{minutes:02d}:00"
  result_time.append(time_str)

  return pd.DataFrame({'Data': result_dates, 'Consecutive_Points': result_consecutive_points, 'Time': result_time})

def convert_to_time(value):
    minutes = value * 15
    hours = minutes // 60
    minutes = minutes % 60
    days = hours // 24
    hours = hours % 24
    seconds = 0
    return '{} days {:02d}:{:02d}:{:02d}'.format(int(days), int(hours), int(minutes), int(seconds))

def convert_to_time_less_than_1day(value):
    minutes = value * 15
    hours = minutes // 60
    minutes = minutes % 60
    seconds = 0
    return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))
##fucnoes modificadas
def resultadosModificada_para_falhas(df):
    date_and_time(df)

    if (duplicates(df)).any():
        df = df.drop_duplicates(subset=['Data'])

    df.drop('Data', axis=1, inplace=True)

    df = format(df)

    if has_seconds(df):
        subset = df[df['Time'].apply(lambda x: ':00' not in x)]

    date_datetime(df)

    if not is_ordered_ascending(df):
        df = sort_date(df)

    date_date_format(df)

    date_datetime(df)
    df = year_month_day(df)


    time_datetime(df)
    time_time(df)
    correct_caudal(df)

    fails_count = non_integer_counts(df)

    entrys_year = entrys_per_year(df)

    entries_without_fails_per_year = entries_without_errors_per_year(entrys_year, fails_count)

    return entries_without_errors_per_year_percent(entries_without_fails_per_year)

