import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

def normalization(data):
    if not isinstance(data, np.ndarray):
        return None
    
    # Calcul du min et max pour chaque colonne
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    
    # Éviter la division par zéro
    range_vals = np.where(max_vals - min_vals == 0, 1, max_vals - min_vals)
    
    # Normalisation : (x - min) / (max - min)
    normalized_data = (data - min_vals) / range_vals
    
    return normalized_data

def visualize_separate(data, feature_x, feature_y, title, is_classification=True):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Vérifier si la colonne 'knight' existe dans le DataFrame
    if is_classification and ('knight' in data.columns):
        # Séparer les données en fonction de la valeur de 'knight'
        jedi = data[data['knight'] == 1]
        sith = data[data['knight'] == 0]
        
        ax.scatter(jedi[feature_x], jedi[feature_y], 
                   color='blue', label='Jedi', alpha=0.7)
        
        ax.scatter(sith[feature_x], sith[feature_y], 
                   color='red', label='Sith', alpha=0.7)
        
        ax.legend()
    else:
        ax.scatter(data[feature_x], data[feature_y], 
                   color='green', alpha=0.7)
    
    ax.set_xlabel(feature_x)
    ax.set_ylabel(feature_y)
    ax.set_title(f"{title} - {feature_x} vs {feature_y}")
    
    plt.tight_layout()
    plt.show()

def transform_data(data):
    transformed = data.copy()
    
    if 'knight' in transformed.columns:
        transformed['knight'] = transformed['knight'].map({'Jedi': 1, 'Sith': 0})
        print("Data transform")
    
    return transformed

def main():
    # Charger les données
    test_df = load("../Test_knight.csv")
    train_df = load("../Train_knight.csv")
    
    if test_df is None or train_df is None:
        return
    
    # Transformer d'abord les données (convertir 'knight' en 0/1)
    transform_test_data = transform_data(test_df)
    transform_train_data = transform_data(train_df)

    # Séparer la colonne 'knight' avant la standardisation
    # knight_test = transform_test_data['knight']
    knight_train = transform_train_data['knight']
    
    # Standardiser les données numériques (sans la colonne 'knight')
    numeric_columns = transform_test_data.select_dtypes(include=['float64', 'int64']).columns
    numeric_columns = numeric_columns.drop('knight') if 'knight' in numeric_columns else numeric_columns
    
    test_numeric = transform_test_data[numeric_columns].to_numpy()
    train_numeric = transform_train_data[numeric_columns].to_numpy()
    
    standar_test_data = normalization(test_numeric)
    standar_train_data = normalization(train_numeric)
    
    # Créer les nouveaux DataFrames avec les données standardisées
    standar_test_df = pd.DataFrame(standar_test_data, columns=numeric_columns)
    standar_train_df = pd.DataFrame(standar_train_data, columns=numeric_columns)
    
    # Rajouter la colonne 'knight'
    # standar_test_df['knight'] = knight_test
    standar_train_df['knight'] = knight_train

    print("Test data standardisé :", standar_test_df)
    print("\nTrain data standardisé :", standar_train_df)

    visualize_separate(standar_train_df, 'Empowered', 'Prescience', "Train Data")
    visualize_separate(standar_test_df, 'Empowered', 'Prescience', "Test Data")
    visualize_separate(standar_train_df, 'Deflection', 'Survival', "Test Data")
    visualize_separate(standar_test_df, 'Deflection', 'Survival', "Test Data")


if __name__ == "__main__":
    main()
