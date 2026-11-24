# ============================================================
# OBJECTIF PEDAGOGIQUE : SELENIUM CLASSIQUE VS BDD
# ============================================================
#
# Ce fichier reprend volontairement la logique du scénario E2E
# présent dans test_cart_e2e.py, mais utilise Behave et Gherkin
# pour implémenter une approche BDD (Behavior Driven Development).
#
# La duplication du code Selenium est intentionnelle afin de
# conserver deux implémentations indépendantes et de comparer :
#
# - La structure et l'organisation du code.
# - La séparation du besoin métier et de la logique technique.
# - La lisibilité et la réutilisabilité des étapes.
# - L'exécution des tests et la restitution des résultats.
# - La maintenabilité des deux approches.
#
# Dans un projet de production, les actions Selenium seraient
# mutualisées, notamment à travers le Page Object Model (POM),
# afin de respecter le principe DRY (Don't Repeat Yourself).
#
# Cette duplication constitue donc un choix pédagogique
# et non une recommandation d'architecture professionnelle.
#
# ============================================================

from behave import given, when, then

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ==========================================
# CORRESPONDANCE DES PRODUITS
# ==========================================

PRODUCTS = {
    "Blue Top": 1,
    "Summer White Top": 6
}


# ==========================================
# 1. ACCES AU SITE ET CONSENTEMENT
# ==========================================

@given('I am on the Automation Exercise homepage')
def open_homepage(context):

    context.driver.get(context.base_url)

    try:
        WebDriverWait(context.driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Autoriser']")
            )
        ).click()

    except TimeoutException:
        pass


# ==========================================
# 2. AJOUT D'UN PRODUIT AU PANIER
# ==========================================

@when('I add "{product}" to my cart')
def add_product(context, product):

    product_id = PRODUCTS[product]

    context.wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             f'.productinfo a[data-product-id="{product_id}"]')
        )
    ).click()

    modal = context.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "#cartModal h4")
        )
    )

    assert modal.text.strip() == "Added!", (
        f"Product addition confirmation is incorrect: {product}"
    )

    context.driver.find_element(
        By.CSS_SELECTOR, "#cartModal button"
    ).click()

    context.wait.until(
        EC.invisibility_of_element_located(
            (By.ID, "cartModal")
        )
    )


# ==========================================
# 3. ACCES AU PANIER
# ==========================================

@when('I open my shopping cart')
@when('I return to my cart')
def open_cart(context):

    context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Cart")
        )
    ).click()

    context.wait.until(
        EC.url_to_be(f"{context.base_url}/view_cart")
    )


# ==========================================
# 4. VERIFICATION DU CONTENU DU PANIER
# ==========================================

@then('my cart should contain the following products:')
def verify_cart_products(context):

    driver = context.driver
    wait = context.wait

    actual_products = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '#cart_info tbody tr[id^="product-"]')
        )
    )

    assert len(actual_products) == len(context.table.rows), (
        f"Expected {len(context.table.rows)} products, "
        f"got {len(actual_products)}"
    )

    for row in context.table:

        product = row["product"]
        product_id = PRODUCTS[product]

        expected_quantity = row["quantity"]
        expected_price = f'Rs. {row["unit_price"]}'
        expected_subtotal = f'Rs. {row["subtotal"]}'

        wait.until(
            EC.visibility_of_element_located(
                (By.ID, f"product-{product_id}")
            )
        )

        actual_name = driver.find_element(
            By.CSS_SELECTOR,
            f"#product-{product_id} .cart_description h4 a"
        ).text.strip()

        actual_quantity = driver.find_element(
            By.CSS_SELECTOR,
            f"#product-{product_id} .cart_quantity button"
        ).text.strip()

        actual_price = driver.find_element(
            By.CSS_SELECTOR,
            f"#product-{product_id} .cart_price p"
        ).text.strip()

        actual_subtotal = driver.find_element(
            By.CSS_SELECTOR,
            f"#product-{product_id} .cart_total_price"
        ).text.strip()

        assert actual_name == product, (
            f"Expected product: {product}, got: {actual_name}"
        )

        assert actual_quantity == expected_quantity, (
            f"{product}: expected quantity {expected_quantity}, "
            f"got {actual_quantity}"
        )

        assert actual_price == expected_price, (
            f"{product}: expected price {expected_price}, "
            f"got {actual_price}"
        )

        assert actual_subtotal == expected_subtotal, (
            f"{product}: expected subtotal {expected_subtotal}, "
            f"got {actual_subtotal}"
        )


