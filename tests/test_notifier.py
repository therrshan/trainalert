"""Tests for TrainAlert."""
import pytest
from trainalert import TrainingNotifier
from trainalert.utils.metrics import MetricTracker


def test_metric_tracker():
    """Test metric tracking functionality."""
    tracker = MetricTracker()
    
    # Log some metrics
    tracker.log("loss", 1.0, epoch=1)
    tracker.log("loss", 0.8, epoch=2)
    tracker.log("loss", 0.6, epoch=3)
    
    # Check latest value
    assert tracker.get_latest("loss") == 0.6
    
    # Check all values
    assert tracker.get_all("loss") == [1.0, 0.8, 0.6]
    
    # Check best value (should be lowest for loss)
    best = tracker.get_best("loss")
    assert best["value"] == 0.6
    assert best["epoch"] == 3


def test_metric_tracker_improvement():
    """Test improvement detection."""
    tracker = MetricTracker()
    
    # First metric - should be improvement
    tracker.log("accuracy", 0.7, epoch=1)
    assert tracker.check_improvement("accuracy") is True
    
    # Better accuracy - should improve
    tracker.log("accuracy", 0.8, epoch=2)
    assert tracker.check_improvement("accuracy") is True
    
    # Worse accuracy - should not improve
    tracker.log("accuracy", 0.75, epoch=3)
    assert tracker.check_improvement("accuracy") is False


def test_training_notifier_init():
    """Test TrainingNotifier initialization."""
    notifier = TrainingNotifier(
        training_name="Test Training",
        email="test@example.com",
        email_password="password"
    )
    
    assert notifier.training_name == "Test Training"
    assert notifier.metric_tracker is not None


def test_log_metric():
    """Test logging single metric."""
    notifier = TrainingNotifier(training_name="Test")
    
    notifier.log_metric("loss", 1.5, epoch=1)
    
    assert notifier.metric_tracker.get_latest("loss") == 1.5


def test_log_multiple_metrics():
    """Test logging multiple metrics at once."""
    notifier = TrainingNotifier(training_name="Test")
    
    metrics = {
        "loss": 1.5,
        "accuracy": 0.85,
        "precision": 0.82
    }
    
    notifier.log_metrics(metrics, epoch=1)
    
    assert notifier.metric_tracker.get_latest("loss") == 1.5
    assert notifier.metric_tracker.get_latest("accuracy") == 0.85
    assert notifier.metric_tracker.get_latest("precision") == 0.82


def test_get_summary():
    """Test getting training summary."""
    notifier = TrainingNotifier(training_name="Test")
    
    for epoch in range(1, 6):
        notifier.log_metric("loss", 2.0 - (epoch * 0.2), epoch=epoch)
    
    summary = notifier.get_summary()
    
    assert summary["total_epochs"] == 5
    assert "metrics" in summary
    assert "loss" in summary["metrics"]


if __name__ == "__main__":
    pytest.main([__file__])