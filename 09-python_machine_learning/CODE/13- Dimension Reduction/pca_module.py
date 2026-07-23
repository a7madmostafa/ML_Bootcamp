import numpy as np

def standardize_data(X):
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    X_std = (X - mean) / std
    return X_std


def compute_covariance_matrix(X):
    n = X.shape[0]
    covariance_matrix = np.dot(X.T, X) / (n-1)
    return covariance_matrix


def calculate_eigenvectors(covariance_matrix):
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
    return eigenvalues, eigenvectors

def select_principal_components(eigenvalues, eigenvectors, k):
    # Sort eigenvalues and eigenvectors in descending order
    sorted_indices = eigenvalues.argsort()[::-1]
    sorted_eigenvalues = eigenvalues[sorted_indices]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Select the top k eigenvectors
    selected_eigenvectors = sorted_eigenvectors[:, :k]
    return selected_eigenvectors


def transform_data(X, selected_eigenvectors):
    transformed_data = np.dot(X, selected_eigenvectors)
    return transformed_data