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

CONTENT_SIMILARITY_PATH = os.path.join(
    MODEL_DIR,
    "content_similarity.pkl"
)

TFIDF_VECTORIZER_PATH = os.path.join(
    MODEL_DIR,
    "tfidf_vectorizer.pkl"
)

PRODUCT_IDS_PATH = os.path.join(
    MODEL_DIR,
    "content_product_ids.pkl"
)


# --------------------------------------------------
# Load trained content-based model
# --------------------------------------------------

with open(CONTENT_SIMILARITY_PATH, "rb") as f:
    content_similarity = pickle.load(f)

with open(TFIDF_VECTORIZER_PATH, "rb") as f:
    tfidf_vectorizer = pickle.load(f)

with open(PRODUCT_IDS_PATH, "rb") as f:
    product_ids = pickle.load(f)


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

def recommend_content(product_id, top_n=5):
    """
    Return products similar to the given product
    using content-based filtering.

    Similarity is based on TF-IDF representations
    of product review text.
    """

    if product_id not in product_to_index:
        raise ValueError(
            f"Product ID '{product_id}' is not available "
            "in the content-based model."
        )

    idx = product_to_index[product_id]

    similarity_scores = content_similarity[idx]

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