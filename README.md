# SeniorShield 🛡️
### Digital Safety Companion for Seniors

A Windows app that helps seniors with everyday tech problems AND watches for scam-like activity, alerting family members before money is lost.

**Think of it like a smoke detector for elder tech scams.**

---

## What It Does

### 🟢 Everyday Help
- Printer problems
- Internet / Wi-Fi issues
- Missing files
- Email problems
- Sound issues
- Strange screen behavior

### 🛡️ Scam Detection
- Detects when remote access tools are installed (TeamViewer, AnyDesk, etc.)
- Alerts family members immediately via email and SMS
- Asks "Are you being pressured?" when suspicious activity detected
- Runs quietly in the background

---

## Quick Start

### 1. Install Requirements

Open Command Prompt and run:

```cmd
pip install psutil Pillow twilio
```

Or install from requirements file:

```cmd
pip install -r requirements.txt
```

### 2. First Launch

Double-click `senior_shield.py` to run.

On first run, it creates a config file at:
```
C:\Users\YOURNAME\.seniorshield\config.json
```

### 3. Configure Your Trusted Contact

Open the config file in any text editor (Notepad works) and fill in:

```json
{
    "trusted_contact": {
        "name": "Sarah",
        "email": "sarah@example.com",
        "phone": "+14165551234",
        "relationship": "Daughter"
    },
    "alert_settings": {
        "email_enabled": true,
        "sms_enabled": true,
        "twilio_sid": "ACxxxxxxxxxxxx",
        "twilio_token": "xxxxxxxxxxxx",
        "twilio_from": "+15555555555"
    }
}
```

#### Getting Twilio credentials (for SMS):

1. Sign up at [twilio.com](https://www.twilio.com) (free trial)
2. Get a phone number ($1/month)
3. Copy your Account SID and Auth Token from the console
4. Paste them into the config

#### Gmail for Email Alerts:

For Gmail, you'll need an **App Password** (not your regular password):

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. → Security → 2-Step Verification (turn it on)
3. → App Passwords → Create new app password
4. Use that 16-character password as your SMTP password

Note: The email alerting in this MVP logs what would be sent. See `alerts.py` to enable real SMTP sending.

---

## How It Works

### The Home Screen

The app shows big, friendly buttons for common problems. Seniors can tap any button to get simple, plain-language help.

### Automatic Protection

The app runs in the background and watches for:
- TeamViewer, AnyDesk, UltraViewer, LogMeIn, RustDesk, etc.
- Suspicious pop-ups
- "Someone is pressuring me" button

### When Something Suspicious Happens

1. App detects suspicious activity
2. Sends email + SMS to family member immediately
3. Asks the senior "Are you okay?" with a simple Yes/No
4. If they're being pressured, family gets an urgent alert

---

## Running the App

```cmd
python senior_shield.py
```

To create a desktop shortcut:
1. Right-click `senior_shield.py`
2. → Create Shortcut
3. → Move shortcut to Desktop

---

## How to Package as .exe (Optional)

To make a standalone Windows executable:

```cmd
pip install pyinstaller
pyinstaller --onefile --windowed senior_shield.py
```

The .exe will appear in the `dist` folder.

---

## What's Monitored

### Remote Access Tools Detected:
- TeamViewer
- AnyDesk
- UltraViewer
- LogMeIn
- RustDesk
- ScreenConnect / ConnectWise Control
- Zoho Assist
- Supremo
- Ammyy Admin
- AeroAdmin

### Alert Triggers:
- Any of the above installed or launched
- User confirms they're being pressured
- User clicks "Something feels wrong"

---

## Privacy

- All config stored locally on the senior's computer
- No banking credentials accessed or stored
- Alerts are event-based, not surveillance
- Trusted contact must be configured by whoever sets it up

---

## MVP Limitations

- [ ] Email sending requires SMTP configuration in `alerts.py`
- [ ] Browser URL monitoring not yet implemented
- [ ] Banking session overlap detection not yet implemented
- [ ] Phone call detection not implemented (would require additional APIs)
- [ ] Caregiver dashboard is just the alert log for now

---

## Next Steps (Future Versions)

- [ ] System tray app (runs minimized)
- [ ] Real SMTP email integration
- [ ] Browser extension for scam URL detection
- [ ] Caregiver web dashboard
- [ ] Risk scoring system
- [ ] macOS support

---

## File Structure

```
senior-shield/
├── senior_shield.py    # Main entry point
├── gui.py              # Senior-friendly interface
├── config.py           # Configuration management
├── monitor.py          # Process monitoring
├── alerts.py           # Email/SMS alerting
├── selfhelp.py         # Self-help guides
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

*Built with ❤️ for keeping seniors safe online.*
