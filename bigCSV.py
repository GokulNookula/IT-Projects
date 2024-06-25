import os
import csv

# Paths to the input directory and the combined output CSV file
input_dir = "Completed Files"  # Directory containing the input CSV files
output_file = "AllAppsCombined.csv"  # Combined output CSV file

# Define the new columns to be added if not present
new_columns = ['User Groups']

# Initialize a set to track unique headers
header_set = set()

# Open the combined output CSV file for writing
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Iterate over all CSV files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_dir, filename)
            
            with open(input_file, 'r', newline='') as infile:
                reader = csv.reader(infile)

                # Read the header row
                header = next(reader)
                original_header = header.copy()

                # Check if 'User Groups' column already exists
                if 'User Groups' not in header:
                    # Insert the 'User Groups' column after 'Product Profile'
                    product_profile_index = header.index('Product Profile')
                    header.insert(product_profile_index + 1, 'User Groups')

                # If this is the first file, write the header to the output file
                if not header_set:
                    writer.writerow(header)
                    header_set = set(header)
                
                # Ensure all headers are the same
                if header_set != set(header):
                    raise ValueError(f"Headers do not match: {header} vs {header_set}")

                for row in reader:
                    # Insert the user groups value if the column was added
                    if 'User Groups' not in original_header:
                        row.insert(product_profile_index + 1, '')

                    # Write the updated row to the output file
                    writer.writerow(row)

print("Completed")
