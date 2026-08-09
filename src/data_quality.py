import os
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "Reviews.csv"
)


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

def load_raw_data(file_path=RAW_DATA_PATH):
    """
    Load the raw Amazon reviews dataset.
    """

    return pd.read_csv(file_path)


# --------------------------------------------------
# Basic Dataset Information
# --------------------------------------------------

def get_basic_statistics(df):
    """
    Return basic information about the dataset.
    """

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "unique_users": df["UserId"].nunique(),
        "unique_products": df["ProductId"].nunique(),
        "average_rating": df["Score"].mean(),
        "minimum_rating": df["Score"].min(),
        "maximum_rating": df["Score"].max()
    }


# --------------------------------------------------
# Missing Value Analysis
# --------------------------------------------------

def get_missing_values(df):
    """
    Return missing-value counts and percentages.
    """

    missing_count = df.isnull().sum()

    missing_percentage = (
        df.isnull().mean() * 100
    )

    result = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_percentage
    })

    return result[result["missing_count"] > 0].sort_values(
        "missing_count",
        ascending=False
    )


# --------------------------------------------------
# Duplicate Analysis
# --------------------------------------------------

def get_duplicate_count(df):
    """
    Return the number of duplicate rows.
    """

    return df.duplicated().sum()


# --------------------------------------------------
# Rating Validation
# --------------------------------------------------

def get_invalid_ratings(df):
    """
    Identify ratings outside the expected 1-5 range.
    """

    invalid = df[
        (df["Score"] < 1) |
        (df["Score"] > 5)
    ]

    return invalid


# --------------------------------------------------
# User-Product Duplicate Analysis
# --------------------------------------------------

def get_duplicate_user_product_pairs(df):
    """
    Identify users who reviewed the same product
    multiple times.
    """

    duplicates = (
        df.groupby(
            ["UserId", "ProductId"]
        )
        .size()
        .reset_index(name="review_count")
    )

    return duplicates[
        duplicates["review_count"] > 1
    ].sort_values(
        "review_count",
        ascending=False
    )


# --------------------------------------------------
# Review Date Analysis
# --------------------------------------------------

def get_date_range(df):
    """
    Return the earliest and latest review dates.
    """

    dates = pd.to_datetime(
        df["Time"],
        unit="s",
        errors="coerce"
    )

    return {
        "earliest_review": dates.min(),
        "latest_review": dates.max(),
        "invalid_dates": dates.isna().sum()
    }


# --------------------------------------------------
# Complete Data Quality Report
# --------------------------------------------------

def generate_quality_report(df):
    """
    Generate and print a complete data-quality report.
    """

    basic_stats = get_basic_statistics(df)
    missing_values = get_missing_values(df)
    duplicate_count = get_duplicate_count(df)
    invalid_ratings = get_invalid_ratings(df)
    duplicate_pairs = get_duplicate_user_product_pairs(df)
    date_info = get_date_range(df)

    print("=" * 60)
    print("AMAZON REVIEWS - DATA QUALITY REPORT")
    print("=" * 60)

    print("\nDATASET OVERVIEW")
    print("-" * 60)

    print(f"Rows:              {basic_stats['rows']:,}")
    print(f"Columns:           {basic_stats['columns']}")
    print(f"Unique users:      {basic_stats['unique_users']:,}")
    print(f"Unique products:   {basic_stats['unique_products']:,}")
    print(f"Average rating:    {basic_stats['average_rating']:.2f}")
    print(
        f"Rating range:      "
        f"{basic_stats['minimum_rating']} - "
        f"{basic_stats['maximum_rating']}"
    )

    print("\nMISSING VALUES")
    print("-" * 60)

    if missing_values.empty:
        print("No missing values found.")
    else:
        print(missing_values)

    print("\nDUPLICATE ROWS")
    print("-" * 60)

    print(f"Duplicate rows: {duplicate_count:,}")

    print("\nRATING VALIDATION")
    print("-" * 60)

    print(
        f"Invalid ratings: {len(invalid_ratings):,}"
    )

    print("\nUSER-PRODUCT DUPLICATES")
    print("-" * 60)

    print(
        f"User-product pairs with multiple reviews: "
        f"{len(duplicate_pairs):,}"
    )

    print("\nDATE VALIDATION")
    print("-" * 60)

    print(
        f"Earliest review: {date_info['earliest_review']}"
    )

    print(
        f"Latest review:   {date_info['latest_review']}"
    )

    print(
        f"Invalid dates:   {date_info['invalid_dates']:,}"
    )

    print("\n" + "=" * 60)


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    df = load_raw_data()

    generate_quality_report(df)