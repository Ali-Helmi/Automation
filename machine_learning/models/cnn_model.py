# machine_learning/models/cnn_model.py

import tensorflow as tf
from tensorflow.keras import layers, models

def build_cnn_model(input_shape=(128, 128, 1), num_classes=10):
    """
    Builds and compiles a CNN model for image-based design prediction.

    Parameters:
    - input_shape (tuple): The shape of the input images (height, width, channels).
    - num_classes (int): The number of output classes for prediction.

    Returns:
    - model: A compiled CNN model.
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def train_cnn_model(model, train_data, train_labels, epochs=10, batch_size=32, validation_data=None):
    """
    Trains the CNN model on the provided dataset.

    Parameters:
    - model: The CNN model to train.
    - train_data (numpy.array): Training data.
    - train_labels (numpy.array): Labels for training data.
    - epochs (int): Number of epochs to train the model.
    - batch_size (int): Batch size for training.
    - validation_data (tuple): Optional validation data (val_data, val_labels).

    Returns:
    - history: Training history containing accuracy and loss per epoch.
    """
    history = model.fit(
        train_data, train_labels,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=validation_data
    )
    
    return history
