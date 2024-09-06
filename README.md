# IT-Projects

# Adobe Pro DC & Creative Cloud User Management

This project is designed to help automate the user management process in the Adobe Admin Console and integrate the information into IAM Admin for effective departmental organization. The project consists of two main components: **Adobe Pro DC** and **Adobe Creative Cloud**. The goal is to generate user reports, organize them by department, and help facilitate user additions and removals for administrators.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Pre-requisites](#pre-requisites)
3. [How It Works](#how-it-works)
   - [Adobe Pro DC](#adobe-pro-dc)
   - [Adobe Creative Cloud](#adobe-creative-cloud)
4. [Usage](#usage)
   - [Step-by-step Guide](#step-by-step-guide)
   - [Running the Scripts](#running-the-scripts)
5. [Configuration](#configuration)
6. [Notes](#notes)

## Project Structure

```bash
.
├── linkGetterForDC.py               # Adobe Pro DC automation script to gather user profiles
├── linkGetterForAllApps.py          # Link gathering script for Adobe Creative Cloud profiles
├── profileDownloadForAllApps.py     # Downloads all user profiles for Adobe Creative Cloud
├── iamAdminCSVfileReader.py         # Reads and matches user departments using IAM Admin data
├── comparingOldCsvWithNewCsv.py     # Compares older CSVs with new data for updates
├── secret.py                        # Contains authentication info (not included for security)
├── Output Test Folder/              # Output folder for generated user lists
└── README.md                        # This documentation file
```

## Pre-requisites

Before running the scripts, ensure the following are installed and configured on your system:

### Python 3.x
Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).

### Selenium
Used for browser automation. Install it using:
```bash
pip install selenium
```
### WebDriver
You will need Chrome WebDriver to work with Selenium. Make sure ChromeDriver is in your system's PATH or downloaded locally.

```bash
pip install webdriver-manager
```
### Other Required Libraries
Install other required libraries such as `pandas`:

```bash
pip install pandas
```
## How It Works

### Adobe Pro DC

The script `linkGetterForDC.py` performs the following tasks:

1. **Log in to the Adobe Admin Console** using credentials from `secret.py`.
2. **Gather user profiles**: It navigates through the Adobe Pro DC user profiles and downloads the list of users.
3. **Generate CSVs**: The gathered user lists are saved into CSV files.
4. **Department Matching**: The script uses `iamAdminCSVfileReader.py` to match the gathered users with their respective departments using IAM Admin.
5. Once the process is complete, the list is sent to your boss for further processing.

### Adobe Creative Cloud

The process for Adobe Creative Cloud is similar but with the following additional steps:

1. **Link Gathering**: The script `linkGetterForAllApps.py` collects the profile links for all the user profiles in Adobe Creative Cloud.
2. **Download Profiles**: The script `profileDownloadForAllApps.py` automates the downloading of all user profiles.
3. **Department Matching**: As with Adobe Pro DC, the script `iamAdminCSVfileReader.py` is used to match and organize the user lists by department.
4. Once the information is processed, it is sent to the appropriate departments for user removal and addition.

## Usage

### Step-by-step Guide

#### Prepare Secret File:
Modify the `secret.py` file to include your Adobe Admin Console login credentials. Make sure this file contains:

```python
email = "your-email"
username = "your-username"
password = "your-password"
```
### Run Adobe Pro DC Automation:
Run the `linkGetterForDC.py` script to gather user profiles from Adobe Admin Console:

```bash
python linkGetterForDC.py
```
### Run Adobe Creative Cloud Automation:
First, gather the profile links by running `linkGetterForAllApps.py`:

```bash
python linkGetterForAllApps.py
```
Next, download the user profiles using `profileDownloadForAllApps.py`:

```bash
python profileDownloadForAllApps.py
```
### Process and Organize Data:
Use `iamAdminCSVfileReader.py` to match and organize the user list by department:

```bash
python iamAdminCSVfileReader.py
```
### Compare CSV Files:
Run `comparingOldCsvWithNewCsv.py` to compare older CSV files with newly generated data for updates:

```bash
python comparingOldCsvWithNewCsv.py
```








