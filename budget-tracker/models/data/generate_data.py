import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# Assign spending levels to users
spending_levels = ["low", "medium", "high"]
user_spending_levels = {user_id: random.choice(spending_levels) for user_id in range(1000)}

# Spending categories and some example vendors per category
categories = {
    "Groceries": ["Whole Foods", "Trader Joe's", "Market Basket", "Walmart", "Stop & Shop"],
    "Dining": ["Starbucks", "Chipotle", "Dunkin'", "Pressed Cafe"],
    "Travel": ["Delta Airlines", "Uber", "Airbnb", "Marriott", "Lyft"],
    "Entertainment": ["Netflix", "AMC Theaters", "Spotify", "Apple Music", "Hulu", "Concert"],
    "Utilities": ["Comcast", "National Grid", "Xfinity", "Water Dept"],
    "Healthcare": ["CVS Pharmacy", "Walgreens", "Blue Cross", "Dental Care"],
    "Rent": ["Landlord", "Management Company", "Apartment Complex"],
    "Shopping": ["Amazon", "Target", "Abercrombie", "H&M", "Old Navy", "Apple Store", "Sephora"],
    "Education": ["Coursera", "Udemy", "Bookstore"],
    "Personal Care": ["Hair Salon", "Nail Salon", "Spa", "Gym Membership"],
    "Miscellaneous": ["Post Office", "Gas Station", "Donation"]
}

# Average monthly spending ranges per category (in USD)
avg_spend = {
    "low": {
        "Groceries": (50, 200),
        "Dining": (0, 100),
        "Travel": (0, 150),
        "Entertainment": (0, 50),
        "Utilities": (0, 50),
        "Healthcare": (0, 150),
        "Rent": (1000, 1500),
        "Shopping": (50, 100),
        "Education": (0, 150),
        "Personal Care": (0, 50),
        "Miscellaneous": (0, 100)
    },
    "medium": {
        "Groceries": (201, 400),
        "Dining": (101, 300),
        "Travel": (151, 400),
        "Entertainment": (51, 200),
        "Utilities": (51, 150),
        "Healthcare": (151, 300),
        "Rent": (1501, 2200),
        "Shopping": (101, 250),
        "Education": (151, 300),
        "Personal Care": (51, 200),
        "Miscellaneous": (101, 200)
    },
    "high": {
        "Groceries": (401, 600),
        "Dining": (301, 600),
        "Travel": (401, 2000),
        "Entertainment": (201, 500),
        "Utilities": (151, 300),
        "Healthcare": (301, 1000),
        "Rent": (2201, 5000),
        "Shopping": (251, 3000),
        "Education": (301, 5000),
        "Personal Care": (201, 600),
        "Miscellaneous": (201, 1000)
    }
}

def generate_transaction(user_id, date):
    spending_level = user_spending_levels[user_id]

    # Randomly choose a category and vendor, avoiding "Rent" for daily transactions
    category = random.choice([cat for cat in categories.keys() if cat != "Rent"])
    vendor = random.choice(categories[category])
    avg_min, avg_max = avg_spend[spending_level][category]

    # Assume 5-20 transactions per month per category
    num_tx = random.randint(5, 20)
    amount = round(np.random.normal((avg_min + avg_max) / 2 / num_tx, 5), 2)
    amount = max(1.0, amount)  # min $1
    return {
        "user_id": user_id,
        "date": date,
        "category": category,
        "vendor": vendor,
        "amount": amount,
    }

def generate_rent_transaction(user_id, month):
    category = "Rent"
    vendor = random.choice(categories[category])
    spending_level = user_spending_levels[user_id]
    
    avg_min, avg_max = avg_spend[spending_level][category]
    amount = round(np.random.uniform(avg_min, avg_max), 2)  # Rent is a fixed monthly payment
    return {
        "user_id": user_id,
        "date": f"2024-{month:02d}-01",  # Rent is paid on the first of the month
        "category": category,
        "vendor": vendor,
        "amount": amount,
    }

def generate_monthly_data(year, month, num_days):
    data = []
    # generate data for each day of the month
    for day in range(1, num_days + 1):
        # generate data for each user
        for user in range(0, 1000):
            date = f"{year}-{month:02d}-{day:02d}"
            if day == 1:
                rent_tx = generate_rent_transaction(user, month)
                data.append(rent_tx)
            
            # Random number of transactions per day
            transactions_per_day = random.randint(0, 10)
            for _ in range(transactions_per_day):
                tx = generate_transaction(user, date)
                data.append(tx)
    return data

# Generate 12 months of data (Jan-Dec 2024)
all_data = []
for month in range(1, 13):
    # Handle different number of days in each month
    if month == 2:
        num_days = 29
    elif month in [4, 6, 9, 11]:
        num_days = 30
    else:
        num_days = 31
    all_data.extend(generate_monthly_data(2024, month, num_days))

df = pd.DataFrame(all_data)

# Shuffle rows
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
df.to_csv("synthetic_credit_card_transactions.csv", index=False)

print(df.head())
