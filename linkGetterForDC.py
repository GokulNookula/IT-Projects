from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import secret
import time
import csv

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the login page
driver.get("https://adminconsole.adobe.com/86CFEC7158E2843F0A495E82@AdobeOrg/products/36D1E2042F24BE018D3A/profiles")
driver.maximize_window()

# Use WebDriverWait to wait until the email field is present
wait = WebDriverWait(driver, 5)

# Locate the email field and enter your email/username
emailField = wait.until(EC.presence_of_element_located((By.ID, "EmailPage-EmailField")))
emailField.send_keys(secret.email)

# Wait for the 'Continue' button to be clickable and then click it
continueButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".spectrum-Button.spectrum-Button--cta.SpinnerButton.SpinnerButton--right")))
continueButton.click()

# Wait for the username field to be present and enter the username
usernameInput = wait.until(EC.presence_of_element_located((By.ID, "username")))
usernameInput.send_keys(secret.username)

# Locate and fill in the password field
passwordInput = driver.find_element(By.ID, "password")
passwordInput.send_keys(secret.password)

# Locate and click the 'Sign In' button
signInButton = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div/div/form/div[2]/button")
signInButton.click()

# Allow some time for login to complete the DUO 2FA part
time.sleep(15)

#We are inside Adobe Pro DC and we want to extract all the profile links here so we can use them for later

# Function to process each row and handle stale element exception
def process_row(row):
    try:
        link_element = row.find_element(By.CLASS_NAME, "WBgRPa_spectrum-Link")
        link_element.click()
        time.sleep(2)  # Allow some time for the page to load
        # Do your actions here on the profile page
        # Navigate back to the previous page
        driver.back()
        time.sleep(2)  # Allow some time to go back to the previous page
    except Exception as e:
        print(f"Error: {e}")

# Get the total number of rows in the table
table = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))
total_rows = len(table)

# Loop through the rows by index to handle stale element reference
for i in range(total_rows):
    # Refresh the table elements to avoid stale element reference
    table = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))
    process_row(table[i])


# table = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))

# for row in table:
#     link_element = row.find_element(By.CLASS_NAME, "WBgRPa_spectrum-Link")
#     link_element.click()
#     time.sleep(5)  # Allow some time for the page to load
#     # Do your actions here on the profile page
#     # Navigate back to the previous page
#     driver.back()
#     time.sleep(5)  # Allow some time to go back to the previous page

# Keep the browser open
input("Press Enter to close the browser...")

driver.quit()