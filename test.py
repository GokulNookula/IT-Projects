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

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the login page
driver.get("https://iamadmin.ucr.edu/app/home/bearHelpToolbox")
driver.maximize_window()

# Use WebDriverWait to wait until the email field is present
wait = WebDriverWait(driver, 5)

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
time.sleep(10)

#We are inside IAMAdmin Portal Now

clickBearHelpTool = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/app/home/bearHelpToolbox']")))
clickBearHelpTool.click()

# Open the input and output CSV files
input_file = "test.csv"
output_file = "output.csv"

# Define the new columns to be added
new_columns = ['Product Entitlement', 'Department Per IAM']

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read the header row
    header = next(reader)

    # Add the new columns to the header
    header.extend(new_columns)

    # Write the updated header to the output file
    writer.writerow(header)

    firstLoop = True

    for row in reader:
        # Extract the NETID from the email
        email = row[3]
        netID = email.split('@')[0]

        if email.endswith('@engr.ucr.edu'):
            department = "NA"
        
        else:
            # Locate the User Lookup input field and enter NETID
            userLookUpInput = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='User Lookup']")))
            if(firstLoop == False):
                userLookUpInput.clear()
            userLookUpInput.send_keys(netID)

            retrieveInfoButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'mat-raised-button') and span[contains(., 'Retrieve User Info')]]")))
            retrieveInfoButton.click()

            # Use XPath to directly locate the department information
            departmentInfo = wait.until(EC.presence_of_element_located((By.XPATH, "//app-attribute-list[@title='Faculty/Staff Attributes']//li[strong[contains(text(), 'Department:')]]")))

            # Extract and print the department info text
            department = departmentInfo.text.replace("Department:", "").strip()

        # Define the new values to be added to each row
        new_values = ['All Apps', department]

        # Remove the 'Domain' value from the row
        row.pop(2)

        # Add the new values to each row
        row.extend(new_values)

        # Write the updated row to the output file
        writer.writerow(row)

        # Set the flag to False after the first iteration
        firstLoop = False


driver.quit()
