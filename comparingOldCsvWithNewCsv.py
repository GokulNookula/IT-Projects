import csv

#This file is to compare old csv file which had manual input of some user information
# transferring that to the new file
# Paths to the input and output files
adobe_pro_dc_file = ".csv" #New File with more users but no Manual Input Information
merged_output_file = '.csv' #Old File with Manual Input
output_file = '.csv' #Generate a new file with manual input of combining information

# Read the Adobe Pro DC user list into a dictionary
adobe_pro_dc_data = {}
with open(adobe_pro_dc_file, 'r', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row['Email']
        adobe_pro_dc_data[email] = row

# Read the merged output and update department names
updated_rows = []
with open(merged_output_file, 'r', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        email = row['Email']
        if email in adobe_pro_dc_data:
            adobe_pro_dc_row = adobe_pro_dc_data[email]
            # Compare and update department names
            if row['Department Per IAM'] != adobe_pro_dc_row['Department Per IAM']:
                row['Department Per IAM'] = adobe_pro_dc_row['Department Per IAM']
        updated_rows.append(row)

# Write the updated rows to the new output file
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f'Updated file has been written to {output_file}')
