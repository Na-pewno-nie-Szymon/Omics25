import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def pca_analysis(data, labels):
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data)
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    #pca_df['label'] = labels  # Dodanie etykiet
    return pca_df

def data_loader(PATH: str) -> pd.DataFrame:
    data = pd.read_excel(PATH)
    return data

def drop_name_columns(data: pd.DataFrame) -> pd.DataFrame:
    data = data.drop(columns=['Name', 'Group'])
    return data

def data_normaliser(data: np.ndarray) -> np.ndarray:
    scaler = StandardScaler()
    return scaler.fit_transform(data)

if __name__=='__main__':
    # Path to file
    PATH = 'Omics25/zajecia3/Metabolomics_Final.xlsx'

    # load data
    full_data = data_loader(PATH)
    numeric_data = drop_name_columns(full_data)
    labels = full_data['Group']  # Pobranie etykiet z kolumny 'Group'


    # Same data but in different formats (pd.DataFrame and np.ndarray)
    data_df = numeric_data
    data_columns = numeric_data.columns
    data_np = numeric_data.to_numpy()

    # Normalised data (mean = 0, std = 1)
    scaled_data = data_normaliser(data_np)

        # Check if data is scaled properly
    if not np.isclose(scaled_data.mean(), 0, atol=1e-6) or not np.isclose(scaled_data.std(), 1, atol=1e-6):
        exit('Data is not scaled properly')
    else:
        print('Data is scaled properly')

    pca_df = pca_analysis(scaled_data, labels)

        # Podział na kategorie
    categories = {
        'Male': pca_df[labels.str.startswith('M')],
        'Female': pca_df[labels.str.startswith('F')],
        'Blank': pca_df[labels == 'Blank'],
        'QC': pca_df[labels == 'QC']
    }

    # Wizualizacja wyników PCA
    plt.figure(figsize=(8, 8))
    colors = {'Male': 'blue', 'Female': 'red', 'Blank': 'green', 'QC': 'purple'}
    markers = {'Male': '.', 'Female': '.', 'Blank': 's', 'QC': '^'}  # Kwadrat dla Blank, trójkąt dla QC
    
    for label, subset in categories.items():
        plt.scatter(subset['PC1'], subset['PC2'], label=label, alpha=0.6, color=colors[label], marker=markers[label])
    
    plt.axhline(y = 0, color='grey', linestyle='--', alpha=0.6)
    plt.axvline(x = 0, color='grey', linestyle='--', alpha=0.6)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA of Metabolomics Data")
    plt.legend()
    plt.show()





