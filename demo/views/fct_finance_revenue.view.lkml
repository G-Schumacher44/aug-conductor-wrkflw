view: fct_finance_revenue {
  sql_table_name: `gcs-automation-project.gold_marts.fct_finance_revenue` ;;

  # ---- Dimensions ----

  dimension: order_date {
    type: date
    datatype: date
    sql: ${TABLE}.order_date ;;
    description: "Date of the order"
  }

  dimension: order_channel {
    type: string
    sql: ${TABLE}.order_channel ;;
    description: "Sales channel (e.g. web, mobile, marketplace)"
  }

  dimension: gross_revenue {
    type: number
    sql: ${TABLE}.gross_revenue ;;
    description: "Total revenue before deductions"
    value_format_name: usd
  }

  dimension: net_revenue {
    type: number
    sql: ${TABLE}.net_revenue ;;
    description: "Revenue after returns and discounts"
    value_format_name: usd
  }

  dimension: shipping_revenue {
    type: number
    sql: ${TABLE}.shipping_revenue ;;
    description: "Revenue collected for shipping"
    value_format_name: usd
  }

  dimension: shipping_cost {
    type: number
    sql: ${TABLE}.shipping_cost ;;
    description: "Actual cost of shipping"
    value_format_name: usd
  }

  dimension: shipping_margin {
    type: number
    sql: ${TABLE}.shipping_margin ;;
    description: "Shipping revenue minus shipping cost"
    value_format_name: usd
  }

  # ---- Measures ----

  measure: count {
    type: count
    description: "Number of revenue records"
  }

  measure: total_gross_revenue {
    type: sum
    sql: ${gross_revenue} ;;
    description: "Sum of gross revenue"
    value_format_name: usd
  }

  measure: total_net_revenue {
    type: sum
    sql: ${net_revenue} ;;
    description: "Sum of net revenue"
    value_format_name: usd
  }

  measure: total_shipping_revenue {
    type: sum
    sql: ${shipping_revenue} ;;
    value_format_name: usd
  }

  measure: total_shipping_cost {
    type: sum
    sql: ${shipping_cost} ;;
    value_format_name: usd
  }

  measure: total_shipping_margin {
    type: sum
    sql: ${shipping_margin} ;;
    value_format_name: usd
  }

  measure: avg_shipping_margin {
    type: average
    sql: ${shipping_margin} ;;
    description: "Average shipping margin per record"
    value_format_name: usd
  }
}