# ==========================================
# 5. CHECKOUT
# ==========================================

@when('I proceed to checkout')
def proceed_to_checkout(context):

    context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Proceed To Checkout")
        )
    ).click()

    context.wait.until(
        lambda driver:
            driver.current_url == f"{context.base_url}/checkout"
            or driver.find_element(
                By.ID, "checkoutModal"
            ).is_displayed()
    )


# ==========================================
# 6. INSCRIPTION ET CREATION DU COMPTE
# ==========================================

@when('I register a new customer account')
def register_customer(context):

    driver = context.driver
    wait = context.wait

    # Recuperation des donnees externalisees
    user = context.test_data["user"]
    address = context.test_data["address"]
    birth_date = user["birth_date"]

    full_name = f'{user["first_name"]} {user["last_name"]}'

    # Acces a la page d'inscription
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             '#checkoutModal a[href="/login"]')
        )
    ).click()

    wait.until(
        EC.url_to_be(f"{context.base_url}/login")
    )

    driver.find_element(
        By.CSS_SELECTOR, '[data-qa="signup-name"]'
    ).send_keys(full_name)

    driver.find_element(
        By.CSS_SELECTOR, '[data-qa="signup-email"]'
    ).send_keys(context.email)

    driver.find_element(
        By.CSS_SELECTOR, '[data-qa="signup-button"]'
    ).click()

    wait.until(
        EC.url_to_be(f"{context.base_url}/signup")
    )

    # Selection de la civilite
    titles = {
        "Mr": "id_gender1",
        "Mrs": "id_gender2"
    }

    wait.until(
        EC.element_to_be_clickable(
            (By.ID, titles[user["title"]])
        )
    ).click()

    # Mot de passe provenant du fichier .env
    driver.find_element(
        By.ID, "password"
    ).send_keys(context.test_password)

    # Date de naissance
    Select(driver.find_element(
        By.ID, "days"
    )).select_by_visible_text(birth_date["day"])

    Select(driver.find_element(
        By.ID, "months"
    )).select_by_visible_text(birth_date["month"])

    Select(driver.find_element(
        By.ID, "years"
    )).select_by_visible_text(birth_date["year"])

    # Preferences utilisateur
    newsletter = driver.find_element(
        By.ID, "newsletter"
    )

    if newsletter.is_selected() != user["newsletter"]:
        newsletter.click()

    partner_offers = driver.find_element(
        By.ID, "optin"
    )

    if partner_offers.is_selected() != user["partner_offers"]:
        partner_offers.click()

    # Identite
    driver.find_element(
        By.ID, "first_name"
    ).send_keys(user["first_name"])

    driver.find_element(
        By.ID, "last_name"
    ).send_keys(user["last_name"])

    # Adresse
    driver.find_element(
        By.ID, "company"
    ).send_keys(address["company"])

    driver.find_element(
        By.ID, "address1"
    ).send_keys(address["street"])

    driver.find_element(
        By.ID, "address2"
    ).send_keys(address["street_2"])

    Select(driver.find_element(
        By.ID, "country"
    )).select_by_visible_text(address["country"])

    driver.find_element(
        By.ID, "state"
    ).send_keys(address["state"])

    driver.find_element(
        By.ID, "city"
    ).send_keys(address["city"])

    driver.find_element(
        By.ID, "zipcode"
    ).send_keys(address["zipcode"])

    driver.find_element(
        By.ID, "mobile_number"
    ).send_keys(address["mobile"])

    # Validation de l'inscription
    driver.find_element(
        By.CSS_SELECTOR, '[data-qa="create-account"]'
    ).click()


# ==========================================
# 7. VERIFICATION DE LA CREATION DU COMPTE
# ==========================================

@then('my account should be successfully created')
def verify_account_creation(context):

    confirmation = context.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'h2[data-qa="account-created"]')
        )
    )

    actual_message = confirmation.text.strip().upper()

    assert actual_message == "ACCOUNT CREATED!", (
        f"Expected ACCOUNT CREATED!, got {actual_message}"
    )

    context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Continue")
        )
    ).click()


