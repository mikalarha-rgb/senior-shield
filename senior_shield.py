#!/usr/bin/env python3
"""
SeniorShield - Digital Safety Companion for Seniors
MVP: Scam detection + family alerting + self-help

Usage:
    python senior_shield.py

First run will create config file at ~/.seniorshield/config.json
Edit that file to set up your trusted contact and alert settings.
"""

import sys
import logging
from gui import main

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    main()
