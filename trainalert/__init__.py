"""
TrainAlert - Smart notification system for ML training workflows.

Simple API for ML engineers to get notifications about training progress,
metrics, and completion via email, Slack, or Discord.
"""

from .core import TrainingNotifier
from .config import Config

__version__ = "0.1.0"
__all__ = ["TrainingNotifier", "Config"]