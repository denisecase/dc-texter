"""
dc_texter/texter.py
Send an SMS text with Python and Gmail.
"""

import logging
import smtplib
from email.message import EmailMessage
from .config import load_config


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_smtp_client(port: int):
    """Return the appropriate SMTP client class based on the port.

    Args:
        port (int): The port number to check.

    Returns:
        class: The appropriate SMTP client class.
        Returns `smtplib.SMTP_SSL` for port 465
        and `smtplib.SMTP` for port 587 or other ports.
    """
    if port == 465:
        return smtplib.SMTP_SSL  # **Ensure correct SSL handling**
    elif port == 587:
        return smtplib.SMTP
    else:
        logging.warning(f"Uncommon SMTP port {port} detected. Verify your settings.")
        return smtplib.SMTP


def send_text(body: str, recipient: str = None, config_file: str = None) -> None:
    """Send a text message via an email-to-SMS gateway.

    Args:
        body (str): The text message content.
        recipient (str, optional): The recipient's phone number or email.
                                   Defaults to `sms_address_for_texts` in the config file.
        config_file (str, optional): Path to the TOML config file. Defaults to `.env.toml`.
    """
    config = load_config(config_file)

    try:
        # Load email settings from config
        host = config["outgoing_email_host"]
        port = int(config["outgoing_email_port"])
        sender_email = config["outgoing_email_address"]
        sender_password = config["outgoing_email_password"]

        # Determine the recipient (function argument takes precedence)
        if not recipient:
            if "sms_address_for_texts" in config:
                recipient = config["sms_address_for_texts"]
            else:
                raise KeyError(
                    "Recipient not provided and 'sms_address_for_texts' not found in config."
                )
        masked_recipient = recipient[:3] + "***" + recipient[-5:]  # Mask for logging

        logging.info(f"Preparing to send SMS to {masked_recipient} via {host}:{port}.")

        # Create SMS message
        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg.set_content(body)

        smtp_class = get_smtp_client(port)

        # Send the text message using SMTP
        with smtp_class(host, port) as server:
            logging.info(f"Connecting to SMTP server: {host}:{port}")

            if port == 587:  # TLS required for 587
                server.starttls()
                logging.info("TLS started.")

            server.login(sender_email, sender_password)
            logging.info(f"Logged in as {sender_email}. Sending text message...")

            server.send_message(msg)
            logging.info(f"Text message sent to {masked_recipient}.")

    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP authentication failed: Invalid username/password.")
        raise RuntimeError("Authentication error: Invalid credentials.")
    except smtplib.SMTPConnectError as e:
        logging.error(f"SMTP connection error: {e}")
        raise RuntimeError(f"SMTP connection error: {e}")
    except smtplib.SMTPRecipientsRefused as e:
        logging.error(f"Recipient refused: {masked_recipient} - {e}")
        raise RuntimeError(f"Recipient address rejected: {masked_recipient}")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
        raise RuntimeError(f"SMTP error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise RuntimeError(f"Unexpected error: {e}")


if __name__ == "__main__":
    logging.info("Ready for work.")
    smileyface = "\U0001F600"
    try:
        message = "You can send notifications from Python programs." + smileyface
        send_text(message)
        logging.info(f"SUCCESS. Text sent: {message}")
    except RuntimeError as e:
        logging.error(f"ERROR: Sending failed: {e}")
