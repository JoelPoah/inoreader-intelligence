"""Email delivery system for reports"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import os
from typing import Optional

from .config import Config


class EmailDelivery:
    """Handle email delivery of reports"""
    
    def __init__(self, config: Config):
        self.config = config
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        
    def send_report(self, report_path: str, subject: Optional[str] = None) -> bool:
        """Send report via email to all recipients"""
        
        if not self.smtp_username or not self.smtp_password:
            print("Email credentials not configured. Skipping email delivery.")
            return False
        
        if not self.config.email_recipients:
            print("No email recipients configured. Skipping email delivery.")
            return False
        
        success_count = 0
        
        for recipient in self.config.email_recipients:
            try:
                # Create message
                msg = MIMEMultipart()
                msg["From"] = self.smtp_username
                msg["To"] = recipient
                msg["Subject"] = subject or f"Daily Intelligence Report - {Path(report_path).stem}"
                
                # Email body
                body = f"""
                Your daily intelligence report is ready!
                
                Report file: {Path(report_path).name}
                Generated: {Path(report_path).stat().st_mtime}
                
                Best regards,
                Inoreader Intelligence System
                """
                
                msg.attach(MIMEText(body, "plain"))
                
                # Attach report file
                with open(report_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {Path(report_path).name}"
                )
                
                msg.attach(part)
                
                # Send email
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                
                text = msg.as_string()
                server.sendmail(self.smtp_username, recipient, text)
                server.quit()
                
                print(f"Report sent successfully to {recipient}")
                success_count += 1
                
            except Exception as e:
                print(f"Failed to send email to {recipient}: {e}")
        
        return success_count > 0
    
    def send_html_report(self, report_path: str, subject: Optional[str] = None) -> bool:
        """Send HTML report as email body to all recipients"""
        
        if not self.smtp_username or not self.smtp_password:
            print("Email credentials not configured. Skipping email delivery.")
            return False
        
        if not self.config.email_recipients:
            print("No email recipients configured. Skipping email delivery.")
            return False
        
        success_count = 0
        
        # Read HTML content once
        try:
            with open(report_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        except Exception as e:
            print(f"Failed to read HTML report: {e}")
            return False
        
        for recipient in self.config.email_recipients:
            try:
                # Create message
                msg = MIMEMultipart("alternative")
                msg["From"] = self.smtp_username
                msg["To"] = recipient
                msg["Subject"] = subject or f"Daily Intelligence Report - {Path(report_path).stem}"
                
                # Plain text version
                text_body = f"""
                Your daily intelligence report is ready!
                
                Please find the report attached or view it in your email client.
                
                Best regards,
                Inoreader Intelligence System
                """
                
                # Attach both versions
                part1 = MIMEText(text_body, "plain")
                part2 = MIMEText(html_content, "html")
                
                msg.attach(part1)
                msg.attach(part2)
                
                # Send email
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                
                text = msg.as_string()
                server.sendmail(self.smtp_username, recipient, text)
                server.quit()
                
                print(f"HTML report sent successfully to {recipient}")
                success_count += 1
                
            except Exception as e:
                print(f"Failed to send HTML email to {recipient}: {e}")
        
        return success_count > 0