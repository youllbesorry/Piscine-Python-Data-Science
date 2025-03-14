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

def visualizer_test(df):
    if df is None or df.empty:
        print("Erreur : DataFrame vide ou invalide")
        return

    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) == 0:
        print("Aucune colonne numérique trouvée dans le DataFrame")
        return

    n_cols = 5
    n_rows = (len(numeric_columns) + n_cols - 1) // n_cols

    plt.figure(figsize=(20, 4 * n_rows))
    
    for idx, column in enumerate(numeric_columns, 1):
        plt.subplot(n_rows, n_cols, idx)
        plt.hist(df[column].dropna(), bins=50, edgecolor='black', color='green')
        plt.title(column)
        plt.ylabel('Fréquence')
    
    plt.subplots_adjust(
        hspace=0.5,
        wspace=0.3 
    )
    
    plt.show()

def visualizer_train(df):
    """
    Crée des histogrammes pour comparer les distributions entre Jedi et Sith.
    
    Args:
        df: DataFrame des chevaliers d'entraînement
    """
    if df is None or df.empty:
        print("Erreur : DataFrame vide ou invalide")
        return

    # Afficher les noms des colonnes pour debug
    print("Colonnes disponibles:", df.columns.tolist())

    # Sélectionner uniquement les colonnes numériques
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) == 0:
        print("Aucune colonne numérique trouvée dans le DataFrame")
        return

    n_cols = 5
    n_rows = (len(numeric_columns) + n_cols - 1) // n_cols

    plt.figure(figsize=(20, 20))
    
    for idx, column in enumerate(numeric_columns, 1):
        plt.subplot(n_rows, n_cols, idx)
        
        # Tracer les histogrammes séparés pour Jedi et Sith
        jedi_data = df[df['knight'] == 'Jedi'][column].dropna()  # 'Class' au lieu de 'class'
        sith_data = df[df['knight'] == 'Sith'][column].dropna()  # 'Class' au lieu de 'class'
        
        plt.hist(jedi_data, bins=50, alpha=0.5, 
                label='Jedi', edgecolor='black', color='blue')
        plt.hist(sith_data, bins=50, alpha=0.5, 
                label='Sith', edgecolor='black', color='red')
        
        plt.title(column)
        plt.ylabel('Fréquence')
        plt.legend()
    
    plt.subplots_adjust(
        hspace=0.5,
        wspace=0.3 
    )
    
    plt.show()

def main():
    test_csv = load("../Test_knight.csv")
    train_csv = load("../Train_knight.csv")
    visualizer_test(test_csv)
    visualizer_train(train_csv)

if __name__ == "__main__":
    main()