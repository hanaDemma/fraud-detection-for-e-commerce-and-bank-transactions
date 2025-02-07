
import pandas as pd

def load_data(docs):
    """
    Loads datasets required for fraud detection analysis.

    Parameters:
    docs (str): The directory path where the datasets are stored.

    Returns:
    tuple: A tuple containing three Pandas DataFrames:
        - Credit_Card: Data on bank transactions with fraud labels.
        - Fraud_Data: E-commerce transaction data for fraud detection.
        - IP_Address_To_Country: Mapping of IP address ranges to country locations.
    """
    # Load credit card transaction dataset
    Credit_Card = pd.read_csv(f'{docs}/creditcard.csv')

    # Load e-commerce fraud transaction dataset
    Fraud_Data = pd.read_csv(f'{docs}/Fraud_Data.csv')

    # Load IP address to country mapping dataset
    IP_Address_To_Country = pd.read_csv(f'{docs}/IpAddress_to_Country.csv')

    return Credit_Card, Fraud_Data, IP_Address_To_Country
