connection: "your-looker-connection-name"

include: "/views/*.view.lkml"

explore: fct_finance_revenue {
  label: "Finance Revenue"
  description: "Revenue by channel and date — gross, net, and shipping breakdown."
}

explore: fct_sales_operations {
  label: "Sales Operations"
  description: "Product-level sales velocity, inventory risk, and profitability."
}

explore: fct_customer_segments {
  label: "Customer Segments"
  description: "Customer lifecycle segments, CLV buckets, and spend behavior."
}

explore: fct_product_profitability {
  label: "Product Profitability"
  description: "Unit economics per product — revenue, margin, and return rates."
}

explore: fct_marketing_attribution {
  label: "Marketing Attribution"
  description: "Channel-level attribution, cart recovery, and time-to-purchase."
}

explore: fct_shipping_analysis {
  label: "Shipping Analysis"
  description: "Shipping speed, cost, revenue, and margin by channel."
}

explore: fct_cart_abandonment {
  label: "Cart Abandonment"
  description: "Cart conversion rates, abandoned value, and recovery metrics."
}

explore: fct_daily_dashboard {
  label: "Daily Dashboard"
  description: "Daily KPI rollup across all domains — revenue, orders, returns."
}

explore: fct_promotions {
  label: "Promotions"
  description: "Promotional campaign performance — attribution, ROAS, and revenue by channel."
}
