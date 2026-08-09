"""
Evaluation utilities for the Amazon Product Recommendation System.

Models evaluated:
1. Popularity-based recommendation
2. Item-based Collaborative Filtering
3. Content-Based Filtering

This evaluation focuses on recommendation quality checks and
behavioral metrics rather than claiming supervised accuracy metrics.
"""

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

POPULARITY_PATH = os.path.join(
    BASE_DIR,
    "data",
    "recommendations",
    "popularity_recommendations.csv"
)


# --------------------------------------------------
# Data Loading
# --------------------------------------------------

def load_data():
    """
    Load product-level information from the raw dataset.
    """

    df = pd.read_csv(
        RAW_DATA_PATH,
        usecols=["ProductId", "Score"]
    )

    product_stats = (
        df.groupby("ProductId")
        .agg(
            average_rating=("Score", "mean"),
            review_count=("Score", "count")
        )
        .reset_index()
    )

    return product_stats


def load_popularity_recommendations():
    """
    Load the existing popularity-based recommendations.
    """

    return pd.read_csv(POPULARITY_PATH)


# --------------------------------------------------
# Recommendation Normalization
# --------------------------------------------------

def normalize_recommendations(recommendations):
    """
    Convert different recommendation output formats
    into a simple list of ProductIds.
    """

    if recommendations is None:
        return []

    # Pandas DataFrame
    if isinstance(recommendations, pd.DataFrame):

        if "ProductId" in recommendations.columns:
            return recommendations["ProductId"].tolist()

        if "product_id" in recommendations.columns:
            return recommendations["product_id"].tolist()

        return recommendations.iloc[:, 0].tolist()

    # Pandas Series
    if isinstance(recommendations, pd.Series):
        return recommendations.tolist()

    # List / tuple / other iterable
    try:
        return list(recommendations)

    except TypeError:
        return []


# --------------------------------------------------
# Single Model Evaluation
# --------------------------------------------------

def evaluate_model(
    model_name,
    recommender,
    product_id,
    product_stats,
    top_k=5
):
    """
    Evaluate one recommendation model for a single product.
    """

    try:
        recommendations = recommender(product_id)

    except Exception as e:

        return {
            "model": model_name,
            "product_id": product_id,
            "success": False,
            "recommendation_count": 0,
            "unique_count": 0,
            "duplicates": 0,
            "self_recommended": False,
            "average_rating": None,
            "average_review_count": None,
            "recommendations": [],
            "error": str(e)
        }

    recommendations = normalize_recommendations(
        recommendations
    )

    recommendations = recommendations[:top_k]

    unique_recommendations = list(
        dict.fromkeys(recommendations)
    )

    duplicate_count = (
        len(recommendations)
        - len(unique_recommendations)
    )

    self_recommended = product_id in unique_recommendations

    # Remove input product from quality statistics
    metadata = product_stats[
        product_stats["ProductId"].isin(
            unique_recommendations
        )
        &
        (product_stats["ProductId"] != product_id)
    ]

    if len(metadata) > 0:

        average_rating = metadata[
            "average_rating"
        ].mean()

        average_review_count = metadata[
            "review_count"
        ].mean()

    else:

        average_rating = None
        average_review_count = None

    return {
        "model": model_name,
        "product_id": product_id,
        "success": True,
        "recommendation_count": len(recommendations),
        "unique_count": len(unique_recommendations),
        "duplicates": duplicate_count,
        "self_recommended": self_recommended,
        "average_rating": average_rating,
        "average_review_count": average_review_count,
        "recommendations": unique_recommendations,
        "error": None
    }


# --------------------------------------------------
# Recommendation Overlap
# --------------------------------------------------

def calculate_jaccard(list_a, list_b):
    """
    Calculate Jaccard similarity between two recommendation lists.
    """

    set_a = set(list_a)
    set_b = set(list_b)

    if not set_a and not set_b:
        return 1.0

    union = set_a | set_b

    if not union:
        return 0.0

    intersection = set_a & set_b

    return len(intersection) / len(union)


# --------------------------------------------------
# Evaluate Models Across Multiple Products
# --------------------------------------------------

