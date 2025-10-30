import time
import random
from trainalert import TrainingNotifier


def example_multi_channel():
    """Example: Send notifications to multiple channels."""
    print("\n=== Multi-Channel Notifications Example ===")
    
    # Credentials loaded from .env file
    # Make sure your .env has EMAIL_ADDRESS, EMAIL_PASSWORD,
    # SLACK_WEBHOOK_URL, and DISCORD_WEBHOOK_URL
    notifier = TrainingNotifier(
        training_name="Multi-Channel Training",
        notify_every_n_epochs=5
    )
    
    notifier.start_training(config={
        "model": "Transformer",
        "dataset": "Custom",
        "batch_size": 64
    })
    
    for epoch in range(1, 11):
        loss = 2.0 * (0.9 ** epoch)
        notifier.log_metric("loss", loss, epoch=epoch)
        time.sleep(0.5)
    
    notifier.training_complete()


def example_custom_checkpoints():
    """Example: Send custom checkpoint notifications."""
    print("\n=== Custom Checkpoints Example ===")
    
    # Credentials loaded from .env file
    notifier = TrainingNotifier(
        training_name="Custom Checkpoint Training",
        notify_every_n_epochs=0  # Disable automatic notifications
    )
    
    notifier.start_training()
    
    for epoch in range(1, 21):
        loss = 2.0 * (0.9 ** epoch)
        accuracy = min(0.95, 0.5 + (epoch * 0.025))
        
        notifier.log_metric("loss", loss, epoch=epoch)
        notifier.log_metric("accuracy", accuracy, epoch=epoch)
        
        # Custom checkpoint at specific epochs
        if epoch in [5, 10, 15, 20]:
            notifier.checkpoint(
                f"Milestone: Epoch {epoch}",
                metrics={
                    "loss": loss,
                    "accuracy": accuracy,
                    "learning_rate": 0.001 * (0.95 ** epoch)
                }
            )
        
        time.sleep(0.3)
    
    notifier.training_complete()


def example_error_handling():
    """Example: Automatic error notifications."""
    print("\n=== Error Handling Example ===")
    
    # Credentials loaded from .env file
    notifier = TrainingNotifier(
        training_name="Error Handling Training",
        notify_on_error=True
    )
    
    try:
        notifier.start_training()
        
        for epoch in range(1, 11):
            loss = 2.0 * (0.9 ** epoch)
            notifier.log_metric("loss", loss, epoch=epoch)
            
            # Simulate an error at epoch 5
            if epoch == 5:
                raise ValueError("Simulated training error: NaN loss detected!")
            
            time.sleep(0.3)
        
        notifier.training_complete()
        
    except Exception as e:
        # Automatically send error notification
        notifier.on_error(e)
        print(f"Error notification sent: {e}")


def example_train_val_split():
    """Example: Track training and validation metrics separately."""
    print("\n=== Train/Val Split Example ===")
    
    # Credentials loaded from .env file
    notifier = TrainingNotifier(
        training_name="Train/Val Metrics",
        notify_every_n_epochs=5,
        include_plots=True
    )
    
    notifier.start_training(config={
        "train_size": 8000,
        "val_size": 2000
    })
    
    for epoch in range(1, 21):
        # Training metrics
        train_loss = 2.0 * (0.9 ** epoch) + random.uniform(-0.05, 0.05)
        train_acc = min(0.95, 0.6 + (epoch * 0.02)) + random.uniform(-0.02, 0.02)
        
        # Validation metrics (typically worse than training)
        val_loss = train_loss + random.uniform(0.1, 0.3)
        val_acc = train_acc - random.uniform(0.02, 0.08)
        
        # Log all metrics
        notifier.log_metrics({
            "train_loss": train_loss,
            "train_accuracy": train_acc,
            "val_loss": val_loss,
            "val_accuracy": val_acc
        }, epoch=epoch)
        
        time.sleep(0.3)
    
    notifier.training_complete(final_metrics={
        "best_val_accuracy": 0.89,
        "best_val_loss": 0.35
    })


def example_learning_rate_schedule():
    """Example: Track learning rate changes."""
    print("\n=== Learning Rate Schedule Example ===")
    
    # Credentials loaded from .env file
    notifier = TrainingNotifier(
        training_name="LR Schedule Training",
        notify_every_n_epochs=10
    )
    
    initial_lr = 0.01
    notifier.start_training(config={
        "initial_lr": initial_lr,
        "lr_schedule": "cosine_annealing"
    })
    
    for epoch in range(1, 51):
        # Simulate cosine annealing LR schedule
        lr = initial_lr * (1 + np.cos(epoch * np.pi / 50)) / 2
        loss = 2.0 * (0.95 ** epoch)
        
        notifier.log_metrics({
            "loss": loss,
            "learning_rate": lr
        }, epoch=epoch)
        
        time.sleep(0.2)
    
    notifier.training_complete()


def example_minimal_notifications():
    """Example: Minimal notifications (start and end only)."""
    print("\n=== Minimal Notifications Example ===")
    
    # Credentials loaded from .env file
    notifier = TrainingNotifier(
        training_name="Minimal Notifications",
        notify_every_n_epochs=0,  # No periodic notifications
        notify_on_improvement=False,  # No improvement notifications
        include_plots=False,  # No plots
        include_system_info=False  # No system info
    )
    
    notifier.start_training()
    
    # Just log metrics without notifications
    for epoch in range(1, 101):
        loss = 2.0 * (0.95 ** epoch)
        notifier.log_metric("loss", loss, epoch=epoch)
        time.sleep(0.1)
    
    # Only get notification at the end
    notifier.training_complete()


def example_multiple_experiments():
    """Example: Track multiple experiments with different notifiers."""
    print("\n=== Multiple Experiments Example ===")
    
    experiments = [
        {"name": "Experiment_A", "lr": 0.001, "batch": 32},
        {"name": "Experiment_B", "lr": 0.01, "batch": 64},
        {"name": "Experiment_C", "lr": 0.0001, "batch": 128}
    ]
    
    # Credentials loaded from .env file for all experiments
    for exp in experiments:
        notifier = TrainingNotifier(
            training_name=exp["name"],
            notify_every_n_epochs=5
        )
        
        notifier.start_training(config=exp)
        
        # Simulate training
        for epoch in range(1, 11):
            loss = 2.0 * (0.9 ** epoch) * (1 + random.uniform(-0.1, 0.1))
            notifier.log_metric("loss", loss, epoch=epoch)
            time.sleep(0.2)
        
        notifier.training_complete()
        print(f"Completed {exp['name']}")
        time.sleep(1)


if __name__ == "__main__":
    import numpy as np
    
    print("TrainAlert Advanced Usage Examples")
    print("=" * 50)
    
    # Run different examples
    # Uncomment the ones you want to try
    
    # example_multi_channel()
    # example_custom_checkpoints()
    # example_error_handling()
    example_train_val_split()
    # example_learning_rate_schedule()
    # example_minimal_notifications()
    # example_multiple_experiments()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("Check your email/Slack/Discord for notifications.")