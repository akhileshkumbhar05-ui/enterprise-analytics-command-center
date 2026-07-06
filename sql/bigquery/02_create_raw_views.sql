-- Enterprise Analytics Command Center
-- Step 02: Create project-owned raw views over BigQuery public e-commerce data.

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_raw.users` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.users`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_raw.orders` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.orders`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_raw.order_items` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.order_items`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_raw.products` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.products`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_raw.inventory_items` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.inventory_items`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_raw.distribution_centers` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.distribution_centers`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_raw.events` AS
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.events`;

