import pandas as pd
import psycopg2
import sqlalchemy as db
import sys
from dotenv import load_dotenv
import os


def load(path: str) -> pd.DataFrame:
    """
    Charge un fichier CSV à partir du chemin spécifié et
    retourne un DataFrame Pandas.

    Paramètres:
    path (str): Le chemin du fichier CSV à charger.

    Retourne:
    pd.DataFrame: Un DataFrame contenant les données du fichier CSV.
    None: Retourne None si une erreur se produit lors du chargement du fichier.

    Exceptions:
    TypeError: Si le chemin fourni n'est pas une
    chaîne de caractères.
    UnicodeDecodeError: Si le fichier ne peut pas être décodé
    correctement (mauvais format).
    FileNotFoundError: Si le fichier spécifié n'est pas trouvé.
    """
    try:
        if (type(path) is not str):
            raise TypeError("The path must be an str")
        df = pd.DataFrame()
        df = pd.read_csv(path)
        print(f"Loading dataset of dimensions {df.shape}")
        return df
    except (UnicodeDecodeError, FileNotFoundError, TypeError) as e:
        print(e)
        return None

def find_db_params():
    load_dotenv("../utils/.env")
    return {
        'host': os.getenv('POSTGRES_HOST'),
        'database': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD')
    }

def create_items_tabls(engine):
    meta_data = db.MetaData()

    items = db.Table('items', meta_data,
            db.Column('product_id', db.Integer, index=True),
            db.Column('category_id', db.BigInteger),
            db.Column('category_code', db.String(100)),
            db.Column('brand', db.String(50)))

    meta_data.create_all(engine)
    print("Table 'items' have been crate with succes")

def import_csv_to_db(path):
    try:
        df = load(path)
    except TypeError as e:
        print(e)
    db_params = find_db_params()
    engine = db.create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")

    create_items_tabls(engine)

    try:
        db_name = f"{path.split('/')[-1].split('.csv')[0]}s"
        print(db_name)
        with engine.connect() as conn:
            conn.execute(db.text(f"DROP TABLE IF EXISTS {db_name}"))
            conn.commit()
        create_items_tabls(engine)
        df.to_sql(db_name, engine, if_exists='append', index=False)
        print("Import réussi dans la base de données")
    except Exception as e:
        print(f"Erreur lors de l'import : {e}")
    finally:
        engine.dispose()
        

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("ERROR : You must input at least 1 path")
        sys.exit()
    for i in range(1, len(sys.argv)):
        print(sys.argv[i])
        import_csv_to_db(sys.argv[i])
