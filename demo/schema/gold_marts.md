# Schema Reference — your-gcp-project.gold_marts

Source: BigQuery dataset `your-gcp-project.gold_marts`
Domain: E-commerce (orders, revenue, shipping, customers, marketing)

All 8 tables are independently aggregated gold-layer fact tables. No FK joins exist between them at this grain.

---

## fct_finance_revenue

| Column | BQ Type | Notes |
|---|---|---|
| order_date | DATE | |
| order_channel | STRING | e.g. web, mobile, marketplace |
| gross_revenue | FLOAT | |
| net_revenue | FLOAT | |
| shipping_revenue | FLOAT | |
| shipping_cost | FLOAT | |
| shipping_margin | FLOAT | gross - cost |

---

## fct_sales_operations

| Column | BQ Type | Notes |
|---|---|---|
| product_id | STRING | |
| order_date | DATE | |
| sales_velocity_7d | FLOAT | rolling 7-day units/day |
| trend_signal | STRING | e.g. rising, flat, declining |
| inventory_quantity | FLOAT | |
| inventory_risk_tier | STRING | e.g. low, medium, high |
| gross_profit | FLOAT | |
| net_margin | FLOAT | |
| return_rate | FLOAT | 0–1 ratio |

---

## fct_customer_segments

| Column | BQ Type | Notes |
|---|---|---|
| customer_segment | STRING | e.g. Champions, At Risk |
| predicted_clv_bucket | STRING | e.g. High, Medium, Low |
| actual_clv_bucket | STRING | |
| customer_count | INTEGER | |
| avg_net_clv | FLOAT | |
| avg_order_value | FLOAT | |
| avg_total_spent | FLOAT | |

---

## fct_product_profitability

| Column | BQ Type | Notes |
|---|---|---|
| product_id | STRING | |
| product_date | DATE | |
| units_sold | INTEGER | |
| units_returned | INTEGER | |
| gross_revenue | FLOAT | |
| net_revenue | FLOAT | |
| gross_profit | FLOAT | |
| net_margin | FLOAT | |
| return_rate | FLOAT | 0–1 ratio |
| margin_pct | FLOAT | 0–1 ratio |

---

## fct_marketing_attribution

| Column | BQ Type | Notes |
|---|---|---|
| metric_date | DATE | |
| channel | STRING | e.g. email, paid_search, organic |
| recovered_orders | INTEGER | cart recovery attribution |
| total_orders | INTEGER | |
| abandoned_carts | INTEGER | |
| converted_carts | INTEGER | |
| abandoned_value | FLOAT | revenue at risk |
| avg_time_to_purchase_hours | FLOAT | |
| at_risk_customers | INTEGER | |
| total_customers | INTEGER | |

---

## fct_shipping_analysis

| Column | BQ Type | Notes |
|---|---|---|
| order_date | DATE | |
| order_channel | STRING | |
| shipping_speed | STRING | e.g. standard, express, overnight |
| orders | INTEGER | |
| shipping_revenue | FLOAT | |
| shipping_cost | FLOAT | |
| shipping_margin | FLOAT | |
| shipping_margin_pct | FLOAT | 0–1 ratio |

---

## fct_cart_abandonment

| Column | BQ Type | Notes |
|---|---|---|
| cart_date | DATE | |
| channel | STRING | |
| total_carts | INTEGER | |
| abandoned_carts | INTEGER | |
| converted_carts | INTEGER | |
| conversion_rate | FLOAT | 0–1 ratio |
| abandoned_value | FLOAT | |
| avg_time_to_purchase_hours | FLOAT | |

---

## fct_daily_dashboard

KPI rollup across all domains. One row per day.

| Column | BQ Type | Notes |
|---|---|---|
| metric_date | DATE | |
| orders_count | INTEGER | |
| gross_revenue | FLOAT | |
| net_revenue | FLOAT | |
| avg_order_value | FLOAT | |
| carts_created | INTEGER | |
| cart_conversion_rate | FLOAT | 0–1 ratio |
| returns_count | INTEGER | |
| return_rate | FLOAT | 0–1 ratio |
| refund_total | FLOAT | |
| revenue_7d_avg | FLOAT | rolling average |
| revenue_30d_avg | FLOAT | rolling average |
| revenue_30d_std | FLOAT | rolling std dev |
| revenue_anomaly_flag | BOOLEAN | true = statistical outlier |

---

## fct_promotions

Promotional campaign performance. One row per promotion per channel.

| Column | BQ Type | Notes |
|---|---|---|
| promotion_id | STRING | |
| promotion_name | STRING | |
| start_date | DATE | |
| end_date | DATE | |
| channel | STRING | e.g. email, social, display |
| discount_type | STRING | e.g. percentage, flat |
| discount_value | FLOAT | |
| orders_attributed | INTEGER | |
| revenue_attributed | FLOAT | |
| cost | FLOAT | |
| roas | FLOAT | revenue / cost |
