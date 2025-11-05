# hotel_analytics.py
# Robust loader + adaptive analytics for Kaggle or fallback local CSV

import os
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Candidate names we will try to detect automatically
CANDIDATES = [
    "hotel_bookings.csv",
    "hotel_bookings (1).csv",
    "hotel_booking.csv",
    "hotel-bookings.csv",
    "Hotel Bookings.csv",
    "hotel_bookings_final.csv"
]

FALLBACK = "hotel_data.csv"

def find_dataset():
    files = os.listdir(BASE_DIR)
    print("Files in project folder:", files)
    # Look for candidate files (case-insensitive)
    for name in CANDIDATES:
        path = os.path.join(BASE_DIR, name)
        if os.path.isfile(path):
            return path, "kaggle"
    # also try any csv containing 'hotel' and 'book'
    for f in files:
        if f.lower().endswith(".csv") and "hotel" in f.lower() and "book" in f.lower():
            return os.path.join(BASE_DIR, f), "kaggle"
    # fallback
    fb = os.path.join(BASE_DIR, FALLBACK)
    if os.path.isfile(fb):
        return fb, "fallback"
    return None, None

def load_csv(path):
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error reading '{path}': {e}")
        return None

def basic_info(df, source_label):
    print(f"\nLoaded dataset from: {source_label}")
    print("--- Basic Dataset Info ---")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    # show head
    print("\nFirst 5 rows:\n", df.head())

def analytics_for_kaggle(df):
    import matplotlib.pyplot as plt
    print("\n--- Kaggle-style analytics ---")
    # total_stay
    if "stays_in_weekend_nights" in df.columns and "stays_in_week_nights" in df.columns:
        df["total_stay"] = df["stays_in_weekend_nights"].fillna(0) + df["stays_in_week_nights"].fillna(0)
        print("Average stay (days):", df["total_stay"].mean())
    # cancellation
    if "is_canceled" in df.columns:
        cancel_rate = df["is_canceled"].mean() * 100
        print(f"Cancellation Rate: {cancel_rate:.2f}%")
    # revenue estimate
    if "adr" in df.columns:
        if "total_stay" in df.columns:
            df["revenue_estimate"] = df["adr"].fillna(0) * df["total_stay"]
        else:
            df["revenue_estimate"] = df["adr"].fillna(0)
        print("Estimated total revenue (sum):", df["revenue_estimate"].sum())
    # safe plots
    try:
        if "hotel" in df.columns:
            df["hotel"].value_counts().plot(kind="bar")
            plt.title("Bookings by Hotel Type")
            plt.tight_layout()
            plt.show()
        if "market_segment" in df.columns:
            df["market_segment"].value_counts().plot(kind="pie", autopct="%1.1f%%", figsize=(6,6))
            plt.title("Market Segment Distribution")
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print("Plot error:", e)

def analytics_for_fallback(df):
    import matplotlib.pyplot as plt
    print("\n--- Local fallback analytics (hotel_data.csv) ---")
    # treat phone as string
    if "Phone" in df.columns:
        df["Phone"] = df["Phone"].astype(str)
    # numeric stats
    if "Days" in df.columns:
        print("Average stay (Days):", pd.to_numeric(df["Days"], errors="coerce").mean())
    if "Amount" in df.columns:
        print("Total revenue (sum of Amount):", pd.to_numeric(df["Amount"], errors="coerce").sum())
    # room type distribution
    if "RoomType" in df.columns:
        try:
            df["RoomType"].value_counts().plot(kind="bar")
            plt.title("Room Type Distribution")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print("Plot failed:", e)

def main():
    path, typ = find_dataset()
    if path is None:
        print("No dataset found in project folder.")
        print(f"Put 'hotel_bookings.csv' (Kaggle) or run hotel_management.py to create '{FALLBACK}'.")
        sys.exit(1)
    print("Dataset path chosen:", path)
    df = load_csv(path)
    if df is None:
        print("Failed to load dataset. Exiting.")
        sys.exit(1)
    basic_info(df, path)
    if typ == "kaggle":
        analytics_for_kaggle(df)
    else:
        analytics_for_fallback(df)
    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()

