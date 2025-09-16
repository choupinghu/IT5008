import pandas as pd

# Read and prepare the data
df = pd.read_csv('staff.csv')

# Rename columns to match schema
df.rename(columns={'Staff': 'StaffID', 'Cuisine': 'CuisineCountry'}, inplace=True)

# Ensure no NaN in critical fields (optional cleanup)
df['Name'] = df['Name'].fillna('')
df['StaffID'] = df['StaffID'].fillna('UNKNOWN')
df['CuisineCountry'] = df['CuisineCountry'].fillna('Unknown')

# -------------------------------
# 1. staff table (StaffID, Name)
# -------------------------------
staff_data = df[['StaffID', 'Name']].drop_duplicates()

# Generate INSERT statements
with open('staff.sql', 'w') as f:
    f.write("-- SQL for staff table\n")
    f.write("INSERT INTO staff (StaffID, Name) VALUES\n")
    rows = []
    for _, row in staff_data.iterrows():
        staff_id = str(row['StaffID']).replace("'", "''")
        name = str(row['Name']).replace("'", "''")
        rows.append(f"    ('{staff_id}', '{name}')")
    f.write(",\n".join(rows))
    f.write(";\n")
    f.write("\n-- End of staff.sql\n")

print(f"✅ Generated staff.sql with {len(staff_data)} unique staff members")

# -------------------------------
# 2. cuisine table (CuisineCountry)
# -------------------------------
unique_cuisines = df[['CuisineCountry']].drop_duplicates()

with open('cuisine.sql', 'w') as f:
    f.write("-- SQL for cuisine table\n")
    f.write("INSERT INTO cuisine (CuisineCountry) VALUES\n")
    rows = []
    for _, row in unique_cuisines.iterrows():
        cuisine = str(row['CuisineCountry']).replace("'", "''")
        rows.append(f"    ('{cuisine}')")
    f.write(",\n".join(rows))
    f.write(";\n")
    f.write("\n-- End of cuisine.sql\n")

print(f"✅ Generated cuisine.sql with {len(unique_cuisines)} unique cuisines")

# -------------------------------
# 3. staff_cuisine table (StaffID, CuisineCountry)
# -------------------------------
staff_cuisine_data = df[['StaffID', 'CuisineCountry']].drop_duplicates()

with open('staff_cuisine.sql', 'w') as f:
    f.write("-- SQL for staff_cuisine table\n")
    f.write("INSERT INTO staff_cuisine (StaffID, CuisineCountry) VALUES\n")
    rows = []
    for _, row in staff_cuisine_data.iterrows():
        staff_id = str(row['StaffID']).replace("'", "''")
        cuisine = str(row['CuisineCountry']).replace("'", "''")
        rows.append(f"    ('{staff_id}', '{cuisine}')")
    f.write(",\n".join(rows))
    f.write(";\n")
    f.write("\n-- End of staff_cuisine.sql\n")

print(f"✅ Generated staff_cuisine.sql with {len(staff_cuisine_data)} mappings")
print("🎉 All SQL files generated successfully!")