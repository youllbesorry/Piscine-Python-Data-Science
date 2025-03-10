import os
import psycopg2
from dotenv import load_dotenv

def connect_to_db_psycopg():
    """
    Établit une connexion à la base de données PostgreSQL.
    
    Returns:
        connection: Objet de connexion PostgreSQL
    """
    load_dotenv("../utils/.env")
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn

def fusion_tables_sql():
    """
    Fusionne la table 'items' dans la table 'customers' en ajoutant
    les colonnes manquantes de la table items.
    """
    conn = connect_to_db_psycopg()
    cur = conn.cursor()
    
    try:
        # Ajout des colonnes de la table items dans la table customers
        cur.execute("""
            ALTER TABLE customers 
            ADD COLUMN IF NOT EXISTS category_id VARCHAR,
            ADD COLUMN IF NOT EXISTS category_code VARCHAR,
            ADD COLUMN IF NOT EXISTS brand VARCHAR;
        """)

        # Mise à jour des nouvelles colonnes avec les données de la table items
        cur.execute("""
            UPDATE customers c
            SET 
                category_id = i.category_id,
                category_code = i.category_code,
                brand = i.brand
            FROM items i
            WHERE c.product_id = i.product_id;
        """)
        
        conn.commit()
        
        # Récupération du nombre de lignes mises à jour
        cur.execute("SELECT COUNT(*) FROM customers")
        count = cur.fetchone()[0]
        print(f"Fusion terminée. {count} lignes dans la table customers.")
        
    except Exception as e:
        conn.rollback()
        print(f"Une erreur s'est produite : {str(e)}")
        raise
    finally:
        cur.close()
        conn.close()

def main():
    """
    Fonction principale qui exécute la fusion des tables.
    """
    try:
        print("Début de la fusion SQL...")
        fusion_tables_sql()
        print("Opération terminée avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    main()
