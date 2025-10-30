"""Email and message formatting utilities."""
from typing import Dict, Any, Optional
from datetime import datetime


class MessageFormatter:
    """Formats messages for different notification channels."""
    
    @staticmethod
    def format_training_start(training_name: str, config: Dict[str, Any]) -> str:
        """Format training start message."""
        lines = [
            f"🚀 Training Started: {training_name}",
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        if config:
            lines.append("Configuration:")
            for key, value in config.items():
                lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_checkpoint(message: str, metrics: Optional[Dict[str, Any]] = None) -> str:
        """Format checkpoint message."""
        lines = [
            f"📍 Checkpoint: {message}",
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        if metrics:
            lines.append("Current Metrics:")
            for key, value in metrics.items():
                if isinstance(value, float):
                    lines.append(f"  {key}: {value:.6f}")
                else:
                    lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_training_complete(
        training_name: str,
        summary: Dict[str, Any],
        final_metrics: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format training completion message."""
        lines = [
            f"✅ Training Complete: {training_name}",
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "Summary:",
            f"  Total Epochs: {summary.get('total_epochs', 'N/A')}",
            f"  Training Time: {summary.get('elapsed_time_formatted', 'N/A')}",
            "",
        ]
        
        # Add metric summary
        if 'metrics' in summary and summary['metrics']:
            lines.append("Metrics Summary:")
            for metric_name, metric_info in summary['metrics'].items():
                lines.append(f"  {metric_name}:")
                lines.append(f"    Latest: {metric_info.get('latest', 'N/A'):.6f}")
                if metric_info.get('best') is not None:
                    lines.append(f"    Best: {metric_info['best']:.6f} (epoch {metric_info.get('best_epoch', 'N/A')})")
            lines.append("")
        
        # Add final metrics if provided
        if final_metrics:
            lines.append("Final Metrics:")
            for key, value in final_metrics.items():
                if isinstance(value, float):
                    lines.append(f"  {key}: {value:.6f}")
                else:
                    lines.append(f"  {key}: {value}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_error(error_message: str, traceback: Optional[str] = None) -> str:
        """Format error message."""
        lines = [
            "❌ Training Error Occurred",
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"Error: {error_message}",
        ]
        
        if traceback:
            lines.extend([
                "",
                "Traceback:",
                traceback
            ])
        
        return "\n".join(lines)
    
    @staticmethod
    def format_improvement(metric_name: str, old_value: float, new_value: float, epoch: int) -> str:
        """Format metric improvement message."""
        is_loss = 'loss' in metric_name.lower()
        emoji = "📉" if is_loss else "📈"
        
        change = new_value - old_value
        change_str = f"{abs(change):.6f}"
        direction = "decreased" if change < 0 else "increased"
        
        return (
            f"{emoji} {metric_name.title()} Improved!\n"
            f"Epoch {epoch}: {old_value:.6f} → {new_value:.6f}\n"
            f"({direction} by {change_str})"
        )
    
    @staticmethod
    def create_html_email(
        subject: str,
        body: str,
        system_info: Optional[str] = None,
        has_plots: bool = False
    ) -> str:
        """Create HTML formatted email."""
        html_body = body.replace('\n', '<br>')
        
        html = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        padding: 20px;
                    }}
                    .container {{
                        background-color: white;
                        border-radius: 8px;
                        padding: 30px;
                        max-width: 800px;
                        margin: 0 auto;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    h2 {{
                        color: #2c3e50;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 10px;
                    }}
                    .content {{
                        color: #34495e;
                        line-height: 1.6;
                        font-family: 'Courier New', monospace;
                        background-color: #f8f9fa;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 20px 0;
                    }}
                    .system-info {{
                        background-color: #e8f4f8;
                        padding: 15px;
                        border-radius: 5px;
                        margin-top: 20px;
                        font-size: 0.9em;
                    }}
                    .footer {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #ddd;
                        color: #7f8c8d;
                        font-size: 0.85em;
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>{subject}</h2>
                    <div class="content">
                        {html_body}
                    </div>
        """
        
        if system_info:
            html += f"""
                    <div class="system-info">
                        <strong>System Information:</strong><br>
                        {system_info.replace(chr(10), '<br>')}
                    </div>
            """
        
        if has_plots:
            html += """
                    <div style="margin-top: 20px;">
                        <p><em>Training plots are attached to this email.</em></p>
                    </div>
            """
        
        html += """
                    <div class="footer">
                        Sent by TrainAlert - ML Training Notification System
                    </div>
                </div>
            </body>
        </html>
        """
        
        return html