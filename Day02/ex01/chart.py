import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import os
from datetime import datetime


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
                    SELECT DATE(event_time) as date, COUNT(DISTINCT user_id) as unique_users
                    FROM customers 
                    WHERE event_time IS NOT NULL
                        AND event_type = 'purchase'
                    GROUP BY DATE(event_time)
                    ORDER BY date
                    """)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df1 = pd.DataFrame(rows, columns=column_names)
    
    cursor.execute("""
                    SELECT DATE_TRUNC('month', event_time) as date, SUM(price) / 1000000 as sum FROM customers
                    WHERE event_type = 'purchase'
                        AND price IS NOT NULL
                    GROUP BY DATE_TRUNC('month', event_time)
                    ORDER BY date
                   """)
    
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df2 = pd.DataFrame(rows, columns=column_names)
    
    cursor.execute("""
                    SELECT 
                        DATE(event_time) AS date,
                        SUM(price) / COUNT(DISTINCT user_id) AS average_spend
                    FROM customers
                    WHERE event_type = 'purchase' 
                        AND price IS NOT NULL
                    GROUP BY DATE(event_time)
                    ORDER BY date;
                   """)
    
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df3 = pd.DataFrame(rows, columns=column_names)
    print(df3.head())
        
    return df1, df2, df3
    
def nb_customers_chart(df):
    plt.plot(df['date'], df['unique_users'])
    
    plt.xlim([datetime(2022, 10, 1), datetime(2023, 1, 31)])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylabel("Numbers of customers")
    plt.grid()
    plt.show()
    
def total_sales_chart(df):
    plt.bar(df['date'], df['sum'], width=25)
    
    plt.xlim([datetime(2022, 9, 15), datetime(2023, 1, 15)])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylabel("Total sales in million of ₳")
    plt.grid()
    plt.show()
    
def average_spend_customers(df):
    plt.plot(df['date'], df['average_spend'])
    
    plt.xlim([datetime(2022, 10, 1), datetime(2023, 1, 31)])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylabel("average spend/customers in ₳")
    plt.grid()
    plt.show()

def main():
    conn = connect_to_db_psycopg()
    cursor = conn.cursor()
    df1, df2, df3 = extract_data(cursor)
    # nb_customers_chart(df1)
    # total_sales_chart(df2)
    average_spend_customers(df3)
    
if __name__ == "__main__":
    main()
