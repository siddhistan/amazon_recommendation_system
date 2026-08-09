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
```

---

## Pipeline

CSV → Data Quality → EDA → (Recommendation Models + SQL Pipeline) → Evaluation → CLI

---

## 1. Data Quality
- 568,454 rows, 10 cols | 256,059 users | 74,258 products | avg rating 4.18
- Missing: ProfileName (26), Summary (27) | 0 duplicates/invalid ratings/dates
- 5,859 repeated user-product pairs (kept, not treated as errors)

## 2. Exploratory Data Analysis (EDA)
- Notebook: `notebooks/analytics.ipynb` — covers distributions, activity, sparsity, trends

### Rating Distribution
- Strongly skewed positive: 63.88% 5-star, 78.07% are 4–5 star

### User/Product Activity
- Users: mean 2.22, median 1, max 448 reviews (highly skewed)
- Products: mean 7.66, median 2, max 913 reviews (long-tail)

## 3. Temporal Analysis
- Reviews grow sharply over time, peaking in 2011–2012 (198,659 in 2012 alone)
- Avg rating slightly declines in later years (4.39 → 4.12, 2007–2012)

## 4. Interaction Sparsity
- 99.997% sparse (568K observed vs. ~19B possible interactions)
- Min-5 filtering → 195,807 interactions, 22,692 users, 6,544 products

## 5. Recommendation Models
- **5.1 Popularity-based:** global baseline for cold-start/new users → `popularity_recommendations.csv`
- **5.2 Item-based Collaborative Filtering:** item-item similarity matrix, excludes input product from output, artifacts in `data/models/`
- **5.3 Content-Based:** TF-IDF + cosine similarity on review text → separate signal from CF

## 6. Weighted Product Ranking
- Combines rating + review volume (Bayesian-style formula) to avoid bias toward low-review high-rating products

## 7. SQL Analytics Pipeline
- ETL: CSV → `load_database.py` → SQLite → `analysis.sql` → `run_sql_analysis.py`
- Covers: rating distribution, active users/products, yearly trends, weighted ranking, etc.

## 8. Recommendation Evaluation
- Behavioral checks (no Precision@K/Recall@K — no ground-truth set)
- Both models return 5 unique, non-duplicate, non-self recommendations
- Collaborative: avg rating 4.23, avg reviews 169.24
- Content-Based: avg rating 4.19, avg reviews 116.44
- Jaccard overlap between models: 0.330

## 9. CLI App
- `python -m app.app` → enter Product ID → shows Popular / Collaborative / Content-Based results

## 10–11. Setup & Run

```bash
git clone <repo> && cd amazon_recommendation_system
python -m venv venv && source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

python -m src.data_quality
python -m src.load_database
python -m src.run_sql_analysis
python -m src.evaluation
python -m app.app
```

## 12. Key Insights
1. Strong positive-rating bias (63.88% 5-star)
2. Highly skewed user activity (median 1 review)
3. Highly skewed product activity (median 2 reviews)
4. Extreme sparsity (99.997%) → needs filtering
5. Review volume concentrated in 2011–2012
6. Rating reliability needs volume-weighting
7. Multiple recommendation strategies complement each other

## 13. Tech Stack
- **Analytics:** Python, Pandas, NumPy, Matplotlib, Jupyter
- **ML:** Scikit-learn, TF-IDF, Cosine Similarity, Item-based CF
- **Data/SQL:** SQLite, SQL, CSV, Pandas ETL
- **Persistence:** Pickle, CSV artifacts

## 14. Project Structure
- `app/` — CLI app
- `src/` — core logic (models, data quality, DB load, SQL, evaluation)
- `data/raw/`, `data/processed/`, `data/models/`, `data/recommendations/`
- `notebooks/` — EDA
- `sql/` — schema + queries

## 15. Limitations
- No dedicated product-name field (Product ID only)
- Cold-start issue for CF on new products
- No Precision@K/Recall@K (no held-out ground truth)
- Model artifacts need consistent environment
- Local-scale only, not distributed

## 16. Future Improvements
- Train/test temporal split, Precision@K, Recall@K, MAP, NDCG@K
- Hybrid CF + content-based model
- User personalization, better metadata
- Incremental updates, Spark/distributed processing
- Cloud storage, REST API, monitoring/auto data-quality checks

## 17. Summary
Full pipeline: Dataset → Data Quality → EDA → SQL/ETL → Recommendation Models (Popularity, CF, Content-Based) → Evaluation → Insights. Demonstrates end-to-end data preprocessing, analytics, SQL, classical ML, and recommendation-system evaluation skills.