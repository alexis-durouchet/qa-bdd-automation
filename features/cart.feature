@US01 @e2e
Feature: Shopping cart and checkout

  As a customer
  I want to purchase products online
  So that I can complete an order

  Scenario: Complete a purchase as a new customer

    Given I am on the Automation Exercise homepage

    When I add "Blue Top" to my cart
    And I add "Summer White Top" to my cart
    And I open my shopping cart

    Then my cart should contain the following products:
      | product          | quantity | unit_price | subtotal |
      | Blue Top         | 1        | 500        | 500      |
      | Summer White Top | 1        | 400        | 400      |

    When I proceed to checkout
    And I register a new customer account

    Then my account should be successfully created

    When I return to my cart
    And I proceed to checkout

    Then the order total should be 900 rupees

    When I place my order
    And I submit valid test payment information

    Then my order should be successfully confirmed

    When I request the invoice download

    Then the invoice download link should be valid

    When I delete my customer account

    Then my account should be successfully deleted