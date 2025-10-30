"""Email notifier implementation."""
import smtplib
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from typing import Dict, Any, Optional, List
from .base import BaseNotifier


class EmailNotifier(BaseNotifier):
    """Send notifications via email."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize email notifier.
        
        Args:
            config: Configuration with email settings
        """
        super().__init__(config)
        
        self.email_address = config.get('email_address')
        self.email_password = config.get('email_password')
        self.smtp_server = config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = config.get('smtp_port', 587)
        self.recipient_email = config.get('recipient_email', self.email_address)
        
        if not self.email_address or not self.email_password:
            print("Warning: Email credentials not provided. Email notifications disabled.")
            self.enabled = False
    
    def send_message(
        self,
        subject: str,
        message: str,
        attachments: Optional[List[io.BytesIO]] = None,
        html: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        Send email notification.
        
        Args:
            subject: Email subject
            message: Email body (plain text)
            attachments: Optional list of image attachments
            html: Optional HTML body
            **kwargs: Additional parameters
        
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            # Attach plain text
            msg.attach(MIMEText(message, 'plain'))
            
            # Attach HTML if provided
            if html:
                msg.attach(MIMEText(html, 'html'))
            
            # Attach images if provided
            if attachments:
                for idx, attachment in enumerate(attachments):
                    img = MIMEImage(attachment.read())
                    img.add_header('Content-Disposition', f'attachment; filename=plot_{idx+1}.png')
                    msg.attach(img)
                    attachment.seek(0)  # Reset buffer
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            print(f"✓ Email sent: {subject}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {e}")
            return False