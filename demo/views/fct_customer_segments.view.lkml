view: fct_customer_segments {
  sql_table_name: `your-gcp-project.gold_marts.fct_customer_segments` ;;

  dimension: customer_segment {
    type: string
    sql: ${TABLE}.customer_segment ;;
  }

  dimension: predicted_clv_bucket {
    type: string
    sql: ${TABLE}.predicted_clv_bucket ;;
  }

  dimension: actual_clv_bucket {
    type: string
    sql: ${TABLE}.actual_clv_bucket ;;
  }

  dimension: customer_count {
    type: number
    sql: ${TABLE}.customer_count ;;
  }

  dimension: avg_net_clv {
    type: number
    sql: ${TABLE}.avg_net_clv ;;
  }

  dimension: avg_order_value {
    type: number
    sql: ${TABLE}.avg_order_value ;;
  }

  dimension: avg_total_spent {
    type: number
    sql: ${TABLE}.avg_total_spent ;;
  }

  measure: count {
    type: count
  }
}
