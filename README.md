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