# ==========================================
# 8. VERIFICATION DU TOTAL DE LA COMMANDE
# ==========================================

@then('the order total should be {total:d} rupees')
def verify_order_total(context, total):

    context.wait.until(
        EC.url_to_be(f"{context.base_url}/checkout")
    )

    actual_total = context.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             "#cart_info tbody tr:last-child .cart_total_price")
        )
    ).text.strip()

    expected_total = f"Rs. {total}"

    assert actual_total == expected_total, (
        f"Expected total {expected_total}, got {actual_total}"
    )

    context.order_total = total


# ==========================================
# 9. PASSAGE DE LA COMMANDE
# ==========================================

@when('I place my order')
def place_order(context):

    context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Place Order")
        )
    ).click()

    context.wait.until(
        EC.url_to_be(f"{context.base_url}/payment")
    )


# ==========================================
# 10. PAIEMENT FICTIF
# ==========================================

@when('I submit valid test payment information')
def submit_payment(context):

    driver = context.driver

    # Recuperation des donnees du fichier .env
    payment = context.payment_data

    driver.find_element(
        By.NAME, "name_on_card"
    ).send_keys(payment["name"])

    driver.find_element(
        By.NAME, "card_number"
    ).send_keys(payment["card_number"])

    driver.find_element(
        By.NAME, "cvc"
    ).send_keys(payment["cvc"])

    driver.find_element(
        By.NAME, "expiry_month"
    ).send_keys(payment["expiry_month"])

    driver.find_element(
        By.NAME, "expiry_year"
    ).send_keys(payment["expiry_year"])

    driver.find_element(
        By.ID, "submit"
    ).click()


# ==========================================
# 11. CONFIRMATION DE LA COMMANDE
# ==========================================

@then('my order should be successfully confirmed')
def verify_order_confirmation(context):

    confirmation = context.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'h2[data-qa="order-placed"]')
        )
    )

    actual_title = confirmation.text.strip().upper()

    assert actual_title == "ORDER PLACED!", (
        f"Expected ORDER PLACED!, got {actual_title}"
    )

    actual_message = context.driver.find_element(
        By.CSS_SELECTOR,
        'h2[data-qa="order-placed"] + p'
    ).text.strip()

    expected_message = (
        "Congratulations! Your order has been confirmed!"
    )

    assert actual_message == expected_message, (
        f"Expected {expected_message}, got {actual_message}"
    )


# ==========================================
# 12. TELECHARGEMENT DE LA FACTURE
# ==========================================

@when('I request the invoice download')
def download_invoice(context):

    invoice = context.wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "a.btn.btn-default.check_out")
        )
    )

    context.invoice_href = invoice.get_dom_attribute("href")

    invoice.click()


# ==========================================
# 13. VERIFICATION DU LIEN DE TELECHARGEMENT
# ==========================================

@then('the invoice download link should be valid')
def verify_invoice_link(context):

    expected_href = (
        f"/download_invoice/{context.order_total}"
    )

    assert context.invoice_href == expected_href, (
        f"Expected invoice link {expected_href}, "
        f"got {context.invoice_href}"
    )


# ==========================================
# 14. SUPPRESSION DU COMPTE
# ==========================================

@when('I delete my customer account')
def delete_account(context):

    context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Continue")
        )
    ).click()

    context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Delete Account")
        )
    ).click()


# ==========================================
# 15. VERIFICATION DE LA SUPPRESSION
# ==========================================

@then('my account should be successfully deleted')
def verify_account_deletion(context):

    confirmation = context.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             'h2[data-qa="account-deleted"]')
        )
    )

    actual_title = confirmation.text.strip().upper()

    assert actual_title == "ACCOUNT DELETED!", (
        f"Expected ACCOUNT DELETED!, got {actual_title}"
    )

    actual_message = context.driver.find_element(
        By.CSS_SELECTOR,
        'h2[data-qa="account-deleted"] + p'
    ).text.strip()

    expected_message = (
        "Your account has been permanently deleted!"
    )

    assert actual_message == expected_message, (
        f"Expected {expected_message}, got {actual_message}"
    )

    context.wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Continue")
        )
    ).click()

    context.wait.until(
        EC.url_to_be(f"{context.base_url}/")
    )
