connection: "your-looker-connection-name"  # TODO: set this in Looker admin

# Auto-discovered views from your-gcp-project.gold_marts
include: "../views/*.view.lkml"

# ---- Explores ----
# Each explore corresponds to one primary fact table.
# No joins at this grain — each fact is independently aggregated.

explore: fct_finance_revenue {
  label: "Revenue"
  description: "Gross and net revenue, shipping P&L by date and channel"
}

explore: fct_sales_operations {
  label: "Sales Operations"
  description: "Per-product sales velocity, inventory risk, gross profit, and return rate"
}

explore: fct_customer_segments {
  label: "Customer Segments"
  description: "Segment-level CLV, order value, and total spend"
}

explore: fct_product_profitability {
  label: "Product Profitability"
  description: "Product-level margin and profitability metrics"
}

explore: fct_marketing_attribution {
  label: "Marketing Attribution"
  description: "Channel attribution, spend, and conversion"
}

explore: fct_shipping_analysis {
  label: "Shipping"
  description: "Shipping performance, cost, and delivery metrics"
}

explore: fct_cart_abandonment {
  label: "Cart Abandonment"
  description: "Abandonment rate and recovery metrics"
}

explore: fct_daily_dashboard {
  label: "Daily Dashboard"
  description: "Pre-aggregated daily KPI rollup across the business"
}
