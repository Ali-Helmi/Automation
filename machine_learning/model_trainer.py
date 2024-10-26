# machine_learning/model_trainer.py

import tensorflow as tf
from sklearn.model_selection import train_test_split, KFold
import numpy as np

def train_model_with_cv(model, data, labels, epochs=10, batch_size=32, k_folds=5):
    """
    Trains the CNN model using k-fold cross-validation.
    
    Parameters:
    - model: Compiled CNN model.
    - data (numpy.array): Dataset for training.
    - labels (numpy.array): Labels corresponding to the data.
    - epochs (int): Number of epochs for each training fold.
    - batch_size (int): Batch size for training.
    - k_folds (int): Number of folds for cross-validation.

    Returns:
    - avg_val_accuracy: Average validation accuracy across all folds.
    - avg_val_loss: Average validation loss across all folds.
    """
    kfold = KFold(n_splits=k_folds, shuffle=True)
    val_accuracies, val_losses = [], []

    for train_idx, val_idx in kfold.split(data):
        train_data, val_data = data[train_idx], data[val_idx]
        train_labels, val_labels = labels[train_idx], labels[val_idx]
        
        history = model.fit(
            train_data, train_labels,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(val_data, val_labels)
        )
        
        val_accuracies.append(history.history['val_accuracy'][-1])
        val_losses.append(history.history['val_loss'][-1])

    avg_val_accuracy = np.mean(val_accuracies)
    avg_val_loss = np.mean(val_losses)

    return avg_val_accuracy, avg_val_loss
