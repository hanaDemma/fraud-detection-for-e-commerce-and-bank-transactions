
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import LabelEncoder


def find_missing_values(df):
    """
    Identifies and summarizes missing values in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to analyze for missing values.

    Returns:
    pd.DataFrame: A summary table containing:
        - Missing values count
        - Percentage of missing values
        - Data type of each column with missing data
    """
    # Count the number of missing values in each column
    null_counts = df.isnull().sum()
    
    # Calculate the percentage of missing values
    percent_of_missing_value = 100 * null_counts / len(df)
    
    # Get the data type of each column
    data_type = df.dtypes

    # Combine all missing value statistics into a summary DataFrame
    missing_data_summary = pd.concat([null_counts, percent_of_missing_value, data_type], axis=1)

    # Rename columns for better readability
    missing_data_summary_table = missing_data_summary.rename(
        columns={0: "Missing values", 1: "Percent of Total Values", 2: "Data Type"}
    )

    # Filter out columns with no missing values and sort by percentage of missing values
    missing_data_summary_table = missing_data_summary_table[
        missing_data_summary_table.iloc[:, 1] != 0
    ].sort_values('Percent of Total Values', ascending=False).round(1)

    # Print summary message
    print(f"From {df.shape[1]} columns selected, there are {missing_data_summary_table.shape[0]} columns with missing values.")

    return missing_data_summary_table



def encoding_categorical_variables(dataframe):
    """
    Encodes categorical variables using Label Encoding.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame containing categorical columns to be encoded.

    Returns:
    pd.DataFrame: A DataFrame with categorical variables replaced by encoded values.
    """
    # Define categorical columns to encode
    categorical_columns = ['device_id', 'source', 'browser', 'country']
    
    encoder = LabelEncoder()

    for col in categorical_columns:
        if col in dataframe.columns:  # Ensure the column exists in the DataFrame
            # Apply Label Encoding and create a new column
            dataframe[col + '_encoded'] = encoder.fit_transform(dataframe[col].astype(str))
    
    # Drop original categorical columns after encoding
    dataframe.drop(columns=categorical_columns, inplace=True, errors='ignore')

    return dataframe


def univariate_analysis(credit_card_data, credit_card_data_columns):
    """
    Performs univariate analysis by plotting histograms with KDE for given numerical columns.

    Parameters:
    credit_card_data (pd.DataFrame): The dataset containing credit card transaction data.
    credit_card_data_columns (list): A list of column names for univariate analysis.

    Returns:
    None
    """
    
    for column in credit_card_data_columns:
        sns.histplot(credit_card_data[column], kde=True)
        plt.title(f'{column} Value Distribution')
        plt.show()


def bivariate_analysis(numerical_columns_data):
    """
    Performs bivariate analysis by plotting a heatmap of correlations between numerical columns.

    Parameters:
    numerical_columns_data (pd.DataFrame): A DataFrame containing only numerical columns.

    Returns:
    None
    """

    plt.figure(figsize=(10,10))
    sns.heatmap(numerical_columns_data.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation between numerical columns')
    plt.show()


def merge_fraud_ip_address_data(fraud_data, ip_address_country):
    """
    Merges fraud transaction data with IP address country mapping using an asof merge.

    Parameters:
    fraud_data (pd.DataFrame): DataFrame containing fraud transaction details, including IP addresses.
    ip_address_country (pd.DataFrame): DataFrame mapping IP address ranges to countries.

    Returns:
    pd.DataFrame: Fraud data merged with country information based on IP address ranges.
    """

    # Ensure IP addresses are numeric (in case they are stored as strings)
    fraud_data['ip_address'] = fraud_data['ip_address'].astype(int)
    ip_address_country['lower_bound_ip_address'] = ip_address_country['lower_bound_ip_address'].astype(int)
    ip_address_country['upper_bound_ip_address'] = ip_address_country['upper_bound_ip_address'].astype(int)

    # Sort the data for merge_asof (merge_asof requires sorted input)
    fraud_data = fraud_data.sort_values('ip_address')
    ip_address_country = ip_address_country.sort_values('lower_bound_ip_address')

    # Perform an asof merge to find the closest lower bound IP address match
    merged_fraud_data = pd.merge_asof(
        fraud_data, 
        ip_address_country, 
        left_on='ip_address', 
        right_on='lower_bound_ip_address', 
        direction='backward'
    )

    # Filter to ensure that the IP address falls within the assigned range
    merged_fraud_data = merged_fraud_data[
        (merged_fraud_data['ip_address'] >= merged_fraud_data['lower_bound_ip_address']) & 
        (merged_fraud_data['ip_address'] <= merged_fraud_data['upper_bound_ip_address'])
    ]

    return merged_fraud_data
