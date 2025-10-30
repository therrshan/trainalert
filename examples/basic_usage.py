"""Basic usage example for TrainAlert."""
import time
import random
from trainalert import TrainingNotifier

def main():
    """Demonstrate basic usage of TrainAlert."""
    
    # Initialize notifier - credentials loaded from .env file
    # Make sure you have EMAIL_ADDRESS and EMAIL_PASSWORD in your .env
    notifier = TrainingNotifier(
        training_name="Basic Training Example",
        notify_every_n_epochs=5,
        notify_on_improvement=True,
        include_plots=True
    )
    
    # Start training notification
    notifier.start_training(config={
        "model": "ResNet50",
        "dataset": "CIFAR-10",
        "batch_size": 32,
        "learning_rate": 0.001,
        "optimizer": "Adam"
    })
    
    # Simulate training loop
    print("Starting training...")
    for epoch in range(1, 21):
        print(f"Epoch {epoch}/20")
        
        # Simulate training
        time.sleep(1)
        
        # Generate fake metrics
        loss = 2.0 * (0.9 ** epoch) + random.uniform(-0.1, 0.1)
        accuracy = min(0.95, 0.5 + (epoch * 0.025) + random.uniform(-0.02, 0.02))
        
        # Log metrics
        notifier.log_metric("loss", loss, epoch=epoch)
        notifier.log_metric("accuracy", accuracy, epoch=epoch)
        
        # Or log multiple metrics at once
        # notifier.log_metrics({
        #     "loss": loss,
        #     "accuracy": accuracy
        # }, epoch=epoch)
    
    # Training complete
    notifier.training_complete(final_metrics={
        "final_loss": loss,
        "final_accuracy": accuracy,
        "best_accuracy": 0.95
    })
    
    print("Training complete!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Optionally notify on error
        print(f"Error: {e}")