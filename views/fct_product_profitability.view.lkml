view: fct_product_profitability {
  sql_table_name: `gcs-automation-project.gold_marts.fct_product_profitability` ;;

  dimension: product_id {
    type: string
    sql: ${TABLE}.product_id ;;
  }

  dimension: product_date {
    type: date
    sql: ${TABLE}.product_date ;;
  }

  dimension: units_sold {
    type: number
    sql: ${TABLE}.units_sold ;;
  }

  dimension: units_returned {
    type: number
    sql: ${TABLE}.units_returned ;;
  }

  dimension: gross_revenue {
    type: number
    sql: ${TABLE}.gross_revenue ;;
  }

  dimension: net_revenue {
    type: number
    sql: ${TABLE}.net_revenue ;;
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

  dimension: margin_pct {
    type: number
    sql: ${TABLE}.margin_pct ;;
  }

  measure: count {
    type: count
  }
}
