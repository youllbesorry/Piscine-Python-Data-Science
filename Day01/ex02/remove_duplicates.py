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
        # Trouver et afficher les doublons (exacts et avec intervalle d'une seconde)
        cursor.execute("""
            WITH duplicates AS (
                SELECT 
                    c1.event_time, 
                    c1.event_type, 
                    c1.product_id, 
                    c1.price, 
                    c1.user_id, 
                    c1.user_session,
                    COUNT(*) as occurrence_count
                FROM customers c1
                JOIN customers c2 ON 
                    c1.event_type = c2.event_type AND
                    c1.product_id = c2.product_id AND
                    c1.price = c2.price AND
                    c1.user_id = c2.user_id AND
                    c1.user_session = c2.user_session AND
                    (c1.event_time = c2.event_time OR 
                     ABS(EXTRACT(EPOCH FROM (c1.event_time - c2.event_time))) <= 1)
                GROUP BY 
                    c1.event_time, 
                    c1.event_type, 
                    c1.product_id, 
                    c1.price, 
                    c1.user_id, 
                    c1.user_session
                HAVING COUNT(*) > 1
            )
            SELECT * FROM duplicates;
        """)
        
        duplicates = cursor.fetchall()
        if duplicates:
            print("Doublons trouvés :")
            for dup in duplicates:
                print(f"Entrée : {dup[:-1]}, Nombre d'occurrences : {dup[-1]}")
        else:
            print("Aucun doublon trouvé")

        # Créer une table temporaire avec les entrées uniques
        cursor.execute("""
            CREATE TEMPORARY TABLE temp_customers AS
            WITH ranked_rows AS (
                SELECT *,
                    ROW_NUMBER() OVER (
                        PARTITION BY 
                            event_type, 
                            product_id, 
                            price, 
                            user_id, 
                            user_session,
                            FLOOR(EXTRACT(EPOCH FROM event_time))
                        ORDER BY event_time
                    ) as rn
                FROM customers
            )
            SELECT 
                event_time,
                event_type,
                product_id,
                price,
                user_id,
                user_session
            FROM ranked_rows
            WHERE rn = 1;
        """)
        
        # Vider la table originale
        cursor.execute("TRUNCATE TABLE customers;")
        
        # Réinsérer les données uniques
        cursor.execute("""
            INSERT INTO customers
            SELECT * FROM temp_customers;
        """)
        
        # Supprimer la table temporaire
        cursor.execute("DROP TABLE temp_customers;")
        
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
