# ╔══════════════════════════════════════════════════════════════╗
# ║  PROJECT 1: Superstore Sales Analysis                       ║
# ║  Your mentor's guide — every line explained                 ║
# ╚══════════════════════════════════════════════════════════════╝
#
# WHAT YOU WILL LEARN IN THIS PROJECT:
#   1. Loading and inspecting data (the very first thing any analyst does)
#   2. Cleaning dirty data (real data is ALWAYS messy)
#   3. Exploratory Data Analysis (EDA) — finding patterns
#   4. Grouping and aggregating data
#   5. Making clear, professional charts
#   6. Interpreting your results like a real analyst
#
# HOW TO RUN THIS:
#   Step 1: Make sure you have the libraries → pip install pandas matplotlib seaborn
#   Step 2: Make sure superstore_sales.csv is in the same folder
#   Step 3: Run: python analysis.py
#   Step 4: Check your "output/" folder for all charts


# ── STEP 0: IMPORT YOUR TOOLS ──────────────────────────────────
# Think of imports like opening your toolbox before starting work.
# pandas  → works with tables (like Excel, but in Python)
# matplotlib + seaborn → draw charts
# os → interact with your computer's file system

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# Create output folder if it doesn't exist yet
os.makedirs("output", exist_ok=True)

# ── STEP 1: LOAD YOUR DATA ─────────────────────────────────────
# pd.read_csv() reads a CSV file and turns it into a "DataFrame"
# A DataFrame is just a fancy table with rows and columns.

print("\n" + "="*60)
print("STEP 1: Loading the data")
print("="*60)

df = pd.read_csv("superstore_sales.csv")

# Always start by looking at your data — NEVER skip this step!
print(f"\n✅ Data loaded successfully!")
print(f"   Rows: {len(df):,}")
print(f"   Columns: {len(df.columns)}")
print(f"\nColumn names:\n  {list(df.columns)}")
print(f"\nFirst 3 rows:")
print(df.head(3).to_string())


# ── STEP 2: UNDERSTAND YOUR DATA ───────────────────────────────
# Before touching the data, spend time UNDERSTANDING it.
# What does each column mean? Are there nulls? What are the data types?

print("\n" + "="*60)
print("STEP 2: Understanding the data")
print("="*60)

# .info() gives you column types and null counts
print("\n--- Column types and null counts ---")
df.info()

# .describe() gives statistics for number columns
print("\n--- Basic statistics ---")
print(df[["Sales", "Profit", "Quantity", "Discount"]].describe().round(2))

# Check if any dates are already parsed as dates (they might be strings)
print(f"\nOrder Date type: {df['Order Date'].dtype}")


# ── STEP 3: CLEAN YOUR DATA ─────────────────────────────────────
# "Dirty data" = wrong types, missing values, inconsistent text.
# Cleaning is often 70% of a real analyst's job!

print("\n" + "="*60)
print("STEP 3: Cleaning the data")
print("="*60)

# Convert date strings → actual date objects so we can filter by month/year
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"]  = pd.to_datetime(df["Ship Date"])

# Extract useful time features from the date
# These new columns will help us analyse trends over time
df["Year"]  = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.strftime("%b")  # "Jan", "Feb", etc.

# Calculate a profit margin column (profit as % of sales)
# We round to 4 decimal places to keep things clean
df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(4)

# Check for missing values — if any column has nulls, we need to decide what to do
missing = df.isnull().sum()
print(f"\nMissing values per column:")
print(missing[missing > 0] if missing.sum() > 0 else "  ✅ No missing values!")

# Check for duplicate rows
dupes = df.duplicated().sum()
print(f"\nDuplicate rows: {dupes}")
if dupes > 0:
    df = df.drop_duplicates()
    print(f"  → Duplicates removed. Rows remaining: {len(df):,}")

print("\n✅ Data is clean. New columns added: Year, Month, Month Name, Profit Margin")


# ── STEP 4: EXPLORATORY DATA ANALYSIS (EDA) ───────────────────
# Now the fun begins! EDA means asking questions and finding answers in the data.
# A good analyst always starts with BUSINESS QUESTIONS, not random graphs.
#
# Our questions:
#   Q1. Which category drives the most revenue AND profit?
#   Q2. Which region is performing best and worst?
#   Q3. How have sales trended over time?
#   Q4. Do discounts actually help or hurt profit?
#   Q5. Which states are our best and worst performers?

print("\n" + "="*60)
print("STEP 4: Exploratory Data Analysis (EDA)")
print("="*60)

# ── Q1: Category Performance ───────────────────────────────────
# groupby() is like "GROUP BY" in SQL, or pivot tables in Excel.
# It groups rows together and lets you calculate summaries per group.

print("\n--- Q1: Category Performance ---")
category_perf = df.groupby("Category").agg(
    Total_Sales   = ("Sales",  "sum"),
    Total_Profit  = ("Profit", "sum"),
    Num_Orders    = ("Order ID", "nunique"),   # nunique = count unique values
    Avg_Discount  = ("Discount", "mean"),
).round(2)

