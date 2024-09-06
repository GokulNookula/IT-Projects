from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import secret
import time
import csv
import os
import shutil

#Total number of pages in Adobe Pro DC
totalPages = 7

# Function to rename and move the downloaded file
def rename_and_move_downloaded_file(downloadDir, originalFilename, newFilename, destinationDir):
    # Ensure the new filename is valid
    newFilename = "".join([c for c in newFilename if c.isalpha() or c.isdigit() or c in (' ', '.', '_', '$')]).rstrip()
    oldFile = os.path.join(downloadDir, originalFilename)
    newFile = os.path.join(destinationDir, newFilename + ".csv")
    
    if os.path.exists(oldFile):
        shutil.move(oldFile, newFile)
        print(f"Moved and renamed '{oldFile}' to '{newFile}'")
    else:
        print(f"File '{oldFile}' does not exist for {newFilename}")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the login page
driver.get("https://adminconsole.adobe.com/86CFEC7158E2843F0A495E82@AdobeOrg/products/36D1E2042F24BE018D3A/profiles")
driver.maximize_window()

# Use WebDriverWait to wait until the email field is present
wait = WebDriverWait(driver, 10)

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
        productProfileLinks = row.find_element(By.CLASS_NAME, "WBgRPa_spectrum-Link")
        productProfileLinks.click()
        time.sleep(1.5)  # Allow some time for the page to load

        #Add the files that need to be downloaded manually to the exception so your program can still run
        #Examples of files that are not in correct format
        excludedProfiles = {
            "BCOE - Tom Gregory",
            "CHASS - Dean's Office - James Lin"
        }

        # Process user groups
        try:
            # Extract the name of the Product Profile we are in for Adobe Pro DC
            productProfName = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='page-header-title']")))
            fileproductProfName = productProfName.text.strip()
            
            if fileproductProfName not in excludedProfiles:
                tableUserGroup = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))
                userGroupTotalRows = len(tableUserGroup)

                for j in range(userGroupTotalRows):
                    tableUserGroup = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))
                    userGroupLink = tableUserGroup[j].find_element(By.CLASS_NAME, "WBgRPa_spectrum-Link")
                    userGroupLink.click()
                    time.sleep(1.5)  # Allow some time for the user group page to load
                    userGroupProfName = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='page-header-title']")))
                    fileuserGroupProfName = userGroupProfName.text.strip()

                    # To Download User Group CSV Files
                    # Click the "More actions" button
                    moreActionsButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='user-operations-menu']")))
                    moreActionsButton.click()

                    # Wait for the dropdown menu to appear and then click "Export users list to CSV"
                    exportCsvOption = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Export users list to CSV']")))
                    exportCsvOption.click()
                    
                    # Rename and move the downloaded file
                    time.sleep(9)
                    downloadDir = r"Add the PATH of your download folder here" #Ex C:\Users\user\Downloads
                    originalFilename = "user-groups.csv"
                    destinationDir = r"Add the PATH for your desired location where you want the file to be" #Ex C:\Users\user\Desktop\Code\Input Folder
                    newFilename = f"{fileproductProfName}${fileuserGroupProfName}"
                    rename_and_move_downloaded_file(downloadDir, originalFilename, newFilename, destinationDir)

                    # Do actions here for user group
                    time.sleep(2)
                    driver.back()
                    time.sleep(1.5)
        except Exception as e:
            print(f"User Group Table Error: {e}")

        # Navigate back to the previous page
        driver.back()
        time.sleep(1.3)  # Allow some time to go back to the previous page
    except Exception as e:
        print(f"Profile Link Error: {e}")

# Function to navigate to a specific page
def navigate_to_page(target_page):
    current_page = 1
    while current_page < target_page:
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-btn']")))
            next_button.click()
            time.sleep(3)  # Allow time for the next page to load
            current_page += 1
        except Exception as e:
            print(f"Error navigating to page {target_page}: {e}")
            break

# Function to process all rows on the current page
def process_current_page(page):
    try:
        table = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))
        total_rows = len(table)
        
        # Loop through the rows by index to handle stale element reference
        for i in range(total_rows):
            # Refresh the table elements to avoid stale element reference
            table = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_5uzlQq_spectrum-Table-row")))
            process_row(table[i])
            if page >= 2:
                for k in range(1,page):
                    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-btn']")))
                    next_button.click()
                    time.sleep(3)  # Allow time for the next page to load
    except Exception as e:
        print(f"Error processing current page: {e}")

# Process all pages
def process_all_pages(start_page):
    navigate_to_page(start_page)
    page = start_page
    while True:
        print(f"Processing page {page}")
        process_current_page(page)
        
        # Check if there is a next page button and click it
        if page <= totalPages:
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='next-btn']")))
                next_button.click()
                time.sleep(3)  # Allow time for the next page to load
                page += 1
            except Exception:
                print("No more pages.")
                break
        else:
            break

# Start processing is to tell the program to which page to start from incase your program crashes in the middle due to servers
#Count starts from 1,2,3 and not 0,1,2..
process_all_pages(start_page=1)

# Keep the browser open
input("Press Enter to close the browser...")

driver.quit()
