import os
import json

from pathlib import Path
from uuid import uuid4
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


# ==========================================
# CONFIGURATION DES CHEMINS
# ==========================================

ROOT_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# CHARGEMENT DES DONNEES DE TEST
# ==========================================

def before_all(context):

    # Chargement des variables d'environnement
    load_dotenv(ROOT_DIR / ".env")

    # Chargement des donnees JSON
    with open(
        ROOT_DIR / "test_data.json",
        "r",
        encoding="utf-8"
    ) as file:

        context.test_data = json.load(file)

    # Configuration du site
    context.base_url = os.getenv(
        "BASE_URL",
        "https://automationexercise.com"
    )

    # Informations de connexion
    context.test_password = os.getenv("TEST_PASSWORD")

    # Informations de paiement fictives
    context.payment_data = {
        "name": os.getenv("PAYMENT_NAME"),
        "card_number": os.getenv("PAYMENT_CARD_NUMBER"),
        "cvc": os.getenv("PAYMENT_CVC"),
        "expiry_month": os.getenv("PAYMENT_EXPIRY_MONTH"),
        "expiry_year": os.getenv("PAYMENT_EXPIRY_YEAR")
    }


# ==========================================
# INITIALISATION AVANT CHAQUE SCENARIO
# ==========================================

def before_scenario(context, scenario):

    # Initialisation du navigateur
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()

    # Configuration des attentes Selenium
    context.wait = WebDriverWait(context.driver, 20)

    # Adresse unique pour chaque execution
    context.email = f"qa.bdd.test.{uuid4().hex[:12]}@example.com"

    # Blocage des requetes publicitaires
    context.driver.execute_cdp_cmd("Network.enable", {})

    context.driver.execute_cdp_cmd(
        "Network.setBlockedURLs",
        {
            "urls": [
                "*googlesyndication.com/*",
                "*doubleclick.net/*",
                "*googleadservices.com/*",
                "*adservice.google.com/*",
                "*adtrafficquality.google/*"
            ]
        }
    )


# ==========================================
# NETTOYAGE APRES CHAQUE SCENARIO
# ==========================================

def after_scenario(context, scenario):

    if hasattr(context, "driver"):
        context.driver.quit()