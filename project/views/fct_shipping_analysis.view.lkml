view: fct_shipping_analysis {
  sql_table_name: `your-gcp-project.gold_marts.fct_shipping_analysis` ;;

  dimension: order_date {
    type: date
    sql: ${TABLE}.order_date ;;
  }

  dimension: order_channel {
    type: string
    sql: ${TABLE}.order_channel ;;
  }

  dimension: shipping_speed {
    type: string
    sql: ${TABLE}.shipping_speed ;;
  }

  dimension: orders {
    type: number
    sql: ${TABLE}.orders ;;
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

  dimension: shipping_margin_pct {
    type: number
    sql: ${TABLE}.shipping_margin_pct ;;
  }

  measure: count {
    type: count
  }
}
