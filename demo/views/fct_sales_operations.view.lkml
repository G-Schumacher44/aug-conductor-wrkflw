view: fct_sales_operations {
  sql_table_name: `gcs-automation-project.gold_marts.fct_sales_operations` ;;

  dimension: product_id {
    type: string
    sql: ${TABLE}.product_id ;;
  }

  dimension: order_date {
    type: date
    sql: ${TABLE}.order_date ;;
  }

  dimension: sales_velocity_7d {
    type: number
    sql: ${TABLE}.sales_velocity_7d ;;
  }

  dimension: trend_signal {
    type: string
    sql: ${TABLE}.trend_signal ;;
  }

  dimension: inventory_quantity {
    type: number
    sql: ${TABLE}.inventory_quantity ;;
  }

  dimension: inventory_risk_tier {
    type: string
    sql: ${TABLE}.inventory_risk_tier ;;
  }

  dimension: gross_profit {
    type: number
    sql: ${TABLE}.gross_profit ;;
  }

  dimension: net_margin {
    type: number
    sql: ${TABLE}.net_margin ;;
  }

  dimension: return_rate {
    type: number
    sql: ${TABLE}.return_rate ;;
  }

  measure: count {
    type: count
  }
}
