# DAX Measure Starter Pack

Create these measures in the `_Measures` table.

## Revenue and Profit

```DAX
Total Gross Revenue =
SUM ( fact_order_items[sale_price] )
```

```DAX
Total Net Revenue =
SUM ( fact_order_items[net_revenue_amount] )
```

```DAX
Total Net Cost =
SUM ( fact_order_items[net_cost_amount] )
```

```DAX
Total Net Profit =
[Total Net Revenue] - [Total Net Cost]
```

```DAX
Net Margin % =
DIVIDE ( [Total Net Profit], [Total Net Revenue] )
```

## Orders and Customers

```DAX
Orders =
DISTINCTCOUNT ( fact_order_items[order_id] )
```

```DAX
Order Items =
COUNTROWS ( fact_order_items )
```

```DAX
Customers =
DISTINCTCOUNT ( fact_order_items[customer_id] )
```

```DAX
Average Order Value =
DIVIDE ( [Total Net Revenue], [Orders] )
```

```DAX
Revenue Per Customer =
DIVIDE ( [Total Net Revenue], [Customers] )
```

## Returns and Cancellations

```DAX
Returned Items =
CALCULATE (
    COUNTROWS ( fact_order_items ),
    fact_order_items[is_returned] = TRUE ()
)
```

```DAX
Cancelled Items =
CALCULATE (
    COUNTROWS ( fact_order_items ),
    fact_order_items[is_cancelled] = TRUE ()
)
```

```DAX
Return Rate =
DIVIDE ( [Returned Items], [Order Items] )
```

```DAX
Cancellation Rate =
DIVIDE ( [Cancelled Items], [Order Items] )
```

## Sessions and Funnel

```DAX
Sessions =
DISTINCTCOUNT ( fact_sessions[session_id] )
```

```DAX
Sessions With Purchase =
CALCULATE (
    DISTINCTCOUNT ( fact_sessions[session_id] ),
    fact_sessions[has_purchase_event] = TRUE ()
)
```

```DAX
Session Conversion Rate =
DIVIDE ( [Sessions With Purchase], [Sessions] )
```

```DAX
Product Event Sessions =
CALCULATE (
    DISTINCTCOUNT ( fact_sessions[session_id] ),
    fact_sessions[product_events] > 0
)
```

```DAX
Cart Event Sessions =
CALCULATE (
    DISTINCTCOUNT ( fact_sessions[session_id] ),
    fact_sessions[cart_events] > 0
)
```

## Cohorts

```DAX
Cohort Active Customers =
SUM ( fact_customer_cohorts[active_customers] )
```

```DAX
Cohort Orders =
SUM ( fact_customer_cohorts[orders] )
```

```DAX
Cohort Revenue =
SUM ( fact_customer_cohorts[net_revenue_amount] )
```

```DAX
Cohort Size =
CALCULATE (
    [Cohort Active Customers],
    REMOVEFILTERS ( fact_customer_cohorts[months_since_first_purchase] ),
    fact_customer_cohorts[months_since_first_purchase] = 0
)
```

```DAX
Cohort Retention % =
DIVIDE ( [Cohort Active Customers], [Cohort Size] )
```

## Data Quality

```DAX
Quality Checks =
COUNTROWS ( ecommerce_quality_checks )
```

```DAX
Passed Quality Checks =
CALCULATE (
    COUNTROWS ( ecommerce_quality_checks ),
    ecommerce_quality_checks[check_status] = "PASS"
)
```

```DAX
Failed Quality Checks =
CALCULATE (
    COUNTROWS ( ecommerce_quality_checks ),
    ecommerce_quality_checks[check_status] = "FAIL"
)
```

```DAX
Data Quality Pass Rate =
DIVIDE ( [Passed Quality Checks], [Quality Checks] )
```

## Formatting

Format these as currency:

- `Total Gross Revenue`
- `Total Net Revenue`
- `Total Net Cost`
- `Total Net Profit`
- `Average Order Value`
- `Revenue Per Customer`
- `Cohort Revenue`

Format these as percentage:

- `Net Margin %`
- `Return Rate`
- `Cancellation Rate`
- `Session Conversion Rate`
- `Cohort Retention %`
- `Data Quality Pass Rate`

