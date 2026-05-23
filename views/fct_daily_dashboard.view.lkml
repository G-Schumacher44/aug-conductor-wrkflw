view: fct_daily_dashboard {
  sql_table_name: `gcs-automation-project.gold_marts.fct_daily_dashboard` ;;

  dimension: metric_date {
    type: date
    sql: ${TABLE}.metric_date ;;
  }

  dimension: orders_count {
    type: number
    sql: ${TABLE}.orders_count ;;
  }

  dimension: gross_revenue {
    type: number
    sql: ${TABLE}.gross_revenue ;;
  }

  dimension: net_revenue {
    type: number
    sql: ${TABLE}.net_revenue ;;
  }

  dimension: avg_order_value {
    type: number
    sql: ${TABLE}.avg_order_value ;;
  }

  dimension: carts_created {
    type: number
    sql: ${TABLE}.carts_created ;;
  }

  dimension: cart_conversion_rate {
    type: number
    sql: ${TABLE}.cart_conversion_rate ;;
  }

  dimension: returns_count {
    type: number
    sql: ${TABLE}.returns_count ;;
  }

  dimension: return_rate {
    type: number
    sql: ${TABLE}.return_rate ;;
  }

  dimension: refund_total {
    type: number
    sql: ${TABLE}.refund_total ;;
  }

  dimension: revenue_7d_avg {
    type: number
    sql: ${TABLE}.revenue_7d_avg ;;
  }

  dimension: revenue_30d_avg {
    type: number
    sql: ${TABLE}.revenue_30d_avg ;;
  }

  dimension: revenue_30d_std {
    type: number
    sql: ${TABLE}.revenue_30d_std ;;
  }

  dimension: revenue_anomaly_flag {
    type: yesno
    sql: ${TABLE}.revenue_anomaly_flag ;;
  }

  measure: count {
    type: count
  }
}
