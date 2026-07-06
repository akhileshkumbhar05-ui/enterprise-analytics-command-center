# E-commerce Power BI Measure Catalog

| Measure | Description | Grain | Draft Formula Logic |
|---|---|---|---|
| Total Revenue | Sum of completed order item revenue | Order item | Sum sale price for valid completed order items |
| Orders | Count of distinct orders | Order | Distinct count order IDs |
| Customers | Count of distinct customers | Customer | Distinct count user/customer IDs |
| Average Order Value | Revenue per order | Order | Total Revenue / Orders |
| New Customers | Customers with first order in selected period | Customer-month | Count customers where first order date is in period |
| Returning Customers | Customers ordering after first purchase | Customer-period | Count customers with prior purchase before period |
| Repeat Purchase Rate | Share of customers with more than one order | Customer | Customers with 2+ orders / total customers |
| Conversion Rate | Purchases divided by sessions or product views | Event/session | Purchase events / eligible starting events |
| Return Rate | Returned/cancelled items over ordered items | Order item | Returned or cancelled items / total items |
| Revenue MoM % | Month-over-month revenue change | Month | Current month revenue vs previous month revenue |
| Data Quality Pass Rate | Passed checks over total checks | Check run | Passed checks / total checks |

Each final measure should include:

- DAX expression.
- Source table.
- Business definition.
- Filters applied.
- Known limitations.

