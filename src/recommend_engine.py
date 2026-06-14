import pandas as pd


def get_popular_products(
    recommendations_path="../data/recommendations/popularity_recommendations.csv",
    top_n=10
):
    """
    Return top popular products.
    """

    popular_products = pd.read_csv(recommendations_path)

    return popular_products.head(top_n)


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


def get_all_recommendations(
    product_id,
    collaborative_function,
    content_function,
    recommendations_path="../data/recommendations/popularity_recommendations.csv"
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