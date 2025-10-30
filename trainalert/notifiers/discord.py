"""Discord notifier implementation."""
import requests
import io
from typing import Dict, Any, Optional, List
from .base import BaseNotifier


class DiscordNotifier(BaseNotifier):
    """Send notifications via Discord webhook."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Discord notifier.
        
        Args:
            config: Configuration with Discord webhook URL
        """
        super().__init__(config)
        
        self.webhook_url = config.get('discord_webhook_url')
        
        if not self.webhook_url:
            print("Warning: Discord webhook URL not provided. Discord notifications disabled.")
            self.enabled = False
    
    def send_message(
        self,
        subject: str,
        message: str,
        attachments: Optional[List[io.BytesIO]] = None,
        **kwargs
    ) -> bool:
        """
        Send Discord notification.
        
        Args:
            subject: Message title
            message: Message body
            attachments: Optional list of images to upload
            **kwargs: Additional parameters
        
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            # Truncate message if too long for Discord (2000 char limit in description)
            max_length = 1900  # Leave room for code blocks
            if len(message) > max_length:
                message = message[:max_length] + "\n... (truncated)"
            
            # Format message for Discord
            discord_message = {
                "embeds": [
                    {
                        "title": subject,
                        "description": f"```\n{message}\n```",
                        "color": 3447003  # Blue color
                    }
                ]
            }
            
            # Prepare files if attachments provided
            files = {}
            if attachments:
                for idx, attachment in enumerate(attachments):
                    files[f'file{idx}'] = (f'plot_{idx+1}.png', attachment.read(), 'image/png')
                    attachment.seek(0)  # Reset buffer
            
            # Send message with proper multipart/form-data encoding
            if files:
                import json
                # Use multipart/form-data for file uploads
                response = requests.post(
                    self.webhook_url,
                    data={'payload_json': json.dumps(discord_message)},
                    files=files
                )
            else:
                # Use JSON for text-only messages
                response = requests.post(
                    self.webhook_url,
                    json=discord_message,
                    headers={'Content-Type': 'application/json'}
                )
            
            if response.status_code in [200, 204]:
                print(f"✓ Discord message sent: {subject}")
                return True
            else:
                print(f"✗ Failed to send Discord message: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Failed to send Discord message: {e}")
            return False