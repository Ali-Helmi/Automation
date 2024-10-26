# machine_learning/evaluation.py

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

def evaluate_model(model, test_data, test_labels):
    """
    Evaluates the trained model on test data and returns accuracy, confusion matrix, and classification report.

    Parameters:
    - model: Trained model.
    - test_data (numpy.array): Data for evaluation.
    - test_labels (numpy.array): True labels for test data.

    Returns:
    - accuracy: Model accuracy on test data.
    - conf_matrix: Confusion matrix for predictions.
    - report: Classification report with precision, recall, f1-score.
    """
    predictions = model.predict(test_data).argmax(axis=1)
    true_labels = test_labels.argmax(axis=1)
    
    accuracy = accuracy_score(true_labels, predictions)
    conf_matrix = confusion_matrix(true_labels, predictions)
    report = classification_report(true_labels, predictions)
    
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification Report:\n", report)
    
    return accuracy, conf_matrix, report

def plot_confusion_matrix(conf_matrix, class_names):
    """
    Plots the confusion matrix as a heatmap.

    Parameters:
    - conf_matrix (array): Confusion matrix.
    - class_names (list): List of class names.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", 
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.title("Confusion Matrix")
    plt.show()