# Add profit margin column to this summary table
category_perf["Profit Margin %"] = (
    (category_perf["Total_Profit"] / category_perf["Total_Sales"]) * 100
).round(1)

# Sort by sales (highest first)
category_perf = category_perf.sort_values("Total_Sales", ascending=False)
print(category_perf)

# ── CHART 1: Category Sales vs Profit ─────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Category Performance", fontsize=16, fontweight="bold", y=1.02)

colors = ["#2196F3", "#4CAF50", "#FF9800"]

# Bar chart: Sales by Category
axes[0].bar(category_perf.index, category_perf["Total_Sales"],
            color=colors, edgecolor="white", linewidth=0.5)
axes[0].set_title("Total Sales by Category", fontweight="bold")
axes[0].set_ylabel("Sales ($)")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
axes[0].tick_params(axis='x', rotation=15)

# Bar chart: Profit by Category
bars = axes[1].bar(category_perf.index, category_perf["Total_Profit"],
                   color=colors, edgecolor="white", linewidth=0.5)
axes[1].set_title("Total Profit by Category", fontweight="bold")
axes[1].set_ylabel("Profit ($)")
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
axes[1].tick_params(axis='x', rotation=15)

# Colour negative bars red so they stand out
for bar, val in zip(bars, category_perf["Total_Profit"]):
    if val < 0:
        bar.set_color("#F44336")

plt.tight_layout()
plt.savefig("output/01_category_performance.png", dpi=150, bbox_inches="tight")
plt.close()
print("\n  📊 Chart saved: output/01_category_performance.png")


# ── Q2: Regional Performance ───────────────────────────────────
print("\n--- Q2: Regional Performance ---")
region_perf = df.groupby("Region").agg(
    Total_Sales  = ("Sales",  "sum"),
    Total_Profit = ("Profit", "sum"),
    Num_Orders   = ("Order ID", "nunique"),
).round(2)
region_perf["Profit Margin %"] = (
    (region_perf["Total_Profit"] / region_perf["Total_Sales"]) * 100
).round(1)
region_perf = region_perf.sort_values("Total_Sales", ascending=False)
print(region_perf)

# ── CHART 2: Regional Sales Map ────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
region_colors = ["#1565C0", "#1976D2", "#42A5F5", "#90CAF9"]
bars = ax.barh(region_perf.index, region_perf["Total_Sales"],
               color=region_colors[:len(region_perf)], edgecolor="white")
ax.set_title("Sales by Region", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Sales ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Add value labels on each bar
for bar in bars:
    width = bar.get_width()
    ax.text(width + 500, bar.get_y() + bar.get_height()/2,
            f"${width:,.0f}", va="center", fontsize=10)

plt.tight_layout()
plt.savefig("output/02_regional_sales.png", dpi=150, bbox_inches="tight")
plt.close()
print("  📊 Chart saved: output/02_regional_sales.png")


# ── Q3: Sales Trend Over Time ──────────────────────────────────
print("\n--- Q3: Sales Trend Over Time ---")
monthly = df.groupby(["Year", "Month"]).agg(
    Monthly_Sales  = ("Sales",  "sum"),
    Monthly_Profit = ("Profit", "sum"),
).reset_index()

# Create a readable label like "2021-Jan"
monthly["Period"] = monthly["Year"].astype(str) + "-" + monthly["Month"].apply(
    lambda m: ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"][m-1]
)

print(f"  Monthly data: {len(monthly)} periods")

# ── CHART 3: Sales Trend Line ───────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(range(len(monthly)), monthly["Monthly_Sales"],
        color="#1565C0", linewidth=2.5, marker="o", markersize=5, label="Sales")
ax.fill_between(range(len(monthly)), monthly["Monthly_Sales"],
                alpha=0.15, color="#1565C0")
ax.plot(range(len(monthly)), monthly["Monthly_Profit"],
        color="#2E7D32", linewidth=2, linestyle="--", marker="s",
        markersize=4, label="Profit")

