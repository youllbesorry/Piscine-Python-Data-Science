import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import os


def connect_to_db_psycopg():
    env_path = Path("../utils/.env")
    if not env_path.exists():
        raise FileNotFoundError(".env file does not exist")
    
    load_dotenv(env_path)
    
    required_vars = ['POSTGRES_HOST',
                     'POSTGRES_DB',
                     'POSTGRES_USER',
                     'POSTGRES_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing environment variables: {missing_vars}")

    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Database connection error: {e}")

def extract_data(cursor):
    cursor.execute("""
                    SELECT price FROM customers
                    WHERE event_type = 'purchase'
                        AND event_type IS NOT NULL
                """)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=column_names)
    print(df.head())
    cursor.execute("""
                    SELECT COUNT(event_type) FROM customers
                    WHERE event_type = 'purchase'
                        AND event_type IS NOT NULL
                """)
    count = cursor.fetchall()
    return df, count

def transform_data(df, count):
    statistiques = {
        'count': count[0][0],
        'mean': df['price'].mean(),
        'median': df['price'].median(),
        'min': df['price'].min(),
        'Q1': df['price'].quantile(0.25),
        'Q2': df['price'].quantile(0.5),
        'Q3': df['price'].quantile(0.75),
        'max': df['price'].max()
    }
    
    for nom, valeur in statistiques.items():
        print(f"{nom}: {valeur:.2f}")
    
    return statistiques

def main():
    conn = connect_to_db_psycopg()
    cursor = conn.cursor()
    df, count = extract_data(cursor)
    transform_data(df, count)

if __name__ == "__main__":
    main()