-- Enterprise Analytics Command Center
-- Step 03: Create standardized staging views.

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_staging.stg_users` AS
SELECT
  id AS customer_id,
  first_name,
  last_name,
  email,
  age,
  gender,
  country,
  state,
  city,
  postal_code,
  latitude,
  longitude,
  traffic_source,
  created_at AS customer_created_at,
  DATE(created_at) AS customer_created_date
FROM `enterprise-analytics-cc.ecom_raw.users`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_staging.stg_orders` AS
SELECT
  order_id,
  user_id AS customer_id,
  status AS order_status,
  gender AS customer_gender,
  created_at AS order_created_at,
  DATE(created_at) AS order_created_date,
  returned_at,
  DATE(returned_at) AS returned_date,
  shipped_at,
  DATE(shipped_at) AS shipped_date,
  delivered_at,
  DATE(delivered_at) AS delivered_date,
  num_of_item
FROM `enterprise-analytics-cc.ecom_raw.orders`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_staging.stg_order_items` AS
SELECT
  id AS order_item_id,
  order_id,
  user_id AS customer_id,
  product_id,
  inventory_item_id,
  status AS item_status,
  created_at AS order_item_created_at,
  DATE(created_at) AS order_item_created_date,
  shipped_at,
  DATE(shipped_at) AS shipped_date,
  delivered_at,
  DATE(delivered_at) AS delivered_date,
  returned_at,
  DATE(returned_at) AS returned_date,
  sale_price
FROM `enterprise-analytics-cc.ecom_raw.order_items`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_staging.stg_products` AS
SELECT
  id AS product_id,
  name AS product_name,
  brand,
  category,
  department,
  sku,
  cost,
  retail_price,
  distribution_center_id
FROM `enterprise-analytics-cc.ecom_raw.products`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_staging.stg_distribution_centers` AS
SELECT
  id AS distribution_center_id,
  name AS distribution_center_name,
  latitude AS distribution_center_latitude,
  longitude AS distribution_center_longitude
FROM `enterprise-analytics-cc.ecom_raw.distribution_centers`;

CREATE OR REPLACE VIEW `enterprise-analytics-cc.ecom_staging.stg_events` AS
SELECT
  id AS event_id,
  user_id AS customer_id,
  session_id,
  sequence_number,
  created_at AS event_created_at,
  DATE(created_at) AS event_created_date,
  ip_address,
  city,
  state,
  postal_code,
  browser,
  traffic_source,
  uri,
  event_type
FROM `enterprise-analytics-cc.ecom_raw.events`;

