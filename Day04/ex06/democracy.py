from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
import sys
import numpy as np

def transform_data(data):
    data_transformed = data.copy()

    if 'knight' in data_transformed.columns:
        data_transformed['knight'] = data_transformed['knight'].apply(
            lambda x: 1 if x == 'Jedi' else 0)

        X = data_transformed.drop('knight', axis=1)
        y = data_transformed['knight']

        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        result = X_scaled.copy()
        result['knight'] = y

        X = result.iloc[:, :-1].values
        Y = result.iloc[:, -1].values

        return result, X, Y
    else:
        scaler = StandardScaler()
        X_scaled = pd.DataFrame(scaler.fit_transform(data_transformed), 
                               columns=data_transformed.columns)

        X = X_scaled.values
        return X_scaled, X, None

def KNN(X_train, y_train, X_val, y_val):
    k_values = range(1, 31)
    accuracy_scores = []
    
    for k in k_values:
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)
        
        y_pred_val = model.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred_val)
        accuracy_scores.append(accuracy * 100)
    
    best_k = k_values[np.argmax(accuracy_scores)]
    print(f'Best K value: {best_k} with accuracy: {max(accuracy_scores):.2f}%')
    
    final_model = KNeighborsClassifier(n_neighbors=best_k)
    final_model.fit(X_train, y_train)
    
    return final_model

def Tree(X_train, y_train):
    model = DecisionTreeClassifier(random_state=1)
    model.fit(X_train, y_train)
    return model

def LogReg(X_train, y_train):
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    return model

def VotingModel(train_data):
    data_transformed, X, y = transform_data(train_data)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42)
    
    knn_model = KNN(X_train, y_train, X_val, y_val)
    tree_model = Tree(X_train, y_train)
    logreg_model = LogReg(X_train, y_train)
    
    voting_clf = VotingClassifier(
        estimators=[
            ('knn', knn_model),
            ('tree', tree_model),
            ('logreg', logreg_model)
        ],
        voting='hard'
    )
    
    voting_clf.fit(X_train, y_train)
    
    y_pred_val = voting_clf.predict(X_val)
    accuracy = accuracy_score(y_val, y_pred_val)
    f1 = f1_score(y_val, y_pred_val)
    
    print(f'Validation Accuracy: {(accuracy * 100):.2f}%')
    print(f'Validation F1 Score: {(f1 * 100):.2f}%')
    
    for name, model in [('KNN', knn_model), ('Tree', tree_model), ('LogReg', logreg_model)]:
        y_pred = model.predict(X_val)
        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)
        print(f'{name} - Accuracy: {(acc * 100):.2f}%, F1 Score: {(f1 * 100):.2f}%')
    
    return voting_clf

def predict_test_data(model, test_data):
    _, X_test, _ = transform_data(test_data)

    y_pred = model.predict(X_test)

    predictions = ['Jedi' if pred == 1 else 'Sith' for pred in y_pred]

    with open('Voting.txt', 'w') as f:
        for prediction in predictions:
            f.write(f"{prediction}\n")

    return predictions

def main():
    if (len(sys.argv) != 3):
        print("Usage: python democracy.py <train_file.csv> <test_file.csv>")
        return

    train_data = pd.read_csv(sys.argv[1])

    model = VotingModel(train_data)

    test_data = pd.read_csv(sys.argv[2])

    predict_test_data(model, test_data)

if __name__ == "__main__":
    main()
