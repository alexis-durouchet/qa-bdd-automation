
import unittest
from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestCartEndToEnd(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.addCleanup(self.driver.quit)

        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 20)
        self.base_url = "https://automationexercise.com"

        # Blocage des requetes publicitaires
        self.driver.execute_cdp_cmd("Network.enable", {})

        self.driver.execute_cdp_cmd(
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

        # Adresse unique pour chaque execution
        self.email = f"qa.bdd.test.{uuid4().hex[:12]}@example.com"

    def test_cart_end_to_end(self):

        driver = self.driver
        wait = self.wait

        # ==========================================
        # 1. ACCES AU SITE
        # ==========================================

        driver.get(self.base_url)

        # ==========================================
        # 2. GESTION DU CONSENTEMENT
        # ==========================================

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[normalize-space()='Autoriser']")
                )
            ).click()

        except TimeoutException:
            pass

        # ==========================================
        # 3. AJOUT DU PREMIER PRODUIT : BLUE TOP
        # ==========================================

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '.productinfo a[data-product-id="1"]')
            )
        ).click()

        modal = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#cartModal h4")
            )
        )

        self.assertEqual("Added!", modal.text.strip())

        driver.find_element(
            By.CSS_SELECTOR, "#cartModal button"
        ).click()

        wait.until(
            EC.invisibility_of_element_located(
                (By.ID, "cartModal")
            )
        )

        # ==========================================
        # 4. AJOUT DU SECOND PRODUIT : SUMMER WHITE TOP
        # ==========================================

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '.productinfo a[data-product-id="6"]')
            )
        ).click()

        modal = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#cartModal h4")
            )
        )

        self.assertEqual("Added!", modal.text.strip())

        driver.find_element(
            By.CSS_SELECTOR, "#cartModal button"
        ).click()

        wait.until(
            EC.invisibility_of_element_located(
                (By.ID, "cartModal")
            )
        )

        # ==========================================
        # 5. ACCES AU PANIER
        # ==========================================

        driver.find_element(By.LINK_TEXT, "Cart").click()

        wait.until(
            EC.url_to_be(f"{self.base_url}/view_cart")
        )

        self.assertEqual(
            f"{self.base_url}/view_cart",
            driver.current_url
        )

        # ==========================================
        # 6. VERIFICATION DES PRODUITS
        # ==========================================

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "product-1")
            )
        )

        self.assertEqual(
            "Blue Top",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-1 .cart_description h4 a"
            ).text.strip()
        )

        self.assertEqual(
            "Summer White Top",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-6 .cart_description h4 a"
            ).text.strip()
        )

        # ==========================================
        # 7. VERIFICATION DES QUANTITES
        # ==========================================

        self.assertEqual(
            "1",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-1 .cart_quantity button"
            ).text.strip()
        )

        self.assertEqual(
            "1",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-6 .cart_quantity button"
            ).text.strip()
        )

        # ==========================================
        # 8. VERIFICATION DES PRIX UNITAIRES
        # ==========================================

        self.assertEqual(
            "Rs. 500",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-1 .cart_price p"
            ).text.strip()
        )

        self.assertEqual(
            "Rs. 400",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-6 .cart_price p"
            ).text.strip()
        )

        # ==========================================
        # 9. VERIFICATION DES SOUS-TOTAUX
        # ==========================================

        self.assertEqual(
            "Rs. 500",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-1 .cart_total_price"
            ).text.strip()
        )

        self.assertEqual(
            "Rs. 400",
            driver.find_element(
                By.CSS_SELECTOR,
                "#product-6 .cart_total_price"
            ).text.strip()
        )

        # ==========================================
        # 10. CHECKOUT ET INSCRIPTION
        # ==========================================

        driver.find_element(
            By.LINK_TEXT, "Proceed To Checkout"
        ).click()

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 '#checkoutModal a[href="/login"]')
            )
        ).click()

        wait.until(
            EC.url_to_be(f"{self.base_url}/login")
        )

        driver.find_element(
            By.CSS_SELECTOR, '[data-qa="signup-name"]'
        ).send_keys("Lucas Martin")

        driver.find_element(
            By.CSS_SELECTOR, '[data-qa="signup-email"]'
        ).send_keys(self.email)

        driver.find_element(
            By.CSS_SELECTOR, '[data-qa="signup-button"]'
        ).click()

        wait.until(
            EC.url_to_be(f"{self.base_url}/signup")
        )

        # ==========================================
        # 11. CREATION DU COMPTE
        # ==========================================

        wait.until(
            EC.element_to_be_clickable(
                (By.ID, "id_gender1")
            )
        ).click()

        driver.find_element(
            By.ID, "password"
        ).send_keys("QaTest2026!E2E")

        Select(driver.find_element(
            By.ID, "days"
        )).select_by_visible_text("15")

        Select(driver.find_element(
            By.ID, "months"
        )).select_by_visible_text("June")

        Select(driver.find_element(
            By.ID, "years"
        )).select_by_visible_text("1995")

        driver.find_element(
            By.ID, "first_name"
        ).send_keys("Lucas")

        driver.find_element(
            By.ID, "last_name"
        ).send_keys("Martin")

        driver.find_element(
            By.ID, "company"
        ).send_keys("QA Automation Lab")

        driver.find_element(
            By.ID, "address1"
        ).send_keys("42 Test Avenue")

        driver.find_element(
            By.ID, "address2"
        ).send_keys("Apartment 5")

        Select(driver.find_element(
            By.ID, "country"
        )).select_by_visible_text("United States")

        driver.find_element(
            By.ID, "state"
        ).send_keys("California")

        driver.find_element(
            By.ID, "city"
        ).send_keys("San Francisco")

        driver.find_element(
            By.ID, "zipcode"
        ).send_keys("94105")

        driver.find_element(
            By.ID, "mobile_number"
        ).send_keys("4155550142")

        driver.find_element(
            By.CSS_SELECTOR, '[data-qa="create-account"]'
        ).click()

        confirmation = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'h2[data-qa="account-created"]')
            )
        )

        self.assertEqual(
            "ACCOUNT CREATED!",
            confirmation.text.strip().upper()
        )

        # ==========================================
        # 12. RETOUR AU PANIER ET CHECKOUT
        # ==========================================

        driver.find_element(
            By.LINK_TEXT, "Continue"
        ).click()

        wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Cart")
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Proceed To Checkout")
            )
        ).click()

        wait.until(
            EC.url_to_be(f"{self.base_url}/checkout")
        )

        # Verification du total de la commande

        self.assertEqual(
            "Rs. 900",
            driver.find_element(
                By.CSS_SELECTOR,
                "#cart_info tbody tr:last-child .cart_total_price"
            ).text.strip()
        )

        # ==========================================
        # 13. ACCES AU PAIEMENT
        # ==========================================

        driver.find_element(
            By.LINK_TEXT, "Place Order"
        ).click()

        wait.until(
            EC.url_to_be(f"{self.base_url}/payment")
        )

        # ==========================================
        # 14. RENSEIGNEMENT DU PAIEMENT FICTIF
        # ==========================================

        driver.find_element(
            By.NAME, "name_on_card"
        ).send_keys("Lucas Martin")

        driver.find_element(
            By.NAME, "card_number"
        ).send_keys("4111111111111111")

        driver.find_element(
            By.NAME, "cvc"
        ).send_keys("123")

        driver.find_element(
            By.NAME, "expiry_month"
        ).send_keys("12")

        driver.find_element(
            By.NAME, "expiry_year"
        ).send_keys("2030")

        driver.find_element(By.ID, "submit").click()

        # ==========================================
        # 15. CONFIRMATION DE LA COMMANDE
        # ==========================================

        confirmation = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'h2[data-qa="order-placed"]')
            )
        )

        self.assertEqual(
            "ORDER PLACED!",
            confirmation.text.strip().upper()
        )

        self.assertEqual(
            "Congratulations! Your order has been confirmed!",
            driver.find_element(
                By.CSS_SELECTOR,
                'h2[data-qa="order-placed"] + p'
            ).text.strip()
        )

        # ==========================================
        # 16. TELECHARGEMENT DE LA FACTURE
        # ==========================================

        invoice = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "a.btn.btn-default.check_out")
            )
        )

        self.assertEqual(
            "/download_invoice/900",
            invoice.get_dom_attribute("href")
        )

        invoice.click()

        # ==========================================
        # 17. CLEANUP : SUPPRESSION DU COMPTE
        # ==========================================

        wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Continue")
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Delete Account")
            )
        ).click()

        confirmation = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 'h2[data-qa="account-deleted"]')
            )
        )

        self.assertEqual(
            "ACCOUNT DELETED!",
            confirmation.text.strip().upper()
        )

        self.assertEqual(
            "Your account has been permanently deleted!",
            driver.find_element(
                By.CSS_SELECTOR,
                'h2[data-qa="account-deleted"] + p'
            ).text.strip()
        )

        driver.find_element(
            By.LINK_TEXT, "Continue"
        ).click()

        wait.until(
            EC.url_to_be(f"{self.base_url}/")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
