# Amazon Product Recommendation System

An end-to-end Amazon product recommendation and analytics system built using
Python, Pandas, SQL, and classical recommendation techniques.

The project processes 568K+ Amazon reviews, performs data-quality validation
and exploratory analysis, builds multiple recommendation approaches, and
evaluates their behavior using reproducible quality checks.

---

## Overview

The system uses Amazon product review data to generate product
recommendations using three complementary approaches:

1. Popularity-Based Recommendation
2. Item-Based Collaborative Filtering
3. Content-Based Filtering using TF-IDF and Cosine Similarity

The project was also extended with a data analytics and SQL pipeline to
analyze user behavior, product activity, rating patterns, temporal trends,
and user-product interaction sparsity.

### Dataset

The dataset contains:

- **568,454 reviews**
- **256,059 unique users**
- **74,258 unique products**
- **10 original columns**
- Average rating: **4.18**
- Rating range: **1–5**

---

## Project Architecture

```text
amazon_recommendation_system/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── Reviews.csv
│   │
│   ├── processed/
│   │
│   ├── models/
│   │   ├── product_ids.pkl
│   │   ├── item_similarity.pkl
│   │   ├── content_similarity.pkl
│   │   ├── tfidf_vectorizer.pkl
│   │   └── content_product_ids.pkl
│   │
│   └── recommendations/
│       └── popularity_recommendations.csv
│
├── notebooks/
│   └── analytics.ipynb
│
├── sql/
│   ├── schema.sql
│   └── analysis.sql
│
└── src/
    ├── collaborative_filtering.py
    ├── content_based.py
    ├── data_quality.py
    ├── evaluation.py
    ├── load_database.py
    ├── run_sql_analysis.py
    └── recommendation_engine.py

