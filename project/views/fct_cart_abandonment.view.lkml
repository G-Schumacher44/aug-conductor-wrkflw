view: fct_cart_abandonment {
  sql_table_name: `gcs-automation-project.gold_marts.fct_cart_abandonment` ;;

  dimension: cart_date {
    type: date
    sql: ${TABLE}.cart_date ;;
  }

  dimension: channel {
    type: string
    sql: ${TABLE}.channel ;;
  }

  dimension: total_carts {
    type: number
    sql: ${TABLE}.total_carts ;;
  }

  dimension: abandoned_carts {
    type: number
    sql: ${TABLE}.abandoned_carts ;;
  }

  dimension: converted_carts {
    type: number
    sql: ${TABLE}.converted_carts ;;
  }

  dimension: conversion_rate {
    type: number
    sql: ${TABLE}.conversion_rate ;;
  }

  dimension: abandoned_value {
    type: number
    sql: ${TABLE}.abandoned_value ;;
  }

  dimension: avg_time_to_purchase_hours {
    type: number
    sql: ${TABLE}.avg_time_to_purchase_hours ;;
  }

  measure: count {
    type: count
  }
}
