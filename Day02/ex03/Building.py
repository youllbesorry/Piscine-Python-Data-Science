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
                    SELECT user_id, COUNT(*) AS nbr_order
                    FROM customers
                    WHERE event_type = 'purchase'
                        AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-01-31 23:59:59'
                    GROUP BY user_id;
                """)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df1 = pd.DataFrame(rows, columns=column_names)
    
    cursor.execute("""
                    SELECT user_id, SUM(price) AS amount
                    FROM customers
                    WHERE event_type = 'purchase'
                        AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-01-31 23:59:59' 
                    GROUP BY user_id
                    ORDER BY amount;
                """)
    rows = cursor.fetchall()
    # column_names = [desc[0] for desc in cursor]
    df2 = [item[1] for item in rows]
    
    return df1, df2
  
def create_frequency_chart(data):
    plt.hist(data['nbr_order'], bins=5, range=[0, 40], color='#B9C4D6', 
             edgecolor='white', zorder=3)
    plt.xticks(np.arange(0, 40, 10))
    plt.show()
    
def create_monetary_chart(data):
    plt.hist(data, bins=5, range=[0, 250], color='#B9C4D6', 
             edgecolor='white', zorder=3)
    plt.xticks(np.arange(0, 250, 50))
    plt.show()
    
def main():
    try:
        conn = connect_to_db_psycopg()
        cursor = conn.cursor()
        
        data1, data2 = extract_data(cursor)
        
        create_frequency_chart(data1)
        create_monetary_chart(data2)
        
        cursor.close()
        conn.close()
        print("Charts created successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()