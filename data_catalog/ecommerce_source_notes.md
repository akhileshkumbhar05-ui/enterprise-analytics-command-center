# E-commerce Source Notes

## Source

BigQuery public dataset:

```text
bigquery-public-data.thelook_ecommerce
```

Project-owned raw views:

```text
enterprise-analytics-cc.ecom_raw
```

## Source Tables Used

- `users`: customer profile and acquisition source.
- `orders`: order header, status, and lifecycle dates.
- `order_items`: item-level sales, product references, and item statuses.
- `products`: product, category, department, brand, cost, and retail price.
- `distribution_centers`: distribution center locations.
- `events`: website/session events for funnel analysis.

## Initial Source Profile From BigQuery

The first successful query returned:

- Orders: `124,866`
- Customers: `79,995`
- First order timestamp: `2019-01-09 14:22:25 UTC`
- Latest order timestamp: `2026-07-06 00:34:29.612237 UTC`

## Modeling Notes

- Raw layer is implemented as views over public tables to keep cost low.
- Staging layer standardizes names and date fields.
- Mart layer is materialized as tables for Power BI performance.
- Revenue calculations should clearly distinguish gross item sales from net revenue that excludes cancelled/returned items.
- Product cost is used as a margin proxy because this is a synthetic public dataset.

## Known Limitations

- TheLook is synthetic public data, so findings should be framed as portfolio/business-case insights rather than real company claims.
- The dataset may contain future-dated or dynamically generated records depending on the public table refresh.
- Marketing spend is not included, so CAC and ROAS require either a synthetic spend table or a separate source.

