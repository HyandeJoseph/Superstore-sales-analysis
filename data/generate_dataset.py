"""
Dataset Generator for Project 1: Superstore Sales Analysis
Run this once to create your dataset: python generate_dataset.py
"""

import csv
import random
from datetime import date, timedelta

random.seed(42)

# ── CONFIGURATION ──────────────────────────────────────────────
CATEGORIES = {
    "Furniture": ["Office Chair", "Bookcase", "Desk", "Filing Cabinet", "Sofa"],
    "Technology": ["Laptop", "Printer", "Phone", "Monitor", "USB Hub", "Keyboard"],
    "Office Supplies": ["Pens", "Notebooks", "Stapler", "Paper Ream", "Folders", "Tape"],
}

REGIONS = ["West", "East", "Central", "South"]
STATES_BY_REGION = {
    "West":    ["California", "Oregon", "Washington", "Nevada", "Arizona"],
    "East":    ["New York", "Pennsylvania", "New Jersey", "Massachusetts", "Virginia"],
    "Central": ["Texas", "Illinois", "Ohio", "Michigan", "Indiana"],
    "South":   ["Florida", "Georgia", "North Carolina", "Tennessee", "Alabama"],
}
SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]

# Price ranges per category
PRICE_RANGE = {
    "Furniture":      (80,  1200),
    "Technology":     (30,   900),
    "Office Supplies":(2,    60),
}

# Discount frequency: some items get discounts, some don't
DISCOUNT_OPTIONS = [0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20, 0.30]

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def generate_row(order_id, row_id):
    region   = random.choice(REGIONS)
    state    = random.choice(STATES_BY_REGION[region])
    category = random.choice(list(CATEGORIES.keys()))
    product  = random.choice(CATEGORIES[category])
    segment  = random.choice(SEGMENTS)
    ship_mode = random.choice(SHIP_MODES)

    order_date = random_date(date(2021, 1, 1), date(2023, 12, 31))
    ship_date  = order_date + timedelta(days=random.randint(1, 7))

    quantity   = random.randint(1, 10)
    unit_price = round(random.uniform(*PRICE_RANGE[category]), 2)
    discount   = random.choice(DISCOUNT_OPTIONS)
    sales      = round(unit_price * quantity * (1 - discount), 2)

    # Profit margin varies by category
    if category == "Furniture":
        profit_pct = random.uniform(-0.10, 0.25)   # furniture sometimes loses money!
    elif category == "Technology":
        profit_pct = random.uniform(0.05, 0.35)
    else:
        profit_pct = random.uniform(0.10, 0.50)

    profit = round(sales * profit_pct, 2)

    return {
        "Row ID":       row_id,
        "Order ID":     order_id,
        "Order Date":   order_date.strftime("%Y-%m-%d"),
        "Ship Date":    ship_date.strftime("%Y-%m-%d"),
        "Ship Mode":    ship_mode,
        "Segment":      segment,
        "Region":       region,
        "State":        state,
        "Category":     category,
        "Product Name": product,
        "Sales":        sales,
        "Quantity":     quantity,
        "Discount":     discount,
        "Profit":       profit,
    }

def main():
    rows = []
    row_id = 1
    order_counter = 1000

    for _ in range(2000):   # 2,000 rows — good size for a beginner project
        order_id = f"CA-{2021 + row_id % 3}-{str(order_counter).zfill(6)}"
        # Each order can have 1-4 line items
        num_items = random.randint(1, 4)
        for _ in range(num_items):
            rows.append(generate_row(order_id, row_id))
            row_id += 1
        order_counter += 1

    # Write to CSV
    output_path = "superstore_sales.csv"
    fieldnames  = list(rows[0].keys())

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅  Dataset created: {output_path}")
    print(f"    Rows: {len(rows)}")
    print(f"    Date range: 2021-01-01 → 2023-12-31")

if __name__ == "__main__":
    main()
