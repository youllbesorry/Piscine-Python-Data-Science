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

def create_tabls(engine, table_name):
    meta_data = db.MetaData()
    
    with engine.connect() as conn:
        conn.execute(db.text(f"DROP TABLE IF EXISTS {table_name}"))
        conn.commit()

    table = db.Table(table_name, meta_data,
            db.Column('event_time', db.DateTime, index=True),
            db.Column('event_type', db.String(100)),
            db.Column('product_id', db.Integer),
            db.Column('price', db.Float),
            db.Column('user_id', db.BigInteger),
            db.Column('user_session', db.UUID))

    meta_data.create_all(engine)
    print(f"Table {table_name} have been crate with succes")

def import_csv_to_db(path):
    try:
        df = load(path)
    except TypeError as e:
        print(e)
    db_params = find_db_params()
    engine = db.create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")

    try:
        db_name = path.split("/")[-1].split(".csv")[0]
        print(db_name)
        create_tabls(engine, db_name)
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
