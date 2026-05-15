import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def build_model(input_shape, task_type, num_classes=None):

    model = Sequential()

    # Input + Hidden Layers
    model.add(Dense(64, activation='relu', input_shape=(input_shape,)))

    model.add(Dense(32, activation='relu'))

    # Output layer based on task
    if task_type == "regression":

        model.add(Dense(1, activation='linear'))

        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )

    elif task_type == "classification":

        # Binary classification
        if num_classes == 2:

            model.add(Dense(1, activation='sigmoid'))

            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )

        # Multiclass classification
        else:

            model.add(Dense(num_classes, activation='softmax'))

            model.compile(
                optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )

    return model