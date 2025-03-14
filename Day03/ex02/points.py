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
    transformed = data.copy()
    
    if 'knight' in transformed.columns:
        transformed['knight'] = transformed['knight'].map({'Jedi': 1, 'Sith': 0})
    
    return transformed

def visualize_separate(data, feature_x, feature_y, title, is_classification=True):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if is_classification and 'knight' in data.columns:
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
    
def visualize_mix(data, feature_x, feature_y, title, is_classification=True):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if is_classification and 'knight' in data.columns:
        jedi = data[data['knight'] == 1]
        sith = data[data['knight'] == 0]
        
        ax.scatter(jedi[feature_x], jedi[feature_y], 
                   color='blue', label='Jedi', alpha=0.7)
        
        ax.scatter(sith[feature_x], sith[feature_y], 
                   color='red', label='Sith', alpha=0.7)
    else:
        scatter = ax.scatter(data[feature_x], data[feature_y],
                            color='green', alpha=0.7)
    
    ax.set_xlabel(feature_x)
    ax.set_ylabel(feature_y)
    ax.set_title(f"{title} - {feature_x} vs {feature_y}")
    
    plt.tight_layout()
    plt.show()

def main():
    train_csv = load("../Train_knight.csv")
    test_csv = load("../Test_knight.csv")
    
    transformed_data_train = transform_data(train_csv)
    transformed_data_test = transform_data(test_csv)

    visualize_separate(transformed_data_train, 'Empowered', 'Prescience', "Train Data")
    visualize_mix(transformed_data_train, 'Deflection', 'Survival', "Train Data")
    
    visualize_separate(transformed_data_test, 'Empowered', 'Prescience', "Test Data")
    visualize_mix(transformed_data_test, 'Deflection', 'Survival', "Test Data")

if __name__ == "__main__":
    main()