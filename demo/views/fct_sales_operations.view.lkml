view: fct_sales_operations {
  sql_table_name: `gcs-automation-project.gold_marts.fct_sales_operations` ;;

  # ---- Dimensions ----

  dimension: product_id {
    type: string
    sql: ${TABLE}.product_id ;;
    primary_key: yes
    description: "Product identifier"
  }

  dimension: order_date {
    type: date
    datatype: date
    sql: ${TABLE}.order_date ;;
  }

  dimension: sales_velocity_7d {
    type: number
    sql: ${TABLE}.sales_velocity_7d ;;
    description: "Units sold in the last 7 days"
    value_format_name: decimal_1
  }

  dimension: trend_signal {
    type: string
    sql: ${TABLE}.trend_signal ;;
    description: "Trending direction: up, down, flat"
  }

  dimension: inventory_quantity {
    type: number
    sql: ${TABLE}.inventory_quantity ;;
    description: "Current inventory level"
  }

  dimension: inventory_risk_tier {
    type: string
    sql: ${TABLE}.inventory_risk_tier ;;
    description: "Risk tier: low, medium, high, critical"
  }

  dimension: gross_profit {
    type: number
    sql: ${TABLE}.gross_profit ;;
    value_format_name: usd
  }

  dimension: net_margin {
    type: number
    sql: ${TABLE}.net_margin ;;
    description: "Net margin as a decimal (e.g. 0.32 = 32%)"
    value_format_name: percent_2
  }

  dimension: return_rate {
    type: number
    sql: ${TABLE}.return_rate ;;
    description: "Return rate as a decimal"
    value_format_name: percent_2
  }

  # ---- Measures ----

  measure: count {
    type: count
    description: "Number of product-date records"
  }

  measure: total_inventory {
    type: sum
    sql: ${inventory_quantity} ;;
    description: "Total units in inventory"
  }

  measure: total_gross_profit {
    type: sum
    sql: ${gross_profit} ;;
    value_format_name: usd
  }

  measure: avg_sales_velocity_7d {
    type: average
    sql: ${sales_velocity_7d} ;;
    description: "Average 7-day sales velocity across products"
    value_format_name: decimal_1
  }

  measure: avg_net_margin {
    type: average
    sql: ${net_margin} ;;
    value_format_name: percent_2
  }

  measure: avg_return_rate {
    type: average
    sql: ${return_rate} ;;
    value_format_name: percent_2
  }
}
