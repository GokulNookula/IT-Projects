from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import secret
import time
import os
import shutil

# Function to rename and move the downloaded file
def rename_and_move_downloaded_file(downloadDir, originalFilename, newFilename, destinationDir):
    # Ensure the new filename is valid
    newFilename = "".join([c for c in newFilename if c.isalpha() or c.isdigit() or c in (' ', '.', '_')]).rstrip()
    oldFile = os.path.join(downloadDir, originalFilename)
    newFile = os.path.join(destinationDir, newFilename + ".csv")
    
    if os.path.exists(oldFile):
        shutil.move(oldFile, newFile)
        print(f"Moved and renamed '{oldFile}' to '{newFile}'")
    else:
        print(f"File '{oldFile}' does not exist.")

drivers = [] #Add Links here for your program

for drive in drivers:
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the login page
    driver.get(drive)
    driver.maximize_window()

    # Use WebDriverWait to wait until the email field is present
    wait = WebDriverWait(driver, 5)

    # Locate the email field and enter your email for Adobe Login
    emailField = wait.until(EC.presence_of_element_located((By.ID, "EmailPage-EmailField")))
    emailField.send_keys(secret.email)

    # Wait for the 'Continue' button to be clickable and then click it in Adobe Login
    continueButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".spectrum-Button.spectrum-Button--cta.SpinnerButton.SpinnerButton--right")))
    continueButton.click()

    # Wait for the username field to be present and enter the username for UCR Login
    usernameInput = wait.until(EC.presence_of_element_located((By.ID, "username")))
    usernameInput.send_keys(secret.username)

    # Locate and fill in the password field for UCR Login
    passwordInput = driver.find_element(By.ID, "password")
    passwordInput.send_keys(secret.password)

    # Locate and click the 'Sign In' button for UCR Login
    signInButton = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div/div/form/div[2]/button")
    signInButton.click()

    # Allow some time for login to complete the DUO 2FA part
    time.sleep(17)
    
    # Extract the name of the Product Profile we are in for All Apps
    productProfName = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='page-header-title']")))
    fileproductProfName = productProfName.text

    # To download the CSV file
    # Click the "More actions" button
    moreActionsButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='user-operations-menu']")))
    moreActionsButton.click()

    # Wait for the dropdown menu to appear and then click "Export users list to CSV"
    exportCsvOption = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Export users list to CSV']")))
    exportCsvOption.click()

    # # For example, to print the number of rows in the table -- For Testing
    # rows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))
    # print(f"Number of rows: {len(rows)}")

    time.sleep(3)

    # Rename and move the downloaded file
    downloadDir = ""
    originalFilename = "users.csv"
    destinationDir = ""
    rename_and_move_downloaded_file(downloadDir, originalFilename, fileproductProfName, destinationDir)
