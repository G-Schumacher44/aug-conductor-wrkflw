# Intent

BQ Project: your-gcp-project
Dataset: gold_marts
Schema reference: ../demo/schema/gold_marts.md

No live BQ or Looker access in this demo — use schema reference only.

## Entities

- fct_finance_revenue
- fct_sales_operations
- fct_customer_segments
- fct_product_profitability
- fct_marketing_attribution
- fct_shipping_analysis
- fct_cart_abandonment
- fct_daily_dashboard

## Modeling Goal

Production-ready LookML data model on top of 8 pre-aggregated BigQuery fact tables
covering an e-commerce business: revenue, sales ops, customer segments, product
profitability, marketing attribution, shipping, cart abandonment, and a daily KPI dashboard.

Done = all 8 tables have enriched views with typed measures, a clean model with
labeled explores, and the project validates in the Looker IDE when a connection
is provisioned.
