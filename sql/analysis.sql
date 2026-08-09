-- ============================================================
-- AMAZON REVIEWS SQL ANALYSIS
-- ============================================================


-- ============================================================
-- 1. DATASET OVERVIEW
-- ============================================================

SELECT
    COUNT(*) AS total_reviews,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(DISTINCT product_id) AS unique_products,
    ROUND(AVG(score), 2) AS average_rating
FROM reviews;


-- ============================================================
-- 2. RATING DISTRIBUTION
-- ============================================================

SELECT
    score AS rating,
    COUNT(*) AS review_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM reviews),
        2
    ) AS percentage
FROM reviews
GROUP BY score
ORDER BY score;


-- ============================================================
-- 3. MOST ACTIVE USERS
-- ============================================================

SELECT
    user_id,
    COUNT(*) AS review_count
FROM reviews
GROUP BY user_id
ORDER BY review_count DESC
LIMIT 10;


-- ============================================================
-- 4. MOST REVIEWED PRODUCTS
-- ============================================================

SELECT
    product_id,
    COUNT(*) AS review_count
FROM reviews
GROUP BY product_id
ORDER BY review_count DESC
LIMIT 10;


-- ============================================================
-- 5. AVERAGE RATING BY PRODUCT
-- ============================================================

SELECT
    product_id,
    COUNT(*) AS review_count,
    ROUND(AVG(score), 2) AS average_rating
FROM reviews
GROUP BY product_id
HAVING COUNT(*) >= 20
ORDER BY average_rating DESC
LIMIT 10;


-- ============================================================
-- 6. REVIEW VOLUME BY YEAR
-- ============================================================

SELECT
    strftime(
        '%Y',
        datetime(review_time, 'unixepoch')
    ) AS review_year,
    COUNT(*) AS review_count
FROM reviews
GROUP BY review_year
ORDER BY review_year;


-- ============================================================
-- 7. AVERAGE RATING BY YEAR
-- ============================================================

SELECT
    strftime(
        '%Y',
        datetime(review_time, 'unixepoch')
    ) AS review_year,
    ROUND(AVG(score), 3) AS average_rating,
    COUNT(*) AS review_count
FROM reviews
GROUP BY review_year
ORDER BY review_year;


-- ============================================================
-- 8. HIGHLY RATED PRODUCTS WITH SUFFICIENT REVIEWS
-- ============================================================

SELECT
    product_id,
    COUNT(*) AS review_count,
    ROUND(AVG(score), 2) AS average_rating
FROM reviews
GROUP BY product_id
HAVING COUNT(*) >= 50
   AND AVG(score) >= 4.5
ORDER BY average_rating DESC, review_count DESC
LIMIT 20;


-- ============================================================
-- 9. LOW-RATED PRODUCTS WITH SUFFICIENT REVIEWS
-- ============================================================

SELECT
    product_id,
    COUNT(*) AS review_count,
    ROUND(AVG(score), 2) AS average_rating
FROM reviews
GROUP BY product_id
HAVING COUNT(*) >= 50
   AND AVG(score) <= 3.0
ORDER BY average_rating ASC, review_count DESC
LIMIT 20;


-- ============================================================
-- 10. REPEATED USER-PRODUCT INTERACTIONS
-- ============================================================

SELECT
    user_id,
    product_id,
    COUNT(*) AS interaction_count
FROM reviews
GROUP BY user_id, product_id
HAVING COUNT(*) > 1
ORDER BY interaction_count DESC
LIMIT 20;

-- ============================================================
-- 11. WEIGHTED PRODUCT RANKING
-- ============================================================
-- Combines product rating with review volume.
-- Products with very few reviews should not automatically
-- outrank products with substantial review history.

WITH product_stats AS (
    SELECT
        product_id,
        COUNT(*) AS review_count,
        AVG(score) AS average_rating
    FROM reviews
    GROUP BY product_id
),

global_stats AS (
    SELECT
        AVG(score) AS global_average_rating
    FROM reviews
)

SELECT
    p.product_id,
    p.review_count,
    ROUND(p.average_rating, 2) AS average_rating,

    ROUND(
        (
            (p.review_count * p.average_rating) +
            (10 * g.global_average_rating)
        )
        /
        (p.review_count + 10),
        3
    ) AS weighted_rating

FROM product_stats p
CROSS JOIN global_stats g

WHERE p.review_count >= 20

ORDER BY weighted_rating DESC
LIMIT 20;