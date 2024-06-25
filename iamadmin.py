from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import secret
import time
import os

# netID = [] #GIVE me a NETID
email = []
netID = email.split('@')[0]

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

# Locate the User Lookup input field and enter NETID
userLookUpInput = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='User Lookup']")))
# #Use this to clear the old input from the input area
# userLookUpInput.clear()
userLookUpInput.send_keys(netID)

retrieveInfoButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'mat-raised-button') and span[contains(., 'Retrieve User Info')]]")))
retrieveInfoButton.click()

# Use XPath to directly locate the department information
departmentInfo = wait.until(EC.presence_of_element_located((By.XPATH, "//app-attribute-list[@title='Faculty/Staff Attributes']//li[strong[contains(text(), 'Department:')]]")))

# Extract and print the department info text
department = departmentInfo.text.replace("Department:", "").strip()
print(f"Department Info: {department}")

driver.quit()
