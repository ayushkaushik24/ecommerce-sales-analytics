-- ====================================================================
-- E-Commerce Sales & Customer Behavior Analytics - SQL Queries
-- ====================================================================

USE sales_analytics;

-- 1. Total Revenue, Total Profit, and Order Summary
SELECT 
    ROUND(SUM(Sales), 2) AS total_revenue,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS profit_margin_pct,
    COUNT(DISTINCT Order_ID) AS total_orders
FROM sales_data;

-- 2. Category & Sub-Category Performance Analysis
SELECT 
    Category,
    Sub_Category,
    ROUND(SUM(Sales), 2) AS category_revenue,
    ROUND(SUM(Profit), 2) AS category_profit
FROM sales_data
GROUP BY Category, Sub_Category
ORDER BY category_profit DESC;

-- 3. Customer RFM Segmentation using SQL Window Functions
WITH Customer_RFM AS (
    SELECT 
        Customer_ID,
        DATEDIFF('2026-09-20', MAX(Order_Date)) AS recency,
        COUNT(DISTINCT Order_ID) AS frequency,
        ROUND(SUM(Sales), 2) AS monetary
    FROM sales_data
    GROUP BY Customer_ID
),
RFM_Scores AS (
    SELECT 
        Customer_ID,
        recency,
        frequency,
        monetary,
        NTILE(4) OVER (ORDER BY recency DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM Customer_RFM
)
SELECT 
    Customer_ID,
    recency,
    frequency,
    monetary,
    (r_score + f_score + m_score) AS rfm_total_score,
    CASE 
        WHEN (r_score + f_score + m_score) >= 10 THEN 'VIP / High Value'
        WHEN (r_score + f_score + m_score) BETWEEN 7 AND 9 THEN 'Loyal Customer'
        WHEN (r_score + f_score + m_score) BETWEEN 5 AND 6 THEN 'At Risk / Churn Risk'
        ELSE 'Lost Customer'
    END AS customer_segment
FROM RFM_Scores
ORDER BY rfm_total_score DESC;