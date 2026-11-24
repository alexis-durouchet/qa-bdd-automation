from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def before_scenario(context, scenario):

    # Initialisation du navigateur
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()

    # Configuration du test
    context.wait = WebDriverWait(context.driver, 20)
    context.base_url = "https://automationexercise.com"

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


def after_scenario(context, scenario):

    # Fermeture du navigateur
    if hasattr(context, "driver"):
        context.driver.quit()