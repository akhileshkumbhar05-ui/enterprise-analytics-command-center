# Power BI Model Relationships

## Model Style

Use a star-schema model.

Facts:

- `fact_order_items`
- `fact_orders`
- `fact_customer_cohorts`
- `fact_sessions`
- `ecommerce_quality_checks`

Dimensions:

- `dim_date`
- `dim_customer`
- `dim_product`

## Recommended Relationship Settings

Use:

- Cardinality: Many-to-one
- Cross filter direction: Single
- Active relationship: Yes, unless noted otherwise

## Core Relationships

Create these first:

| From Fact Table | From Column | To Dimension Table | To Column | Active |
|---|---|---|---|---|
| `fact_order_items` | `order_item_created_date` | `dim_date` | `date_day` | Yes |
| `fact_orders` | `order_created_date` | `dim_date` | `date_day` | Yes |
| `fact_sessions` | `session_date` | `dim_date` | `date_day` | Yes |
| `fact_order_items` | `customer_id` | `dim_customer` | `customer_id` | Yes |
| `fact_orders` | `customer_id` | `dim_customer` | `customer_id` | Yes |
| `fact_sessions` | `customer_id` | `dim_customer` | `customer_id` | Yes |
| `fact_order_items` | `product_id` | `dim_product` | `product_id` | Yes |

## Cohort Relationships

For the first version, you can leave `fact_customer_cohorts` disconnected and build cohort visuals directly from its own fields:

- `cohort_month`
- `months_since_first_purchase`
- `active_customers`
- `orders`
- `net_revenue_amount`

Later, we can add a month-level date dimension or create controlled relationships for cohort month and order month.

## Quality Table

For the first version, keep `ecommerce_quality_checks` disconnected.

Use it directly on the Data Quality page.

## Important Modeling Choices

Do not create a relationship between `fact_orders` and `fact_order_items` for the first version.

Reason:

- Both are fact tables.
- Fact-to-fact relationships can create confusing filters.
- Use `fact_order_items` for product/category revenue.
- Use `fact_orders` for order-level lifecycle metrics.

## Date Table

In Power BI, mark `dim_date` as the date table:

```text
Table tools > Mark as date table > date_day
```

Also consider turning off Auto date/time:

```text
File > Options and settings > Options > Current File > Data Load > Auto date/time
```

