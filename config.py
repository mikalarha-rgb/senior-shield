"""
SeniorShield - Configuration
Stores trusted contact info, alerts, and settings.
"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".seniorshield"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_default_config():
    return {
        "trusted_contact": {
            "name": "Family Member",
            "email": "family@example.com",
            "phone": "+1234567890",  # For SMS via Twilio
            "relationship": "Son/Daughter"
        },
        "alert_settings": {
            "email_enabled": True,
            "sms_enabled": False,
            "twilio_sid": "",  # Get from twilio.com
            "twilio_token": "",
            "twilio_from": ""  # Your Twilio phone number
        },
        "monitoring": {
            "remote_access_tools": [
                "TeamViewer.exe",
                "AnyDesk.exe",
                "UltraViewer.exe",
                "LogMeIn.exe",
                "RustDesk.exe",
                "ScreenConnect.exe",
                "ConnectWise.exe",
                "ZohoAssist.exe",
                "Supremo.exe",
                "AmmyyAdmin.exe",
                "AeroAdmin.exe"
            ],
            "suspicious_keywords": [
                "microsoft support",
                "your computer is infected",
                "call now",
                "urgent security alert",
                "refund",
                "crypto recovery",
                "tech support"
            ]
        },
        "sensitivity": "medium"  # low, medium, high
    }


def ensure_config():
    """Create default config if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump(get_default_config(), f, indent=2)


def load_config():
    """Load configuration from file."""
    ensure_config()
    with open(CONFIG_FILE, "r") as f:
        saved = json.load(f)
    # Merge with defaults to handle old configs missing new keys
    defaults = get_default_config()
    for key, value in defaults.items():
        if key not in saved:
            saved[key] = value
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                if subkey not in saved[key]:
                    saved[key][subkey] = subvalue
    return saved


def save_config(config):
    """Save configuration to file."""
    ensure_config()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def update_trusted_contact(name=None, email=None, phone=None, relationship=None):
    """Update trusted contact info."""
    config = load_config()
    if name is not None:
        config["trusted_contact"]["name"] = name
    if email is not None:
        config["trusted_contact"]["email"] = email
    if phone is not None:
        config["trusted_contact"]["phone"] = phone
    if relationship is not None:
        config["trusted_contact"]["relationship"] = relationship
    save_config(config)
    return config["trusted_contact"]


def update_alert_settings(email_enabled=None, sms_enabled=None, twilio_sid=None,
                          twilio_token=None, twilio_from=None):
    """Update alert settings."""
    config = load_config()
    if email_enabled is not None:
        config["alert_settings"]["email_enabled"] = email_enabled
    if sms_enabled is not None:
        config["alert_settings"]["sms_enabled"] = sms_enabled
    if twilio_sid is not None:
        config["alert_settings"]["twilio_sid"] = twilio_sid
    if twilio_token is not None:
        config["alert_settings"]["twilio_token"] = twilio_token
    if twilio_from is not None:
        config["alert_settings"]["twilio_from"] = twilio_from
    save_config(config)
    return config["alert_settings"]
