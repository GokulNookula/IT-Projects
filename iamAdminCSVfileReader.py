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

#Choose which Adobe Software you are working on

adobe = 'All Apps' ## or "Adobe Pro DC"

# Paths to the input and output directories
input_dir = "Input Folder"
output_file = "completeAllApps.csv"

# Function to process a CSV file
def process_csv(input_file, writer, wait, product_profile, user_group):
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)

        # Read the header row
        header = next(reader)

        for row in reader:
            # Extract the NETID from the email
            email = row[3]
            netID = email.split('@')[0]

            if email.endswith('@engr.ucr.edu'):
                department = "Not Available"
            else:
                # Locate the User Lookup input field and enter NETID
                userLookUpInput = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='User Lookup']")))
                userLookUpInput.clear()
                userLookUpInput.send_keys(netID)

                retrieveInfoButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'mat-raised-button') and span[contains(., 'Retrieve User Info')]]")))
                retrieveInfoButton.click()

                try:
                    # Use XPath to directly locate the department information
                    departmentInfo = wait.until(EC.presence_of_element_located((By.XPATH, "//app-attribute-list[@title='Faculty/Staff Attributes']//li[strong[contains(text(), 'Department:')]]")))

                    # Extract and print the department info text
                    department = departmentInfo.text.replace("Department:", "").strip()
                except:
                    department = "Not Available"

            # Define the new values to be added to each row
            new_values = [product_profile, user_group, adobe, department]

            # Create the updated row based on the input file type
            if len(row) > 6:
                # Input file type 1
                updated_row = row[:2] + row[3:6] + new_values
            else:
                # Input file type 2
                updated_row = row[:5] + new_values

            # Write the updated row to the output file
            writer.writerow(updated_row)

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

# We are inside IAMAdmin Portal Now
clickBearHelpTool = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/app/home/bearHelpToolbox']")))
clickBearHelpTool.click()

# Locate the User Lookup input field outside the loop to clear it for each new file
userLookUpInput = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='User Lookup']")))

# Open the output file for writing
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    # Write the header row to the output file
    header = ['Identity Type', 'Username', 'Email', 'First Name', 'Last Name', 'Product Profile', 'User Groups', 'Product Entitlement', 'Department Per IAM']
    writer.writerow(header)

    # Iterate over all CSV files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            input_file_path = os.path.join(input_dir, filename)

            # Clear the input field before processing a new CSV file
            userLookUpInput.clear()

            # Get the product profile and user group from the filename (excluding the .csv extension)
            parts = filename[:-4].split('$')
            product_profile = parts[0]
            user_group = parts[1] if len(parts) > 1 else ''

            # Process the current CSV file
            process_csv(input_file_path, writer, wait, product_profile, user_group)

driver.quit()
