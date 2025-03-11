import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path


def connect_to_db_psycopg():
    env_path = Path("../utils/.env")
    if not env_path.exists():
        raise FileNotFoundError("Le fichier .env n'existe pas")
    
    load_dotenv(env_path)
    
    required_vars = ['POSTGRES_HOST',
                     'POSTGRES_DB',
                     'POSTGRES_USER',
                     'POSTGRES_PASSWORD']
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

def parse_items_table(conn, cursor):
    try:
        # Créer une table temporaire pour la fusion en gardant la première occurrence
        cursor.execute("""
            CREATE TEMP TABLE temp_items AS
            SELECT DISTINCT ON (product_id)
                product_id,
                category_id,
                category_code,
                brand
            FROM items
            ORDER BY product_id, category_id NULLS LAST;
        """)
        
        # Mettre à jour la table items avec les données fusionnées
        cursor.execute("""
            DELETE FROM items;
            
            INSERT INTO items (product_id, category_id, category_code, brand)
            SELECT product_id, category_id, category_code, brand
            FROM temp_items;
        """)
        
        # Valider les changements
        conn.commit()
        
        # Vérifier le nombre de lignes
        cursor.execute("SELECT COUNT(*) FROM items")
        row_count = cursor.fetchone()[0]
        print(f"Fusion terminée. {row_count} produits dans la table.")
            
    except Exception as e:
        conn.rollback()
        print(f"Une erreur s'est produite : {str(e)}")
        raise

def fusion_tables_sql():
    conn = connect_to_db_psycopg()
    cursor = conn.cursor()
    
    # Décommentez cette ligne pour traiter la table items d'abord
    parse_items_table(conn, cursor)
    
    try:
        # Vérifier si les colonnes existent déjà
        try:
            cursor.execute("""
                ALTER TABLE customers 
                ADD COLUMN category_id BIGINT,
                ADD COLUMN category_code VARCHAR(255),
                ADD COLUMN brand VARCHAR(255)
            """)
            conn.commit()
            print("Colonnes ajoutées à la table customers")
        except psycopg2.errors.DuplicateColumn:
            conn.rollback()
            print("Les colonnes existent déjà")
        
        # Fusion des données basée sur product_id
        cursor.execute("""
            UPDATE customers c
            SET 
                category_id = i.category_id,
                category_code = i.category_code,
                brand = i.brand
            FROM items i
            WHERE c.product_id = i.product_id
        """)
        
        # Vérifier les résultats
        cursor.execute("""
            SELECT COUNT(*) FROM customers
            WHERE category_id IS NOT NULL 
            OR category_code IS NOT NULL
            OR brand IS NOT NULL
        """)
        updated_count = cursor.fetchone()[0]
        
        conn.commit()
        print(f"Fusion réussie : {updated_count} lignes mises à jour")
        
    except Exception as e:
        conn.rollback()
        print(f"Une erreur s'est produite : {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()
        
    
    

def main():

    try:
        print("Début de la fusion SQL...")
        fusion_tables_sql()
        print("Opération terminée avec succès.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    main()
