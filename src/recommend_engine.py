import os
import pandas as pd


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RECOMMENDATIONS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "recommendations",
    "popularity_recommendations.csv"
)


# --------------------------------------------------
# Popularity-Based Recommendations
# --------------------------------------------------

def get_popular_products(
    recommendations_path=RECOMMENDATIONS_PATH,
    top_n=10
):
    """
    Return the top popular products.

    Parameters
    ----------
    recommendations_path : str
        Path to the popularity recommendations CSV.

    top_n : int
        Number of popular products to return.

    Returns
    -------
    pandas.DataFrame
        Top popular products.
    """

    popular_products = pd.read_csv(
        recommendations_path
    )

    return popular_products.head(top_n)


# --------------------------------------------------
# Collaborative Filtering
# --------------------------------------------------

def get_collaborative_recommendations(
    product_id,
    collaborative_function,
    top_n=5
):
    """
    Return collaborative filtering recommendations.
    """

    return collaborative_function(
        product_id,
        top_n
    )


# --------------------------------------------------
# Content-Based Filtering
# --------------------------------------------------

def get_content_recommendations(
    product_id,
    content_function,
    top_n=5
):
    """
    Return content-based recommendations.
    """

    return content_function(
        product_id,
        top_n
    )


# --------------------------------------------------
# Get All Recommendation Types
# --------------------------------------------------

def get_all_recommendations(
    product_id,
    collaborative_function,
    content_function,
    recommendations_path=RECOMMENDATIONS_PATH
):
    """
    Return all recommendation types together.
    """

    return {
        "popular": get_popular_products(
            recommendations_path
        ),

        "collaborative": get_collaborative_recommendations(
            product_id,
            collaborative_function
        ),

        "content": get_content_recommendations(
            product_id,
            content_function
        )
    }