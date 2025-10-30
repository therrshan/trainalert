"""Slack notifier implementation."""
import requests
import io
from typing import Dict, Any, Optional, List
from .base import BaseNotifier


class SlackNotifier(BaseNotifier):
    """Send notifications via Slack webhook."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Slack notifier.
        
        Args:
            config: Configuration with Slack webhook URL
        """
        super().__init__(config)
        
        self.webhook_url = config.get('slack_webhook_url')
        
        if not self.webhook_url:
            print("Warning: Slack webhook URL not provided. Slack notifications disabled.")
            self.enabled = False
    
    def send_message(
        self,
        subject: str,
        message: str,
        attachments: Optional[List[io.BytesIO]] = None,
        **kwargs
    ) -> bool:
        """
        Send Slack notification.
        
        Args:
            subject: Message title
            message: Message body
            attachments: Not used for Slack (webhook limitation)
            **kwargs: Additional parameters
        
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            # Format message for Slack
            slack_message = {
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": subject,
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"```{message}```"
                        }
                    }
                ]
            }
            
            response = requests.post(
                self.webhook_url,
                json=slack_message,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"✓ Slack message sent: {subject}")
                return True
            else:
                print(f"✗ Failed to send Slack message: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Failed to send Slack message: {e}")
            return False