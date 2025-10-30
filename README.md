# TrainAlert 🚀

**Smart notification system for ML training workflows**

TrainAlert is a lightweight Python library that sends you notifications about your ML training progress via Email, Slack, or Discord. Stop checking training logs manually - get notified when your model finishes, improves, or crashes!

## Features ✨

- **Simple API**: Just 3 lines to get started
- **Multi-channel notifications**: Email, Slack, Discord
- **Smart notifications**: 
  - Training start/completion
  - Periodic epoch updates
  - Metric improvements
  - Error alerts
- **Rich visualizations**: Auto-generated training plots
- **System insights**: GPU usage, memory, training time
- **ML framework agnostic**: Works with PyTorch, TensorFlow, JAX, or any Python training loop
- **Zero configuration**: Works with .env files or direct parameters

## Installation 📦

```bash
pip install trainalert
```

Or install from source:

```bash
git clone https://github.com/yourusername/trainalert.git
cd trainalert
pip install -e .
```

## Quick Start 🚀

### Basic Usage

```python
from trainalert import TrainingNotifier

# Initialize
notifier = TrainingNotifier(
    training_name="My Awesome Model",
    email="your_email@gmail.com",
    email_password="your_app_password"
)

# Start training
notifier.start_training(config={"model": "ResNet50", "epochs": 100})

# Training loop
for epoch in range(100):
    loss = train_one_epoch()
    notifier.log_metric("loss", loss, epoch=epoch)

# Done!
notifier.training_complete()
```

That's it! You'll get beautiful email notifications with plots and system info.

## Configuration 🔧

### Email Setup (Gmail)

1. Go to your Google Account settings
2. Enable 2-factor authentication
3. Generate an "App Password" for mail
4. Use this app password in TrainAlert

### Environment Variables (Recommended)

Create a `.env` file:

```bash
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

Then just:

```python
notifier = TrainingNotifier(training_name="My Model")
```

## Advanced Usage 🎯

### PyTorch Example

```python
from trainalert import TrainingNotifier

notifier = TrainingNotifier(
    training_name="ResNet Training",
    email="your_email@gmail.com",
    email_password="your_app_password",
    notify_every_n_epochs=10,  # Notify every 10 epochs
    notify_on_improvement=True,  # Notify when metrics improve
    include_plots=True,  # Include training plots
    include_system_info=True  # Include GPU/CPU info
)

notifier.start_training(config={
    "model": "ResNet50",
    "dataset": "ImageNet",
    "batch_size": 256,
    "learning_rate": 0.1
})

for epoch in range(100):
    train_loss = train_epoch(model, train_loader)
    val_loss, val_acc = validate(model, val_loader)
    
    # Log multiple metrics
    notifier.log_metrics({
        "train_loss": train_loss,
        "val_loss": val_loss,
        "val_accuracy": val_acc
    }, epoch=epoch)

notifier.training_complete(final_metrics={
    "best_val_accuracy": best_acc,
    "final_train_loss": train_loss
})
```

### TensorFlow/Keras Example

```python
from trainalert import TrainingNotifier
import tensorflow as tf

# Custom Keras callback
class TrainAlertCallback(tf.keras.callbacks.Callback):
    def __init__(self, notifier):
        self.notifier = notifier
    
    def on_epoch_end(self, epoch, logs=None):
        self.notifier.log_metrics({
            "loss": logs['loss'],
            "accuracy": logs['accuracy'],
            "val_loss": logs['val_loss'],
            "val_accuracy": logs['val_accuracy']
        }, epoch=epoch + 1)

notifier = TrainingNotifier(training_name="Keras Model")
notifier.start_training()

model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,
    callbacks=[TrainAlertCallback(notifier)]
)

notifier.training_complete()
```

### Error Handling

```python
notifier = TrainingNotifier(
    training_name="My Model",
    notify_on_error=True  # Auto-notify on crashes
)

try:
    notifier.start_training()
    # Your training code
    for epoch in range(100):
        loss = train_epoch()
        notifier.log_metric("loss", loss, epoch=epoch)
    notifier.training_complete()
except Exception as e:
    notifier.on_error(e)  # Sends error notification with traceback
    raise
