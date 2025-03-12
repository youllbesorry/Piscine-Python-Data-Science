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

def count_row_per_column(cursor):
    results = {}
    cursor.execute("SELECT COUNT(*) FROM customers "
                   "WHERE event_type IS NOT NULL")
    results['total'] = cursor.fetchone()[0]
    for name in ['view', 'cart', 'purchase', 'remove_from_cart']:
        cursor.execute("SELECT COUNT(*) FROM customers "
                       f"WHERE event_type = '{name}' ")
        results[name] = cursor.fetchone()[0]
    print("results = ", results)
    return results

def main():
    conn = connect_to_db_psycopg()
    cursor = conn.cursor()
    result = count_row_per_column(conn, cursor)
    for key, data in result.items():
        if (key == 'total'):
            continue
        result[key] = (data / result['total']) * 100
    print("result = ", result)
    fig, ax = plt.subplots()
    ax.pie([value for key, value in result.items() if key !=  'total'], labels=[key for key in result.keys() if key != 'total'], autopct='%1.1f%%')
    plt.show()

if __name__ == "__main__":
    main()
