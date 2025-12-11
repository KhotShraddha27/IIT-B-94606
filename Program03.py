import csv

# Read CSV file
with open("products.csv", "r") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# a) Row in clean format
print("---- PRODUCT DETAILS ----")
for row in rows:
    print(f"ID: {row['product_id']}, Product_Name: {row['product_name']}, Category: {row['category']}, "
          f"Price: {row['price']}, Quantity: {row['quantity']}")

# b) Total number of rows
print("\nTotal number of rows:", len(rows))

# c) Total number of products priced above 500
count_above_500 = sum(1 for row in rows if float(row["price"]) > 500)
print("Products priced above 500:", count_above_500)

# d) Average price of all products
avg_price = sum(float(row["price"]) for row in rows) / len(rows)
print("Average price of all products:", avg_price)

# e) List all products from a specific category
category = input("\nEnter category to search: ").strip().lower()
print(f"\nProducts in category '{category}':")
found = False
for row in rows:
    if row["category"].strip().lower() == category:
        print(f"- {row['product_name']} (Price: {row['price']}, Qty: {row['quantity']})")
        found = True
if not found:
    print("No products found in this category.")

# f) Total quantity of all items in stock
total_qty = sum(int(row["quantity"]) for row in rows)
print("\nTotal quantity in stock:", total_qty)
