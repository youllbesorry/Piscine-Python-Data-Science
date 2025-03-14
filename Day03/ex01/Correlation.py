import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
   
def transform_data(data):
    data_transformed = data.copy()
    
    data_transformed['knight'] = data_transformed['knight'].apply(lambda x: 1 if x == 'Jedi' else 0)
    return data_transformed

def calculate_correlation(data):
    
    correlation_matrix = data.corr(numeric_only=True)
    
    knight_correlations = correlation_matrix['knight']
    
    sorted_correlations = knight_correlations.sort_values(ascending=False)
    
    sorted_correlations = knight_correlations[sorted_correlations.index]

    for feature, corr in sorted_correlations.items():
        print(f"{feature}: {corr:.4f}")
    
    return sorted_correlations
        
    
def main():
    train_csv = load("../Train_knight.csv")
    transformed_data = transform_data(train_csv)
    calculate_correlation(transformed_data)

if __name__ == "__main__":
    main()