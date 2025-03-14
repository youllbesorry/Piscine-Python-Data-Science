import pandas as pd
from sklearn.model_selection import train_test_split
import sys

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

def split_data(df):
    try:
        train_df, val_df = train_test_split(
            df,
            train_size=0.80,
            test_size=0.20,
            random_state=42
        )

        train_df.to_csv("Training_knight.csv", index=False)
        val_df.to_csv("Validation_knight.csv", index=False)
        
        print(f"Données divisées avec succès :")
        print(f"Training set : {len(train_df)} échantillons ({len(train_df)/len(df)*100:.1f}%)")
        print(f"Validation set : {len(val_df)} échantillons ({len(val_df)/len(df)*100:.1f}%)")
        
    except Exception as e:
        print(f"Erreur lors de la division des données : {e}")

def main():
    if (len(sys.argv) <= 1):
        print("You must enter a least a 1 file")
        return
    for i in range(1, len(sys.argv)):
        df = load(sys.argv[i])
        split_data(df)

if __name__ == "__main__":
    main()
