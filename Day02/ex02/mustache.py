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
    cursor.execute("""
                    SELECT COUNT(event_type) FROM customers
                    WHERE event_type = 'purchase'
                        AND event_type IS NOT NULL
                """)
    count = cursor.fetchall()
    
    cursor.execute("""
                    SELECT user_id, AVG(price) as avg_price 
                    FROM customers
                    WHERE event_type = 'purchase'
                        AND event_type IS NOT NULL
                    GROUP BY user_id
                """)
    user_rows = cursor.fetchall()
    user_columns = [desc[0] for desc in cursor.description]
    user_df = pd.DataFrame(user_rows, columns=user_columns)
    
    return df, count, user_df

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

def box_plot(df):
    plt.grid(True, alpha=0.3)
    plt.boxplot(df['price'].tolist(), vert=False, patch_artist=True,
               boxprops=dict(facecolor='lightgreen'), widths=0.7)
    plt.xlabel('price')
    plt.yticks([])
    plt.show()

def zoom_box_plot(df):
    plt.grid(True, alpha=0.3)
    plt.boxplot(df['price'].tolist(), vert=False, patch_artist=True,
               boxprops=dict(facecolor='lightgreen'), widths=0.7)
    plt.xlim(-1, 13)
    
    plt.xlabel('price')
    plt.yticks([])
    plt.tight_layout()
    plt.show()

def user_basket_box_plot(user_df):
    plt.boxplot(user_df['avg_price'].tolist(), vert=False, patch_artist=True,
               boxprops=dict(facecolor='lightblue'), widths=0.7)
    plt.grid(True, alpha=0.3)
    plt.yticks([])
    plt.tight_layout()
    plt.show()

def main():
    try:
        conn = connect_to_db_psycopg()
    except Exception as e:
        print(e)
    cursor = conn.cursor()
    df, count, user_df = extract_data(cursor)
    transform_data(df, count)
    box_plot(df)
    zoom_box_plot(df)
    user_basket_box_plot(user_df)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()