```

### Multiple Notification Channels

```python
notifier = TrainingNotifier(
    training_name="Multi-Channel Training",
    email="your_email@gmail.com",
    email_password="your_app_password",
    slack_webhook_url="https://hooks.slack.com/services/...",
    discord_webhook_url="https://discord.com/api/webhooks/..."
)

# Messages sent to all active channels!
notifier.start_training()
```

## API Reference 📚

### TrainingNotifier

#### Constructor

```python
TrainingNotifier(
    training_name: str = "ML Training",
    email: Optional[str] = None,
    email_password: Optional[str] = None,
    recipient_email: Optional[str] = None,
    provider: str = "gmail",  # 'gmail', 'outlook', 'yahoo'
    notify_every_n_epochs: int = 10,
    notify_on_improvement: bool = True,
    notify_on_error: bool = True,
    include_plots: bool = True,
    include_system_info: bool = True,
    slack_webhook_url: Optional[str] = None,
    discord_webhook_url: Optional[str] = None
)
```

#### Methods

- `start_training(config: Dict)`: Notify training start
- `log_metric(name: str, value: float, epoch: int)`: Log single metric
- `log_metrics(metrics: Dict, epoch: int)`: Log multiple metrics
- `checkpoint(message: str, metrics: Dict)`: Send checkpoint notification
- `training_complete(final_metrics: Dict)`: Notify completion
- `on_error(error: Exception)`: Send error notification

## Notification Examples 📧

### Training Start Email
```
🚀 Training Started: ResNet Training
Time: 2025-01-15 10:30:45

Configuration:
  model: ResNet50
  dataset: ImageNet
  batch_size: 256
  learning_rate: 0.1

System Information:
  Platform: Linux (3.11.0)
  CPU: Intel Core i9-9900K
  Memory: 32.0 GB
  GPUs: 2
    GPU 0: NVIDIA RTX 3090
      Memory: 12GB / 24GB (50%)
      Utilization: 85%
```

### Training Complete Email
```
✅ Training Complete: ResNet Training
Time: 2025-01-15 18:45:20

Summary:
  Total Epochs: 100
  Training Time: 8h 14m 35s

Metrics Summary:
  train_loss:
    Latest: 0.234156
    Best: 0.198234 (epoch 89)
  val_accuracy:
    Latest: 94.560000
    Best: 94.890000 (epoch 95)

[Training plots attached]
```

## Supported Email Providers 📮

- Gmail (default)
- Outlook
- Yahoo
- Custom SMTP servers

## Requirements 📋

- Python >= 3.8
- matplotlib >= 3.5.0
- numpy >= 1.21.0
- requests >= 2.26.0
- python-dotenv >= 0.19.0

Optional:
- GPUtil (for GPU monitoring)
- psutil (for CPU/memory monitoring)

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

Inspired by the needs of ML engineers who are tired of babysitting training runs!

## Support 💬

If you have any questions or run into issues:
- Open an issue on GitHub
- Check the examples/ directory for more use cases
- Read the FAQ below

## FAQ ❓

**Q: Do I need to keep my script running for notifications to work?**
A: Yes, TrainAlert sends notifications from your training script. Use tools like `screen` or `tmux` for long training runs.

**Q: Can I use this with Google Colab?**
A: Yes! Just pip install and configure your email credentials.

**Q: Does this work with distributed training?**
A: Yes, but only initialize TrainAlert on the main process (rank 0) to avoid duplicate notifications.

**Q: How do I get a Gmail app password?**
A: Go to Google Account → Security → 2-Step Verification → App Passwords. Generate a new one for "Mail".

**Q: Can I customize email templates?**
A: Yes! Check the `utils/formatting.py` file for template customization.

**Q: Is my email password stored anywhere?**
A: No, it's only used in-memory to send emails via SMTP. Use environment variables for better security.

## Roadmap 🗺️

- [ ] Telegram notifications
- [ ] WhatsApp notifications
- [ ] Web dashboard for tracking
- [ ] Integration with Weights & Biases
- [ ] Cost estimation for cloud training
- [ ] Automatic early stopping suggestions

---

Made with ❤️ for ML engineers by ML engineers