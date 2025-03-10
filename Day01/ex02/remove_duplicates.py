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

def remove_deplicates():
    conn = connect_to_db_psycopg()
    cursor = conn.cursor()
    
    try:
        # Trouver les doublons
        find_duplicates_query = """
            SELECT MIN(event_time) as event_time, event_type, product_id, price, user_id, user_session, COUNT(*) as count
            FROM customers
            GROUP BY event_type, product_id, price, user_id, user_session, FLOOR(EXTRACT(EPOCH FROM event_time))
            HAVING COUNT(*) > 1;
        """
        
        cursor.execute(find_duplicates_query)
        duplicates = cursor.fetchall()
        
        if duplicates:
            print("Doublons trouvés :")
            for dup in duplicates:
                print(f"Entrée : {dup[:-1]}, Occurrences : {dup[-1]}")
        else:
            print("Aucun doublon trouvé")

        # Supprimer les doublons
        cursor.execute("""
            CREATE TEMPORARY TABLE temp_customers AS
            SELECT DISTINCT ON (event_type, product_id, price, user_id, user_session, FLOOR(EXTRACT(EPOCH FROM event_time))) *
            FROM customers
            ORDER BY event_type, product_id, price, user_id, user_session, FLOOR(EXTRACT(EPOCH FROM event_time)), event_time;
        """)
        
        cursor.execute("TRUNCATE TABLE customers")
        cursor.execute("INSERT INTO customers SELECT * FROM temp_customers")
        cursor.execute("DROP TABLE temp_customers")
        
        conn.commit()
        print("Suppression des doublons terminée")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur : {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    remove_deplicates()
