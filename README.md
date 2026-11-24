
# QA BDD Automation

## Project overview

This project demonstrates an end-to-end QA automation workflow using Python, Selenium, Behave, Gherkin and GitHub Actions.

The objective is to automate and validate a complete e-commerce customer journey on [Automation Exercise](https://automationexercise.com/).

The project was developed as part of a QA Software Tester training program.

## Technologies and tools

| Tool | Purpose |
|---|---|
| Python | Test automation language |
| Selenium WebDriver | Browser automation |
| Katalon Recorder | Initial scenario recording |
| Gherkin | Business-readable test scenarios |
| Behave | BDD test execution |
| JSON | Externalized test data |
| Python-dotenv | Environment configuration |
| PowerShell | Local execution and reporting |
| Git | Version control |
| GitHub | Repository and Pull Requests |
| GitHub Actions | Continuous integration |

## Test scenario - US01

Complete an online purchase as a new customer.

The automated scenario covers:

- Website navigation
- Adding two products to the shopping cart
- Product name validation
- Quantity validation
- Unit price validation
- Subtotal validation
- Customer account registration
- Checkout
- Order total validation
- Payment using fictitious data
- Order confirmation
- Invoice download request and link validation
- Customer account deletion

## Test results

| Metric | Validated local execution |
|---|---:|
| Features | 1 passed |
| Scenarios | 1 passed |
| Steps | 18 passed |
| Failed steps | 0 |
| Skipped steps | 0 |
| Success rate | 100% |

## Project structure

```text
qa-bdd-automation/
|
|-- .github/
|   `-- workflows/
|       `-- bdd-tests.yml
|
|-- features/
|   |-- steps/
|   |   `-- cart_steps.py
|   |-- cart.feature
|   `-- environment.py
|
|-- reports/
|-- .env.example
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- run_bdd.ps1
|-- test_cart_e2e.py
`-- test_data.json
```

## Automation implementations

Two implementations of the same business scenario are available for comparison.

### Classic Selenium automation

Python and Selenium using the unittest framework.

[View Selenium implementation](test_cart_e2e.py)

### BDD automation

Business-readable Gherkin scenarios connected to reusable Python step definitions.

- [Gherkin scenario](features/cart.feature)
- [Step definitions](features/steps/cart_steps.py)
- [Behave lifecycle hooks](features/environment.py)

## Installation

Clone the repository:

```bash
git clone https://github.com/alexis-durouchet/qa-bdd-automation.git
cd qa-bdd-automation
```

Create a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a local `.env` file using `.env.example` as a template and configure fictitious test credentials and payment information.

Google Chrome is required for local browser execution.

## Test execution

### Classic Selenium

```bash
python test_cart_e2e.py
```

### Behave BDD

```bash
python -m behave
```

### BDD with timestamped reporting

```powershell
.\run_bdd.ps1
```

## Test reports

Reports contain individual step results, execution times and overall test statistics.

### Local execution

- [Initial local report](reports/bdd_report.txt)
- [Timestamped local report](reports/bdd_report_2026-11-24_12-04-41.txt)

### Automated CI execution

- [CI campaign 1](reports/ci_bdd_report_2026-11-24_11-26-38.txt)
- [CI campaign 2](reports/ci_bdd_report_2026-11-24_11-31-19.txt)
- [CI campaign 3](reports/ci_bdd_report_2026-11-24_11-32-37.txt)

[View all test reports](reports/)

## Continuous integration

GitHub Actions provides automated remote execution of the BDD scenario.

The pipeline handles:

- Repository checkout
- Python environment configuration
- Dependency installation
- Headless Chrome execution
- Automated BDD testing
- Timestamped report generation
- Automatic report publication

[View CI workflow](.github/workflows/bdd-tests.yml)

[View GitHub Actions execution history](https://github.com/alexis-durouchet/qa-bdd-automation/actions)

## Git workflow

The project follows a feature-branch development approach:

- features/selenium-e2e
- features/bdd-behave
- features/test-reporting
- features/github-actions

Each development stage is integrated through a Pull Request.

[View Pull Request history](https://github.com/alexis-durouchet/qa-bdd-automation/pulls?q=is%3Apr)

## Skills demonstrated

- Functional test automation
- End-to-end testing
- Test scenario design
- Behavior-Driven Development
- Selenium locators and explicit waits
- Assertions and expected result validation
- Reusable step definitions
- Test data management
- Environment configuration
- Automated test reporting
- Git branching and Pull Requests
- Continuous integration

## Project scope

This is an educational QA automation project.

All customer and payment information used during testing is fictitious.

The project demonstrates continuous integration rather than application deployment.
