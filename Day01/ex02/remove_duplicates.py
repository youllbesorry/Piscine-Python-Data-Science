import psycopg2
from dotenv import load_dotenv
import os
import time
from pathlib import Path

def connect_to_db_psycopg():
    # Vérifier si le fichier .env existe
    env_path = Path("../utils/.env")
    if not env_path.exists():
        raise FileNotFoundError("Le fichier .env n'existe pas")
    
    load_dotenv(env_path)
    
    # Vérifier si toutes les variables d'environnement sont présentes
    required_vars = ['POSTGRES_HOST', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Variables d'environnement manquantes: {missing_vars}")

    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        raise Exception(f"Erreur de connexion à la base de données: {e}")

def remove_duplicates():
    conn = None
    cursor = None
    
    try:
        conn = connect_to_db_psycopg()
        cursor = conn.cursor()
        
        start_time = time.time()
        
        cursor.execute("""
            CREATE TEMPORARY TABLE temp_customers AS
            WITH ranked_events AS (
                SELECT *,
                    LAG(event_time) OVER (
                        PARTITION BY event_type, product_id, price, user_id, user_session
                        ORDER BY event_time
                    ) as prev_event_time
                FROM customers
            )
            SELECT DISTINCT ON (
                event_type, product_id, price, user_id, user_session, event_time
            ) *
            FROM customers c
            WHERE NOT EXISTS (
                SELECT 1
                FROM customers c2
                WHERE c2.event_type = c.event_type
                AND c2.product_id = c.product_id
                AND c2.price = c.price
                AND c2.user_id = c.user_id
                AND c2.user_session = c.user_session
                AND c2.event_time != c.event_time
                AND ABS(EXTRACT(EPOCH FROM c.event_time - c2.event_time)) <= 1
            )
            ORDER BY 
                event_type, 
                product_id, 
                price, 
                user_id, 
                user_session,
                event_time DESC;
        """)
        
        print(f"Table temporaire créée en {time.time() - start_time:.2f} secondes")
        
        print("Vidage de la table customers...")
        start_time = time.time()
        cursor.execute("TRUNCATE TABLE customers")
        print(f"Table vidée en {time.time() - start_time:.2f} secondes")
        
        print("Réinsertion des données...")
        start_time = time.time()
        cursor.execute("""
            INSERT INTO customers 
            SELECT * FROM temp_customers
        """)
        print(f"Réinsertion terminée en {time.time() - start_time:.2f} secondes")
        
        cursor.execute("DROP TABLE temp_customers")
        conn.commit()
        print("Suppression des doublons terminée avec succès")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Erreur : {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    remove_duplicates()