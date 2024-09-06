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
driver.get("https://adminconsole.adobe.com/86CFEC7158E2843F0A495E82@AdobeOrg/products/9D1AE726AB5FC8B1539A/profiles")
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

#We are inside All Apps and we want to extract all the profile links here so we can use them for later

# Open a CSV file to write the links
with open('profileLinks.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    # Getting inside the table of list of profiles
    # We have 5 pages of profiles in Adobe
    for i in range(5): #CHANGE PAGE NUMBER HERE
        numRows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))

        for row in numRows:
            try:
                link_element = row.find_element(By.CLASS_NAME, "WBgRPa_spectrum-Link")
                link = link_element.get_attribute("href")
                writer.writerow([link + ","])
            except Exception as e:
                print(f"Error occurred while processing a row: {e}")

        # Do not go to the next page when we reach the 5th page
        if(i < 5):
            # To click on the next page button and then do the row part again
            time.sleep(5)

            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-btn']")))
            next_button.click()

            time.sleep(5)

print("Closing Chrome")

driver.quit()
