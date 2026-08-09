import os
import pickle


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(
    BASE_DIR,
    "data",
    "models"
)

PRODUCT_IDS_PATH = os.path.join(
    MODEL_DIR,
    "product_ids.pkl"
)

ITEM_SIMILARITY_PATH = os.path.join(
    MODEL_DIR,
    "item_similarity.pkl"
)


# --------------------------------------------------
# Load trained collaborative filtering model
# --------------------------------------------------

with open(PRODUCT_IDS_PATH, "rb") as f:
    product_ids = pickle.load(f)

with open(ITEM_SIMILARITY_PATH, "rb") as f:
    item_similarity = pickle.load(f)


# --------------------------------------------------
# Create Product ID -> Matrix Index mapping
# --------------------------------------------------

product_to_index = {
    product: idx
    for idx, product in enumerate(product_ids)
}


# --------------------------------------------------
# Recommendation Function
# --------------------------------------------------

def recommend_collaborative(product_id, top_n=5):
    """
    Return products similar to the given product
    using item-based collaborative filtering.

    Parameters
    ----------
    product_id : str
        Product ID for which recommendations are required.

    top_n : int
        Number of recommendations to return.

    Returns
    -------
    pandas.Index
        Product IDs of the most similar products.
    """

    if product_id not in product_to_index:
        raise ValueError(
            f"Product ID '{product_id}' is not available "
            "in the collaborative filtering model."
        )

    idx = product_to_index[product_id]

    similarity_scores = item_similarity[idx]

    sorted_indices = similarity_scores.argsort()[::-1]

    recommendations = []

    for index in sorted_indices:

        recommended_product = product_ids[index]

        if recommended_product == product_id:
           continue

        recommendations.append(
            recommended_product
        )

        if len(recommendations) == top_n:
           break

    return recommendations