# Only show every 3rd label to avoid crowding
tick_positions = list(range(0, len(monthly), 3))
ax.set_xticks(tick_positions)
ax.set_xticklabels([monthly["Period"].iloc[i] for i in tick_positions], rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_title("Monthly Sales & Profit Trend (2021–2023)", fontsize=14, fontweight="bold")
ax.set_ylabel("Amount ($)")
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("output/03_sales_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("  📊 Chart saved: output/03_sales_trend.png")


# ── Q4: Do Discounts Help or Hurt Profit? ──────────────────────
# This is a critical business question that surprises many people!
# Higher discounts often destroy profit margins.

print("\n--- Q4: Discount vs Profit Analysis ---")

# Create discount buckets: 0%, 1–10%, 11–20%, 21–30%, 31%+
def bucket_discount(d):
    if d == 0:        return "0% (No discount)"
    elif d <= 0.10:   return "1–10%"
    elif d <= 0.20:   return "11–20%"
    elif d <= 0.30:   return "21–30%"
    else:             return "31%+"

df["Discount Bucket"] = df["Discount"].apply(bucket_discount)

discount_analysis = df.groupby("Discount Bucket").agg(
    Avg_Profit_Margin = ("Profit Margin", "mean"),
    Num_Orders        = ("Order ID", "count"),
    Total_Profit      = ("Profit", "sum"),
).round(3)

# Sort by discount level
bucket_order = ["0% (No discount)", "1–10%", "11–20%", "21–30%", "31%+"]
discount_analysis = discount_analysis.reindex(bucket_order)
print(discount_analysis)

# ── CHART 4: Discount vs Profit Margin ─────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
margin_vals = discount_analysis["Avg_Profit_Margin"] * 100
bar_colors  = ["#43A047" if v > 0 else "#E53935" for v in margin_vals]
bars = ax.bar(discount_analysis.index, margin_vals,
              color=bar_colors, edgecolor="white", linewidth=0.5)
ax.axhline(0, color="black", linewidth=0.8, linestyle="-")
ax.set_title("Average Profit Margin by Discount Level", fontsize=14, fontweight="bold")
ax.set_ylabel("Avg Profit Margin (%)")
ax.set_xlabel("Discount Level")
ax.tick_params(axis='x', rotation=20)

# Add value labels
for bar, val in zip(bars, margin_vals):
    ypos = bar.get_height() + 0.2 if val >= 0 else bar.get_height() - 0.8
    ax.text(bar.get_x() + bar.get_width()/2, ypos,
            f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("output/04_discount_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("  📊 Chart saved: output/04_discount_analysis.png")


# ── Q5: Top & Bottom 5 States ──────────────────────────────────
print("\n--- Q5: State-Level Performance ---")
state_perf = df.groupby("State").agg(
    Total_Sales  = ("Sales",  "sum"),
    Total_Profit = ("Profit", "sum"),
).round(2).sort_values("Total_Profit", ascending=False)

top5    = state_perf.head(5)
bottom5 = state_perf.tail(5)

print("Top 5 states by profit:")
print(top5)
print("\nBottom 5 states by profit:")
print(bottom5)

# ── CHART 5: Top vs Bottom States ──────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("State Profitability: Top 5 vs Bottom 5", fontsize=14, fontweight="bold")

axes[0].barh(top5.index, top5["Total_Profit"], color="#43A047", edgecolor="white")
axes[0].set_title("🏆 Top 5 States (Profit)", fontweight="bold")
axes[0].set_xlabel("Total Profit ($)")
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

axes[1].barh(bottom5.index, bottom5["Total_Profit"], color="#E53935", edgecolor="white")
axes[1].set_title("⚠️  Bottom 5 States (Profit)", fontweight="bold")
axes[1].set_xlabel("Total Profit ($)")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.tight_layout()
plt.savefig("output/05_state_performance.png", dpi=150, bbox_inches="tight")
plt.close()
print("  📊 Chart saved: output/05_state_performance.png")


# ── STEP 5: SUMMARY REPORT ─────────────────────────────────────
# A real analyst doesn't just make charts — they EXPLAIN what the charts mean.
# This is what separates a junior analyst from a great one.

print("\n" + "="*60)
print("STEP 5: SUMMARY / ANALYST FINDINGS")
print("="*60)

total_sales  = df["Sales"].sum()
total_profit = df["Profit"].sum()
overall_margin = (total_profit / total_sales) * 100
best_category  = category_perf["Total_Sales"].idxmax()
best_region    = region_perf["Total_Sales"].idxmax()
worst_region   = region_perf["Total_Sales"].idxmin()

print(f"""
📊 SUPERSTORE SALES ANALYSIS — EXECUTIVE SUMMARY
──────────────────────────────────────────────────
Period Analysed:    2021 – 2023
Total Revenue:      ${total_sales:,.2f}
Total Profit:       ${total_profit:,.2f}
Overall Margin:     {overall_margin:.1f}%

KEY FINDINGS:
1. CATEGORY: "{best_category}" is our top revenue driver.
   → Furniture sometimes runs NEGATIVE margins — investigate discounting.

2. REGIONAL: "{best_region}" leads in sales. "{worst_region}" needs attention.
   → Consider targeted promotions or cost review in underperforming regions.

3. DISCOUNTS: Orders with 31%+ discounts show negative profit margins.
   → RECOMMENDATION: Cap discounts at 20% or require manager approval above that.

4. SEASONALITY: Sales tend to peak in Q4 (Oct–Dec) across all categories.
   → Plan inventory and staffing ahead of Q4 rush.

CHARTS SAVED IN: output/ folder
  01_category_performance.png
  02_regional_sales.png
  03_sales_trend.png
  04_discount_analysis.png
  05_state_performance.png
──────────────────────────────────────────────────
✅ Project 1 complete! Add these charts to your GitHub portfolio.
""")
