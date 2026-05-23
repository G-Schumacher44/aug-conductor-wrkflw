view: fct_promotions {
  sql_table_name: `your-gcp-project.gold_marts.fct_promotions` ;;

  dimension: promotion_id {
    type: string
    sql: ${TABLE}.promotion_id ;;
  }

  dimension: promotion_name {
    type: string
    sql: ${TABLE}.promotion_name ;;
  }

  dimension: start_date {
    type: date
    sql: ${TABLE}.start_date ;;
  }

  dimension: end_date {
    type: date
    sql: ${TABLE}.end_date ;;
  }

  dimension: channel {
    type: string
    sql: ${TABLE}.channel ;;
  }

  dimension: discount_type {
    type: string
    sql: ${TABLE}.discount_type ;;
  }

  dimension: discount_value {
    type: number
    sql: ${TABLE}.discount_value ;;
  }

  dimension: orders_attributed {
    type: number
    sql: ${TABLE}.orders_attributed ;;
  }

  dimension: revenue_attributed {
    type: number
    sql: ${TABLE}.revenue_attributed ;;
  }

  dimension: cost {
    type: number
    sql: ${TABLE}.cost ;;
  }

  dimension: roas {
    type: number
    sql: ${TABLE}.roas ;;
  }

  measure: count {
    type: count
  }
}
