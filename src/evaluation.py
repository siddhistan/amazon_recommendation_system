"""
Evaluation utilities for recommendation models.

Models:
1. Popularity Recommender
2. Collaborative Filtering
3. Content-Based Filtering
"""

def compare_recommendations(
    product_id,
    collaborative_func,
    content_func
):

    print("=" * 50)
    print("PRODUCT:", product_id)

    print("\nCollaborative Filtering:")
    print(collaborative_func(product_id))

    print("\nContent-Based Filtering:")
    print(content_func(product_id))
    
def show_top_popular(popular_products, n=10):
    
    print("=" * 50)
    print(f"TOP {n} POPULAR PRODUCTS")

    print(popular_products.head(n))
    
def count_unique_recommendations(recommendations):
    
    return len(set(recommendations))