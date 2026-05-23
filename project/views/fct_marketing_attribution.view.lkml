view: fct_marketing_attribution {
  sql_table_name: `gcs-automation-project.gold_marts.fct_marketing_attribution` ;;

  dimension: metric_date {
    type: date
    sql: ${TABLE}.metric_date ;;
  }

  dimension: channel {
    type: string
    sql: ${TABLE}.channel ;;
  }

  dimension: recovered_orders {
    type: number
    sql: ${TABLE}.recovered_orders ;;
  }

  dimension: total_orders {
    type: number
    sql: ${TABLE}.total_orders ;;
  }

  dimension: abandoned_carts {
    type: number
    sql: ${TABLE}.abandoned_carts ;;
  }

  dimension: converted_carts {
    type: number
    sql: ${TABLE}.converted_carts ;;
  }

  dimension: abandoned_value {
    type: number
    sql: ${TABLE}.abandoned_value ;;
  }

  dimension: avg_time_to_purchase_hours {
    type: number
    sql: ${TABLE}.avg_time_to_purchase_hours ;;
  }

  dimension: at_risk_customers {
    type: number
    sql: ${TABLE}.at_risk_customers ;;
  }

  dimension: total_customers {
    type: number
    sql: ${TABLE}.total_customers ;;
  }

  measure: count {
    type: count
  }
}
