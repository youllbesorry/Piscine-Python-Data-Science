import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd


def calculate_variance(dataset):
    dataset['knight'] = dataset['knight'].map({'Jedi': 1, 'Sith': 0})
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dataset)
    
    pca = PCA()
    pca.fit(scaled_data)
    
    explained_variance_ratio = pca.explained_variance_ratio_
    
    cumulative_variance = np.cumsum(explained_variance_ratio) * 100
    
    n_components_90 = np.argmax(cumulative_variance >= 90) + 1
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(
        range(1, len(cumulative_variance) + 1),
        cumulative_variance,
        'b-',
        linewidth=2
    )

    print(f"Variances (Percentage): \n", explained_variance_ratio)
    print(f"Cumulative Variances (Percentage): \n", cumulative_variance)
    print(f"Number of components needed to explain 90% of variance: {n_components_90}")

    plt.xlabel('Number of components')
    plt.ylabel('Explained variance (%)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    try:
        data = pd.read_csv("../Train_knight.csv")
        
        calculate_variance(data)
    except Exception as e:
        print(f"An error occurred: {e}")
