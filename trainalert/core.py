"""Core TrainingNotifier class."""
import traceback
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .config import Config, SMTP_CONFIGS
from .utils.metrics import MetricTracker
from .utils.system import SystemInfo
from .utils.formatting import MessageFormatter
from .visualizers.plots import PlotGenerator
from .notifiers.email import EmailNotifier
from .notifiers.slack import SlackNotifier
from .notifiers.discord import DiscordNotifier


class TrainingNotifier:
    """
    Main class for ML training notifications.
    
    Provides simple API for logging metrics and sending notifications
    during model training.
    """
    
    def __init__(
        self,
        training_name: str = "ML Training",
        email: Optional[str] = None,
        email_password: Optional[str] = None,
        recipient_email: Optional[str] = None,
        provider: str = "gmail",
        notify_every_n_epochs: int = 10,
        notify_on_improvement: bool = True,
        notify_on_error: bool = True,
        include_plots: bool = True,
        include_system_info: bool = True,
        slack_webhook_url: Optional[str] = None,
        discord_webhook_url: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize TrainingNotifier.
        
        Args:
            training_name: Name of the training run
            email: Sender email address
            email_password: Email password (app-specific password for Gmail)
            recipient_email: Recipient email (defaults to sender email)
            provider: Email provider ('gmail', 'outlook', 'yahoo', or 'custom')
            notify_every_n_epochs: Send notification every N epochs
            notify_on_improvement: Send notification when metrics improve
            notify_on_error: Send notification on training errors
            include_plots: Include metric plots in notifications
            include_system_info: Include system information in notifications
            slack_webhook_url: Slack webhook URL for notifications
            discord_webhook_url: Discord webhook URL for notifications
            config: Additional configuration dictionary
        """
        self.training_name = training_name
        self.notify_every_n_epochs = notify_every_n_epochs
        self.notify_on_improvement = notify_on_improvement
        self.notify_on_error = notify_on_error
        self.include_plots = include_plots
        self.include_system_info = include_system_info
        
        # Initialize config
        self.config = Config(config or {})
        
        # Set email configuration
        if email:
            self.config.set('email_address', email)
        if email_password:
            self.config.set('email_password', email_password)
        if recipient_email:
            self.config.set('recipient_email', recipient_email)
        
        # Set SMTP settings based on provider
        if provider in SMTP_CONFIGS:
            self.config.update(SMTP_CONFIGS[provider])
        
        # Set webhook URLs
        if slack_webhook_url:
            self.config.set('slack_webhook_url', slack_webhook_url)
        if discord_webhook_url:
            self.config.set('discord_webhook_url', discord_webhook_url)
        
        # Initialize components
        self.metric_tracker = MetricTracker()
        self.notifiers = self._setup_notifiers()
        self.training_config = {}
        
        print(f"TrainAlert initialized for '{training_name}'")
        print(f"Active notifiers: {[n.__class__.__name__ for n in self.notifiers if n.is_enabled()]}")
    
    def _setup_notifiers(self) -> List:
        """Setup notification backends."""
        notifiers = []
        
        # Email notifier
        email_notifier = EmailNotifier(self.config.config)
        if email_notifier.is_enabled():
            notifiers.append(email_notifier)
        
        # Slack notifier
        slack_notifier = SlackNotifier(self.config.config)
        if slack_notifier.is_enabled():
            notifiers.append(slack_notifier)
        
        # Discord notifier
        discord_notifier = DiscordNotifier(self.config.config)
        if discord_notifier.is_enabled():
            notifiers.append(discord_notifier)
        
        return notifiers
    
    def start_training(self, config: Optional[Dict[str, Any]] = None):
        """
        Notify training start.
        
        Args:
            config: Training configuration dictionary
        """
        self.training_config = config or {}
        message = MessageFormatter.format_training_start(self.training_name, self.training_config)
        
        system_info = None
        if self.include_system_info:
            system_info = SystemInfo.format_system_info()
            message += f"\n\n{system_info}"
        
        html = MessageFormatter.create_html_email(
            "Training Started",
            message,
            system_info=system_info if self.include_system_info else None
        )
        
        self._send_to_all_notifiers("🚀 Training Started", message, html=html)
    
    def log_metric(self, metric_name: str, value: float, epoch: Optional[int] = None):
        """
        Log a metric value.
        
        Args:
            metric_name: Name of the metric (e.g., 'loss', 'accuracy')
            value: Metric value
            epoch: Optional epoch number
        """
        self.metric_tracker.log(metric_name, value, epoch)
        
        # Check for improvement notification
        if self.notify_on_improvement and self.metric_tracker.check_improvement(metric_name):
            best_info = self.metric_tracker.get_best(metric_name)
            if best_info and len(self.metric_tracker.get_all(metric_name)) > 1:
                # Get previous value
                all_values = self.metric_tracker.get_all(metric_name)
                if len(all_values) >= 2:
                    prev_value = all_values[-2]
                    message = MessageFormatter.format_improvement(
                        metric_name, prev_value, value, epoch or len(all_values)
                    )
                    self._send_to_all_notifiers(
                        f"📈 {metric_name.title()} Improved!",
                        message
                    )
        
        # Check for epoch-based notification
        if epoch and self.notify_every_n_epochs > 0:
            if epoch % self.notify_every_n_epochs == 0:
                self.checkpoint(f"Epoch {epoch} completed")
    
    def log_metrics(self, metrics: Dict[str, float], epoch: Optional[int] = None):
        """
        Log multiple metrics at once.
        
        Args:
            metrics: Dictionary of metric names to values
            epoch: Optional epoch number
        """
        for metric_name, value in metrics.items():
            self.metric_tracker.log(metric_name, value, epoch)
        
        # Epoch-based notification
        if epoch and self.notify_every_n_epochs > 0:
            if epoch % self.notify_every_n_epochs == 0:
                self.checkpoint(f"Epoch {epoch} completed", metrics)
    
    def checkpoint(self, message: str, metrics: Optional[Dict[str, Any]] = None):
        """
        Send a checkpoint notification.
        
        Args:
            message: Checkpoint message
            metrics: Optional current metrics dictionary
        """
        # Get latest metrics if not provided
        if metrics is None:
            metrics = {}
            for metric_name in self.metric_tracker.metrics.keys():
                latest = self.metric_tracker.get_latest(metric_name)
                if latest is not None:
                    metrics[metric_name] = latest
        
        formatted_message = MessageFormatter.format_checkpoint(message, metrics)
        
        # Generate plots if requested
        attachments = None
        if self.include_plots and self.metric_tracker.metrics:
            attachments = self._generate_plots()
        
        html = MessageFormatter.create_html_email(
            "Checkpoint",
            formatted_message,
            has_plots=bool(attachments)
        )
        
        self._send_to_all_notifiers(
            f"📍 {self.training_name} - Checkpoint",
            formatted_message,
            attachments=attachments,
            html=html
        )
    
    def training_complete(self, final_metrics: Optional[Dict[str, Any]] = None):
        """
        Notify training completion.
        
        Args:
            final_metrics: Optional final metrics dictionary
        """
        summary = self.metric_tracker.get_summary()
        message = MessageFormatter.format_training_complete(
            self.training_name,
            summary,
            final_metrics
        )
        
        # Add system info
        if self.include_system_info:
            system_info = SystemInfo.format_system_info()
            message += f"\n\n{system_info}"
        
        # Generate plots
        attachments = None
        if self.include_plots and self.metric_tracker.metrics:
            attachments = self._generate_plots()
        
        html = MessageFormatter.create_html_email(
            "Training Complete",
            message,
            system_info=SystemInfo.format_system_info() if self.include_system_info else None,
            has_plots=bool(attachments)
        )
        
        self._send_to_all_notifiers(
            f"✅ {self.training_name} - Complete!",
            message,
            attachments=attachments,
            html=html
        )
    
    def on_error(self, error: Union[str, Exception]):
        """
        Notify on training error.
        
        Args:
            error: Error message or exception
        """
        if not self.notify_on_error:
            return
        
        error_message = str(error)
        traceback_str = None
        
        if isinstance(error, Exception):
            traceback_str = ''.join(traceback.format_exception(
                type(error), error, error.__traceback__
            ))
        
        message = MessageFormatter.format_error(error_message, traceback_str)
        
        html = MessageFormatter.create_html_email(
            "Training Error",
            message
        )
        
        self._send_to_all_notifiers(
            f"❌ {self.training_name} - Error!",
            message,
            html=html
        )
    
    def _generate_plots(self) -> List:
        """Generate plots for all metrics."""
        attachments = []
        
        # Generate individual plots or multi-metric plot
        if len(self.metric_tracker.metrics) <= 4:
            # Create multi-metric plot
            plot = PlotGenerator.create_multi_metric_plot(
                self.metric_tracker.metrics,
                self.metric_tracker.epochs if self.metric_tracker.epochs else None
            )
            if plot:
                attachments.append(plot)
        else:
            # Create individual plots for each metric
            for metric_name, values in self.metric_tracker.metrics.items():
                plot = PlotGenerator.create_metric_plot(
                    metric_name,
                    values,
                    self.metric_tracker.epochs if self.metric_tracker.epochs else None
                )
                attachments.append(plot)
        
        return attachments
    
    def _send_to_all_notifiers(
        self,
        subject: str,
        message: str,
        attachments: Optional[List] = None,
        html: Optional[str] = None
    ):
        """Send notification to all enabled notifiers."""
        for notifier in self.notifiers:
            if notifier.is_enabled():
                try:
                    notifier.send_message(
                        subject=subject,
                        message=message,
                        attachments=attachments,
                        html=html
                    )
                except Exception as e:
                    print(f"Error sending notification via {notifier.__class__.__name__}: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get training summary."""
        return self.metric_tracker.get_summary()