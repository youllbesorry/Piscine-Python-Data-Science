import pandas as pd
import matplotlib.pyplot as plt
import sys


def load(path: str):
    try:
        if (type(path) is not str):
            raise TypeError("The path must be an str")
        data = open(path, 'r').read().splitlines()
        return data
    except (UnicodeDecodeError, FileNotFoundError, TypeError) as e:
        print(e)
        return None

    
def transform_data(data):
    try:
        transform = [1 if x == 'Jedi' else 0 for x in data]
        return transform
    except Exception as e:
        print(f"Erreur de transformation : {e}")
        return None
    
def calculate_confusion_matrix(t_value, p_value):    
    TP = 0
    TN = 0
    FP = 0
    FN = 0

    for i in range(len(t_value)):
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

    jedi_precision = TP / (TP + FP)
    sith_precision = TN / (TN + FN)

    jedi_recall = TP / (TP + FN)
    sith_recall = TN / (TN + FP)

    jedi_f1 = 2 * (jedi_precision * jedi_recall) / (jedi_precision + jedi_recall)
    sith_f1 = 2 * (sith_precision * sith_recall) / (sith_precision + sith_recall)

    return accuracy, jedi_precision, sith_precision, jedi_recall, sith_recall, jedi_f1, sith_f1

def display_confusion_matrix(matrix):
    [[TN, FP], [FN, TP]] = matrix
    accuracy, jedi_precision, sith_precision, jedi_recall, sith_recall, jedi_f1, sith_f1 = calculate_metrics(matrix)
    
    print("              precision    recall  f1-score    total")
    print(f"Jedi          {jedi_precision:.2f}         {jedi_recall:.2f}    {jedi_f1:.2f}       {TP + FN}")
    print(f"Sith          {sith_precision:.2f}         {sith_recall:.2f}    {sith_f1:.2f}       {TN + FP}")
    print(f"accuracy                           {accuracy:.2f}       {TP + TN + FP + FN}")
    
    print(f"{matrix}")

def main():
    if (len(sys.argv) != 3):
        print("You must at least enter 2 path")
        return
    
    predicted_value = transform_data(load(sys.argv[1]))
    true_value = transform_data(load(sys.argv[2]))

    if true_value is not None and predicted_value is not None:
        matrix = calculate_confusion_matrix(true_value, predicted_value)
        display_confusion_matrix(matrix)
        
        plt.figure(figsize=(8, 6))
        plt.imshow(matrix, cmap='YlOrRd')
        plt.colorbar()
        
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