def evaluate_models(
    product_ids,
    collaborative_func,
    content_func,
    top_k=5
):
    """
    Evaluate collaborative and content-based models
    across multiple test products.
    """

    product_stats = load_data()

    results = []

    for product_id in product_ids:

        collaborative_result = evaluate_model(
            "Collaborative Filtering",
            collaborative_func,
            product_id,
            product_stats,
            top_k
        )

        content_result = evaluate_model(
            "Content-Based",
            content_func,
            product_id,
            product_stats,
            top_k
        )

        results.append(
            collaborative_result
        )

        results.append(
            content_result
        )

    return results


# --------------------------------------------------
# Print Evaluation Report
# --------------------------------------------------

def print_evaluation_report(results):

    print("=" * 70)
    print("RECOMMENDATION MODEL EVALUATION")
    print("=" * 70)

    results_df = pd.DataFrame(results)

    successful = results_df[
        results_df["success"] == True
    ]

    if successful.empty:

        print("\nNo successful recommendations.")
        return

    print("\nMODEL SUMMARY")
    print("-" * 70)

    summary = (
        successful
        .groupby("model")
        .agg(
            queries=("product_id", "count"),
            avg_recommendations=(
                "recommendation_count",
                "mean"
            ),
            avg_unique=(
                "unique_count",
                "mean"
            ),
            avg_duplicates=(
                "duplicates",
                "mean"
            ),
            self_recommendations=(
                "self_recommended",
                "sum"
            ),
            avg_rating=(
                "average_rating",
                "mean"
            ),
            avg_review_count=(
                "average_review_count",
                "mean"
            )
        )
        .reset_index()
    )

    print(
        summary.to_string(
            index=False
        )
    )

    print("\nINDIVIDUAL RESULTS")
    print("-" * 70)

    for result in results:

        print(
            f"\nProduct: {result['product_id']}"
        )

        print(
            f"Model: {result['model']}"
        )

        if not result["success"]:

            print(
                f"ERROR: {result['error']}"
            )

            continue

        print(
            f"Recommendations: "
            f"{result['recommendations']}"
        )

        print(
            f"Duplicates: "
            f"{result['duplicates']}"
        )

        print(
            f"Self recommended: "
            f"{result['self_recommended']}"
        )

        if result["average_rating"] is not None:

            print(
                f"Average recommended rating: "
                f"{result['average_rating']:.2f}"
            )

            print(
                f"Average recommended review count: "
                f"{result['average_review_count']:.2f}"
            )

    # --------------------------------------------------
    # Collaborative vs Content Overlap
    # --------------------------------------------------

    print("\n" + "=" * 70)
    print("COLLABORATIVE vs CONTENT OVERLAP")
    print("=" * 70)

    product_ids = results_df[
        "product_id"
    ].unique()

    overlaps = []

    for product_id in product_ids:

        collaborative = results_df[
            (results_df["product_id"] == product_id)
            &
            (results_df["model"] == "Collaborative Filtering")
        ]

        content = results_df[
            (results_df["product_id"] == product_id)
            &
            (results_df["model"] == "Content-Based")
        ]

        if collaborative.empty or content.empty:
            continue

        if not collaborative.iloc[0]["success"]:
            continue

        if not content.iloc[0]["success"]:
            continue

        score = calculate_jaccard(
            collaborative.iloc[0]["recommendations"],
            content.iloc[0]["recommendations"]
        )

        overlaps.append(score)

        print(
            f"{product_id}: "
            f"{score:.2f}"
        )

    if overlaps:

        print(
            f"\nAverage Jaccard overlap: "
            f"{sum(overlaps) / len(overlaps):.3f}"
        )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    from src.collaborative_filtering import (
        recommend_collaborative,
        product_to_index
    )

    from src.content_based import (
        recommend_content
    )

    product_stats = load_data()

    # Select products that actually exist in the
    # collaborative filtering model.
    valid_products = list(product_to_index.keys())

    test_products = (
        product_stats[
            product_stats["ProductId"].isin(valid_products)
        ]
        .query("review_count >= 20")
        .sample(
            n=5,
            random_state=42
        )["ProductId"]
        .tolist()
    )

    print("Test products:")

    for product in test_products:
        print(f"- {product}")

    results = evaluate_models(
        test_products,
        recommend_collaborative,
        recommend_content,
        top_k=5
    )

    print_evaluation_report(results)