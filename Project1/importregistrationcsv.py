import pandas as pd

# Read and prepare the data
df = pd.read_csv('registration.csv')

# Rename columns to match your database schema
df.rename(columns={'Date': 'CallDate', 'Time': 'CallTime'}, inplace=True)

# Ensure correct data types and handle missing values
df['CallDate'] = pd.to_datetime(df['CallDate'], errors='coerce').dt.date  # Convert to date
df['CallTime'] = pd.to_datetime(df['CallTime'], errors='coerce').dt.time  # Convert to time

# Replace NaN with None (which will become NULL in SQL)
df['Phone'] = df['Phone'].fillna('').astype(str)
df['Firstname'] = df['Firstname'].fillna('').astype(str)
df['Lastname'] = df['Lastname'].fillna('').astype(str)

# Handle empty or invalid dates/times
df['CallDate'] = df['CallDate'].fillna(pd.Timestamp('1970-01-01').date()).astype(str)
df['CallTime'] = df['CallTime'].fillna('00:00:00').astype(str)

# Remove duplicates
registration_data = df[['CallDate', 'CallTime', 'Phone', 'Firstname', 'Lastname']].drop_duplicates()

# Generate the SQL file
with open('registration.sql', 'w') as f:
    f.write("-- SQL for registration table\n")
    f.write("-- Generated from registration.csv\n")
    f.write("INSERT INTO registration (CallDate, CallTime, Phone, Firstname, Lastname) VALUES\n")
    
    rows = []
    for _, row in registration_data.iterrows():
        call_date = row['CallDate']
        call_time = row['CallTime']
        phone = str(row['Phone']).replace("'", "''")
        firstname = str(row['Firstname']).replace("'", "''")
        lastname = str(row['Lastname']).replace("'", "''")
        rows.append(f"    ('{call_date}', '{call_time}', '{phone}', '{firstname}', '{lastname}')")
    
    f.write(",\n".join(rows))
    f.write(";\n")
    f.write("\n-- End of registration.sql\n")

print(f"✅ Generated registration.sql with {len(registration_data)} unique registrations")