import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from trainalert import TrainingNotifier


# Simple neural network
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(10, 50)
        self.fc2 = nn.Linear(50, 20)
        self.fc3 = nn.Linear(20, 2)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    
    avg_loss = total_loss / len(dataloader)
    accuracy = 100. * correct / total
    return avg_loss, accuracy


def main():
    """Train a PyTorch model with TrainAlert notifications."""
    
    # Initialize TrainAlert - credentials loaded from .env file
    notifier = TrainingNotifier(
        training_name="PyTorch SimpleNet Training",
        notify_every_n_epochs=10,
        notify_on_improvement=True,
        include_plots=True,
        include_system_info=True
    )
    
    # Setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Create dummy dataset
    X = torch.randn(1000, 10)
    y = torch.randint(0, 2, (1000,))
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Model, loss, optimizer
    model = SimpleNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Start training notification
    notifier.start_training(config={
        "model": "SimpleNet",
        "device": str(device),
        "batch_size": 32,
        "learning_rate": 0.001,
        "optimizer": "Adam",
        "epochs": 50
    })
    
    try:
        # Training loop
        for epoch in range(1, 51):
            train_loss, train_acc = train_epoch(model, dataloader, criterion, optimizer, device)
            
            print(f"Epoch {epoch}/50 - Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%")
            
            # Log metrics to TrainAlert
            notifier.log_metrics({
                "train_loss": train_loss,
                "train_accuracy": train_acc
            }, epoch=epoch)
        
        # Training complete
        notifier.training_complete(final_metrics={
            "final_train_loss": train_loss,
            "final_train_accuracy": train_acc
        })
        
        print("Training completed successfully!")
        
    except Exception as e:
        # Notify on error
        notifier.on_error(e)
        raise


if __name__ == "__main__":
    main()
