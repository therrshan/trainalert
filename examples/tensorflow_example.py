"""TensorFlow/Keras training example with TrainAlert.

Before running this example:
1. Create a .env file in your project root
2. Add your credentials:
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
3. Install TensorFlow: pip install tensorflow
4. Run: python examples/tensorflow_example.py
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from trainalert import TrainingNotifier


# Custom callback for TrainAlert
class TrainAlertCallback(keras.callbacks.Callback):
    """Keras callback that logs to TrainAlert."""
    
    def __init__(self, notifier):
        super().__init__()
        self.notifier = notifier
    
    def on_epoch_end(self, epoch, logs=None):
        """Log metrics at end of each epoch."""
        if logs:
            self.notifier.log_metrics({
                "train_loss": logs.get('loss', 0),
                "train_accuracy": logs.get('accuracy', 0),
                "val_loss": logs.get('val_loss', 0),
                "val_accuracy": logs.get('val_accuracy', 0)
            }, epoch=epoch + 1)


def create_model():
    """Create a simple Keras model."""
    model = keras.Sequential([
        keras.layers.Dense(64, activation='relu', input_shape=(20,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation='softmax')
    ])
    return model


def main():
    """Train a TensorFlow model with TrainAlert notifications."""
    
    # Initialize TrainAlert - credentials loaded from .env file
    notifier = TrainingNotifier(
        training_name="TensorFlow/Keras Training",
        notify_every_n_epochs=10,
        notify_on_improvement=True,
        include_plots=True,
        include_system_info=True
    )
    
    # Create dummy data
    X_train = np.random.randn(1000, 20)
    y_train = np.random.randint(0, 10, 1000)
    X_val = np.random.randn(200, 20)
    y_val = np.random.randint(0, 10, 200)
    
    # Create and compile model
    model = create_model()
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Start training notification
    notifier.start_training(config={
        "model": "Keras Sequential",
        "layers": 3,
        "optimizer": "Adam",
        "batch_size": 32,
        "epochs": 50,
        "dataset_size": len(X_train)
    })
    
    try:
        # Train with TrainAlert callback
        history = model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=32,
            callbacks=[TrainAlertCallback(notifier)],
            verbose=1
        )
        
        # Get final metrics
        final_loss = history.history['loss'][-1]
        final_acc = history.history['accuracy'][-1]
        final_val_loss = history.history['val_loss'][-1]
        final_val_acc = history.history['val_accuracy'][-1]
        
        # Training complete
        notifier.training_complete(final_metrics={
            "final_train_loss": final_loss,
            "final_train_accuracy": final_acc,
            "final_val_loss": final_val_loss,
            "final_val_accuracy": final_val_acc
        })
        
        print("Training completed successfully!")
        
    except Exception as e:
        # Notify on error
        notifier.on_error(e)
        raise


if __name__ == "__main__":
    main()