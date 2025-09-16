import pandas as pd

# Read and prepare the data
df = pd.read_csv('menu.csv')

# Rename columns to match your database schema
df.rename(columns={'Cuisine': 'CuisineCountry'}, inplace=True)

# Ensure critical fields are strings and handle NaN
df['Item'] = df['Item'].fillna('').astype(str)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)  # Convert to numeric, handle bad values
df['CuisineCountry'] = df['CuisineCountry'].fillna('Unknown').astype(str)

# Remove duplicates (same item, price, cuisine)
menu_data = df[['Item', 'Price', 'CuisineCountry']].drop_duplicates()

# Generate the SQL file
with open('menu.sql', 'w') as f:
    f.write("-- SQL for menu table\n")
    f.write("-- Generated from menu.csv\n")
    f.write("INSERT INTO menu (Item, Price, CuisineCountry) VALUES\n")
    
    rows = []
    for _, row in menu_data.iterrows():
        item = row['Item'].replace("'", "''")  # Escape single quotes
        price = row['Price']
        cuisine = row['CuisineCountry'].replace("'", "''")
        rows.append(f"    ('{item}', {price}, '{cuisine}')")
    
    f.write(",\n".join(rows))
    f.write(";\n")
    f.write("\n-- End of menu.sql\n")

print(f"✅ Generated menu.sql with {len(menu_data)} unique menu items")