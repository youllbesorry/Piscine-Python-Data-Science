import psycopg2
from dotenv import load_dotenv
import os


def connect_to_db_psycopg():
    load_dotenv("../utils/.env")
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn

def load():
    try:
        conn = connect_to_db_psycopg()
        if conn.closed == 0:
            print("Connection established successfully")
        cursor = conn.cursor()
    except psycopg2.Error as e:
        print(e)
        return None

    cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name LIKE 'data\_202%\_%' 
    ESCAPE '\\'
    """)
    
    data_tables = [table[0] for table in cursor.fetchall()]
    
    if not data_tables:
        print("No matching table found")
        cursor.close()
        conn.close()
        return
    
    for table_name in data_tables:
        print(f"Table found: {table_name}")
    
    cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'customers'
    )
    """)
    
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        base_table = data_tables[0]
        cursor.execute(f"""
        CREATE TABLE customers AS 
        SELECT * FROM {base_table} 
        WHERE 1=0
        """)
        print("Table 'customers' created")
    
    cursor.execute("DELETE FROM customers")
    
    if len(data_tables) > 1:
        query = "INSERT INTO customers\n"
        query += "SELECT * FROM (\n"
        
        # Construire la requête UNION ALL
        union_queries = []
        for table in data_tables:
            union_queries.append(f"SELECT * FROM {table}")
        
        query += "\nUNION ALL\n".join(union_queries)
        query += "\n) AS combined_data"
        
        cursor.execute(query)
        conn.commit()
        print("Data from union of tables inserted into 'customers'")
    
    else:
        base_table = data_tables[0]
        cursor.execute(f"""
        INSERT INTO customers
        SELECT * FROM {base_table}
        """)
        conn.commit()
        print(f"Data from {base_table} copied to 'customers'")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    load()
