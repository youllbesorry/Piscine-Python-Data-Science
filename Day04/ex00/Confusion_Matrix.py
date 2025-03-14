import pandas as pd
import matplotlib.pyplot as plt
import sys


def load(path: str):
    try:
        if (type(path) is not str):
            raise TypeError("The path must be an str")
        data = pd.read_fwf(path)
        return data
    except (UnicodeDecodeError, FileNotFoundError, TypeError) as e:
        print(e)
        return None

    
def transform_data(data):
    try:
        # Récupérer la première colonne et réinitialiser l'index à partir de 1
        column = data.iloc[:, 0].reset_index(drop=True)
        # Ajouter 1 à l'index pour commencer à 1
        column.index = column.index + 1
        # Transformer les valeurs
        transform = column.map({'Jedi': 1, 'Sith': 0})
        return transform.tolist()
    except Exception as e:
        print(f"Erreur de transformation : {e}")
        return None
    
def calculate_confusion_matrix(t_value, p_value):
    if len(t_value) != len(p_value):
        print("Les listes n'ont pas la même longueur")
        return None
        
    TP = 0  # True Positive (Jedi correctement identifié)
    TN = 0  # True Negative (Sith correctement identifié)
    FP = 0  # False Positive (Sith identifié comme Jedi)
    FN = 0  # False Negative (Jedi identifié comme Sith)

    # Commencer à partir de l'index 1
    for i in range(-1, len(t_value)):
        if t_value[i] == 1 and p_value[i] == 1:
            TP += 1
        elif t_value[i] == 0 and p_value[i] == 0:
            TN += 1
        elif t_value[i] == 0 and p_value[i] == 1:
            FP += 1
        elif t_value[i] == 1 and p_value[i] == 0:
            FN += 1
            
    return [[TN, FP], [FN, TP]]

def calculate_metrics(confusion_matrix):
    [[TN, FP], [FN, TP]] = confusion_matrix

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return accuracy, precision, recall, f1

def display_confusion_matrix(matrix):
    [[TN, FP], [FN, TP]] = matrix
    accuracy, precision, recall, f1 = calculate_metrics(matrix)
    
    # Affichage des métriques au format demandé
    print("              precision    recall  f1-score    total")
    print(f"Jedi          {precision:.2f}         {recall:.2f}    {f1:.2f}       {TP + FN}")
    print(f"Sith          {precision:.2f}         {recall:.2f}    {f1:.2f}       {TN + FP}")
    print(f"accuracy                           {accuracy:.2f}       {TP + TN + FP + FN}")
    
    # Affichage de la matrice
    print(f"{matrix}")

def main():
    if (len(sys.argv) != 3):
        print("You must at least enter 2 path")
        return
    
    true_value = transform_data(load(sys.argv[1]))
    predicted_value = transform_data(load(sys.argv[2]))

    print(true_value)
    print(predicted_value)

    if true_value is not None and predicted_value is not None:
        matrix = calculate_confusion_matrix(true_value, predicted_value)
        display_confusion_matrix(matrix)
        
        # Ajout de la visualisation avec matplotlib
        plt.figure(figsize=(8, 6))
        plt.imshow(matrix, cmap='YlOrRd')
        plt.colorbar()
        
        # Ajout des valeurs dans les cellules
        for i in range(2):
            for j in range(2):
                plt.text(j, i, str(matrix[i][j]), 
                        ha='center', va='center')
        
        plt.title('Matrice de Confusion')
        plt.ylabel('Valeurs Réelles')
        plt.xlabel('Valeurs Prédites')
        plt.show()

if __name__ == "__main__":
    main()