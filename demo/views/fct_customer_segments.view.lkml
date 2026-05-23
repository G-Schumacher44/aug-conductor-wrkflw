view: fct_customer_segments {
  sql_table_name: `gcs-automation-project.gold_marts.fct_customer_segments` ;;

  # ---- Dimensions ----

  dimension: customer_segment {
    type: string
    sql: ${TABLE}.customer_segment ;;
    description: "Customer segment label (e.g. VIP, At-Risk, New)"
  }

  dimension: predicted_clv_bucket {
    type: string
    sql: ${TABLE}.predicted_clv_bucket ;;
    description: "ML-predicted customer lifetime value bucket"
  }

  dimension: actual_clv_bucket {
    type: string
    sql: ${TABLE}.actual_clv_bucket ;;
    description: "Realized customer lifetime value bucket"
  }

  dimension: customer_count {
    type: number
    sql: ${TABLE}.customer_count ;;
    description: "Number of customers in this segment"
  }

  dimension: avg_net_clv {
    type: number
    sql: ${TABLE}.avg_net_clv ;;
    description: "Average net customer lifetime value"
    value_format_name: usd
  }

  dimension: avg_order_value {
    type: number
    sql: ${TABLE}.avg_order_value ;;
    value_format_name: usd
  }

  dimension: avg_total_spent {
    type: number
    sql: ${TABLE}.avg_total_spent ;;
    value_format_name: usd
  }

  # ---- Measures ----

  measure: count {
    type: count
    description: "Number of segment records"
  }

  measure: total_customers {
    type: sum
    sql: ${customer_count} ;;
    description: "Total customers across segments"
  }

  measure: avg_clv {
    type: average
    sql: ${avg_net_clv} ;;
    description: "Average net CLV across segments"
    value_format_name: usd
  }

  measure: avg_order_value_across_segments {
    type: average
    sql: ${avg_order_value} ;;
    value_format_name: usd
  }
}
