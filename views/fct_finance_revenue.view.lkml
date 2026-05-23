view: fct_finance_revenue {
  sql_table_name: `gcs-automation-project.gold_marts.fct_finance_revenue` ;;

  dimension: order_date {
    type: date
    sql: ${TABLE}.order_date ;;
  }

  dimension: order_channel {
    type: string
    sql: ${TABLE}.order_channel ;;
  }

  dimension: gross_revenue {
    type: number
    sql: ${TABLE}.gross_revenue ;;
  }

  dimension: net_revenue {
    type: number
    sql: ${TABLE}.net_revenue ;;
  }

  dimension: shipping_revenue {
    type: number
    sql: ${TABLE}.shipping_revenue ;;
  }

  dimension: shipping_cost {
    type: number
    sql: ${TABLE}.shipping_cost ;;
  }

  dimension: shipping_margin {
    type: number
    sql: ${TABLE}.shipping_margin ;;
  }

  measure: count {
    type: count
  }
}
