# Project Intent & Contract

## What We Are Building

A LookML data model on top of a BigQuery e-commerce gold mart. The mart contains
pre-aggregated fact tables covering revenue, sales operations, customer segmentation,
product profitability, marketing attribution, shipping performance, and cart abandonment.

The goal is a Looker data model that lets business analysts explore these facts without
writing SQL — slicing revenue by channel, understanding customer CLV, tracking inventory
risk, and attributing marketing spend.

## Stack

- **Language / Framework:** LookML (Looker)
- **Data Warehouse:** Google BigQuery
- **Build Tool:** Looker IDE or lkml-tools for local validation

## Primary Data Sources

- **BigQuery project:** `gcs-automation-project`
- **Dataset:** `gold_marts`
- **Tables:** fct_finance_revenue, fct_sales_operations, fct_customer_segments,
  fct_product_profitability, fct_marketing_attribution, fct_shipping_analysis,
  fct_cart_abandonment, fct_daily_dashboard

## Key Entities / Domains

1. **Revenue** (`fct_finance_revenue`) — gross/net revenue, shipping revenue/cost/margin by date and channel
2. **Sales Operations** (`fct_sales_operations`) — per-product sales velocity, inventory risk, gross profit, return rate
3. **Customer Segments** (`fct_customer_segments`) — segment-level CLV, order value, total spend
4. **Product Profitability** (`fct_product_profitability`) — product-level margin and profitability metrics
5. **Marketing Attribution** (`fct_marketing_attribution`) — channel attribution, spend, and conversion metrics
6. **Shipping** (`fct_shipping_analysis`) — shipping performance, cost, and delivery metrics
7. **Cart Abandonment** (`fct_cart_abandonment`) — abandonment rate and recovery metrics
8. **Daily Dashboard** (`fct_daily_dashboard`) — pre-aggregated daily KPI rollup

## Definition of Done (V1 / Slice 01)

- [ ] One `.view.lkml` file for every table in `gold_marts`
- [ ] `models/gold_marts.model.lkml` with explores for each primary entity
- [ ] Every view has a `count` measure
- [ ] Sum/average measures on revenue, profit, and quantity columns
- [ ] Handoff log entry written with connection placeholder noted
- [ ] No hardcoded credentials in any LookML file

## Known Constraints

- Gold mart tables are already aggregated — no row-level customer or order IDs
- No joins between tables (each fact is independent at this grain)
- Looker connection name is a placeholder — operator must set it in Looker admin
- **BQ access fallback:** if `bq` CLI is unavailable, use `demo/schema/gold_marts.md`
  as the authoritative schema reference — do not invent column names
