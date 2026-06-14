# app/app.py

from src.recommendation_engine import get_popular_products
from src.collaborative_filtering import recommend_collaborative
from src.content_based import recommend_content


def main():

    print("=" * 60)
    print("AMAZON PRODUCT RECOMMENDATION SYSTEM")
    print("=" * 60)

    product_id = input("\nEnter Product ID: ").strip()

    print("\nTOP POPULAR PRODUCTS")
    print("-" * 60)

    print(get_popular_products())

    print("\nCOLLABORATIVE FILTERING RECOMMENDATIONS")
    print("-" * 60)

    try:
        print(recommend_collaborative(product_id))

    except Exception as e:
        print("Error:", e)

    print("\nCONTENT-BASED RECOMMENDATIONS")
    print("-" * 60)

    try:
        print(recommend_content(product_id))

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()