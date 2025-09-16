import pandas as pd
import numpy as np

# Read and prepare the data
df = pd.read_csv('order.csv')

# Rename columns to match schema
df.rename(columns={
    'Date': 'OrderDate',
    'Time': 'OrderTime',
    'Order': 'OrderID',
    'Card': 'CardNo',
    'Staff': 'StaffID'
}, inplace=True)

# Ensure correct data types
df['OrderID'] = df['OrderID'].astype(str)
df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce').dt.date
df['OrderTime'] = pd.to_datetime(df['OrderTime'], errors='coerce').dt.time
df['StaffID'] = df['StaffID'].astype(str)
df['Item'] = df['Item'].fillna('Unknown').astype(str)
df['Payment'] = df['Payment'].fillna('cash').astype(str)
df['CardType'] = df['CardType'].fillna('unknown').astype(str)
df['TotalPrice'] = pd.to_numeric(df['TotalPrice'], errors='coerce')

# Clean Phone numbers
def clean_phone(x):
    if pd.isna(x) or str(x).strip() in ['', 'nan', 'NaN']:
        return None
    try:
        return str(int(float(x)))
    except:
        return None

df['Phone'] = df['Phone'].apply(clean_phone)

# Fill missing Firstname/Lastname
df['Firstname'] = df['Firstname'].fillna('').astype(str)
df['Lastname'] = df['Lastname'].fillna('').astype(str)

# -------------------------------
# 1. orderinfo table
# -------------------------------
orderinfo_cols = [
    'OrderID', 'OrderDate', 'OrderTime', 'Payment',
    'CardNo', 'CardType', 'TotalPrice',
    'Phone', 'Firstname', 'Lastname'
]
orderinfo_data = df[orderinfo_cols].drop_duplicates(subset='OrderID')

# Convert NaN/None to NULL, escape quotes
def format_value(val):
    if pd.isna(val) or val is None:
        return 'NULL'
    elif isinstance(val, str):
        escaped = val.replace("'", "''")  # Escape single quotes for SQL
        return f"'{escaped}'"
    elif isinstance(val, (int, float)):
        return str(val)
    else:
        return f"'{str(val)}'"

with open('orderinfo.sql', 'w') as f:
    f.write("-- SQL for orderinfo table\n")
    f.write("-- Generated from order.csv\n")
    f.write("INSERT INTO orderinfo (\n")
    f.write("    OrderID, OrderDate, OrderTime, Payment,\n")
    f.write("    CardNo, CardType, TotalPrice,\n")
    f.write("    Phone, Firstname, Lastname\n")
    f.write(") VALUES\n")

    rows = []
    for _, row in orderinfo_data.iterrows():
        values = [format_value(row[col]) for col in orderinfo_cols]
        rows.append(f"    ({', '.join(values)})")
    
    f.write(",\n".join(rows))
    f.write(";\n")
    f.write("\n-- End of orderinfo.sql\n")

print(f"✅ Generated orderinfo.sql with {len(orderinfo_data)} unique orders")

# -------------------------------
# 2. orderitems table (with Quantity)
# -------------------------------
orderitems_grouped = df.groupby(['OrderID', 'Item', 'StaffID'], as_index=False).size().rename(columns={'size': 'Quantity'})
orderitems_grouped = orderitems_grouped.sort_values(['OrderID', 'Item', 'StaffID'])

with open('orderitems.sql', 'w') as f:
    f.write("-- SQL for orderitems table\n")
    f.write("-- Generated from order.csv (grouped by OrderID, Item, StaffID)\n")
    f.write("INSERT INTO orderitems (OrderID, Item, StaffID, Quantity) VALUES\n")

    rows = []
    for _, row in orderitems_grouped.iterrows():
        order_id = f"'{row['OrderID']}'"
        item = f"'{row['Item'].replace("'", "''")}'"      # Fixed: use ' instead of \"
        staff_id = f"'{row['StaffID']}'"
        quantity = str(row['Quantity'])
        rows.append(f"    ({order_id}, {item}, {staff_id}, {quantity})")
    
    f.write(",\n".join(rows))
    f.write(";\n")
    f.write("\n-- End of orderitems.sql\n")

# -------------------------------
# 📊 DATA QUALITY REPORT
# -------------------------------

print("\n" + "="*50)
print("📊 DATA QUALITY REPORT")
print("="*50)
print(f"📄 Original CSV rows: {len(df)}")

# Check for missing OrderID (can't insert without it)
invalid_orders = df[df['OrderID'].isna() | (df['OrderID'] == '')]
if len(invalid_orders) > 0:
    print(f"❌ Rows with invalid OrderID (dropped): {len(invalid_orders)}")

# After cleaning
valid_df = df.dropna(subset=['OrderID'])  # Assume OrderID is critical
print(f"✅ Rows with valid OrderID: {len(valid_df)}")

# orderinfo: one row per order
print(f"📁 Unique orders (orderinfo): {len(orderinfo_data)}")
print(f"📁 Total order-item entries (before group): {len(df)}")
print(f"📦 Grouped order-item rows (orderitems): {len(orderitems_grouped)}")

# Optional: warn if quantity > 10 (possible error)
high_qty = orderitems_grouped[orderitems_grouped['Quantity'] > 10]
if len(high_qty) > 0:
    print(f"⚠️  High quantity items (Qty > 10): {len(high_qty)}")
    print(high_qty[['OrderID', 'Item', 'Quantity']].head(5).to_string(index=False))

print("="*50)

print(f"✅ Generated orderitems.sql with {len(orderitems_grouped)} grouped item entries")
print("🎉 All SQL files generated successfully!")