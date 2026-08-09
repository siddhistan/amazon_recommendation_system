# app/app.py

from src.recommend_engine import get_popular_products
from src.collaborative_filtering import recommend_collaborative
from src.content_based import recommend_content


def main():

    print("=" * 60)
    print("AMAZON PRODUCT RECOMMENDATION SYSTEM")
    print("=" * 60)

    product_id = input("\nEnter Product ID: ").strip()

    if not product_id:
        print("Error: Product ID cannot be empty.")
        return

    print("\n" + "=" * 60)
    print("TOP POPULAR PRODUCTS")
    print("=" * 60)

    try:
        popular_products = get_popular_products(top_n=10)
        print(popular_products.to_string(index=False))
    except Exception as e:
        print("Error loading popular products:", e)

    print("\n" + "=" * 60)
    print("COLLABORATIVE FILTERING RECOMMENDATIONS")
    print("=" * 60)

    try:
        recommendations = recommend_collaborative(
            product_id,
            top_n=5
        )

        for i, product in enumerate(recommendations, start=1):
            print(f"{i}. {product}")

    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected error:", e)

    print("\n" + "=" * 60)
    print("CONTENT-BASED RECOMMENDATIONS")
    print("=" * 60)

    try:
        recommendations = recommend_content(
            product_id,
            top_n=5
        )

        for i, product in enumerate(recommendations, start=1):
            print(f"{i}. {product}")

    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    main()