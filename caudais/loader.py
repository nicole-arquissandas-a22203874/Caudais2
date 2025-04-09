import pandas as pd
from .models import Medicao

def carregar_excel(arquivo_excel, serie):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(arquivo_excel)

    # Convert 'Data' column to datetime, invalid dates become NaT (null)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

    # Convert 'Caudal' column to numeric, invalid values become NaN (null)
    df['Caudal'] = pd.to_numeric(df['Caudal'], errors='coerce')

    # Create Medicao instances from the DataFrame, allowing nulls for invalid data
    medicoes_to_create = [
        Medicao(
            serie=serie,
            valor=row['Caudal'] if pd.notna(row['Caudal']) else None,  # Replace NaN with None
            timestamp=row['Data'] if pd.notna(row['Data']) else None   # Replace NaT with None
        )
        for _, row in df.iterrows()
    ]

    # Bulk insert Medicao instances into the database
    if medicoes_to_create:
        Medicao.objects.bulk_create(medicoes_to_create, batch_size=7000)

    return 'Medições carregadas com sucesso, incluindo valores nulos para dados inválidos!'
