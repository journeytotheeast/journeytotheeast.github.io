# Big Query basic

### Date-Partitioned tables
- A partitioned table is a table that is divided into segments, called partitions, that make it easier to manage and query your data. By dividing a large table into smaller partitions, you can improve query performance, and control costs by reducing the number of bytes read by a query.

- Scanning through the entire dataset every time to compare rows against a `WHERE` condition is wasteful. This is especially true if you only really care about records for a specific period of time like:
  - All transactions for the last year
  - All visitor interactions within the last 7 days
  - All products sold in the last month
- Instead of scanning the entire dataset and filtering on a date field -> ignore scanning records in certain partitions if they are irrelevant to our query.
- example:
```sql
#standardSQL  
 CREATE OR REPLACE TABLE covid_955.oxford_policy_tracker_197
 PARTITION BY date
 OPTIONS (
   partition_expiration_days=90,
   description="oxford policy tracker, partitioned by day"
 ) AS
 SELECT
   *
 FROM `bigquery-public-data.covid19_govt_response.oxford_policy_tracker`
 WHERE alpha_3_code NOT IN ("GBR", "BRA", "CAN", "USA")
```

### Create Auto-Expiring Partitioned table
- Auto-expiring partitioned tables are used to comply with data privacy statuses, and can be used to avoid unnecessary storage (which you'll be charged for in a production environment). If you want to create a rolling window of data, add an expiration date so the partition disappears after you're finished using it.
```sql
#standardSQL
 CREATE OR REPLACE TABLE ecommerce.days_with_rain
 PARTITION BY date
 OPTIONS (
   partition_expiration_days=60,
   description="weather stations with precipitation, partitioned by day"
 ) AS
 SELECT
   DATE(CAST(year AS INT64), CAST(mo AS INT64), CAST(da AS INT64)) AS date,
   (SELECT ANY_VALUE(name) FROM `bigquery-public-data.noaa_gsod.stations` AS stations
    WHERE stations.usaf = stn) AS station_name,  -- Stations may have multiple names
   prcp
 FROM `bigquery-public-data.noaa_gsod.gsod*` AS weather
 WHERE prcp < 99.9  -- Filter unknown values
   AND prcp > 0      -- Filter
   AND CAST(_TABLE_SUFFIX AS int64) >= 2018
```

### Solving Data Join Pitfalls
- Joining data tables can provide meaningful insight into your dataset. However, when you join your data, there are common pitfalls that could corrupt your results. Types of joins:
  - `Cross join`: combine each row of the first dataset with each row of the second dataset, where every combinations is represented in the output.
  - `Inner join`: requires that key values exist n both tables for the records to appear in the result table.
- Pitfall: non-unique key
- Join pitfall solution: use distinct SKUs before joining
```sql
SELECT
  productSKU,
  ARRAY_AGG(DISTINCT v2ProductName) AS push_all_names_into_array
FROM `data-to-insights.ecommerce.all_sessions_raw`
WHERE productSKU = 'GGOEGAAX0098'
GROUP BY productSKU
```

### Working with JSON, Array, Structs
- In traditional relational database, we would go normalization (going from one table to many tables). This is a common approach for transactional databases like MySql. For data warehousing, we often go denormalization, and bring many separate tables into one large reporting table.
- Create arrays:
```sql
SELECT
  fullVisitorId,
  date,
  ARRAY_AGG(DISTINCT v2ProductName) AS products_viewed,
  ARRAY_LENGTH(ARRAY_AGG(DISTINCT v2ProductName)) AS distinct_products_viewed,
  ARRAY_AGG(DISTINCT pageTitle) AS pages_viewed,
  ARRAY_LENGTH(ARRAY_AGG(DISTINCT pageTitle)) AS distinct_pages_viewed
  FROM `data-to-insights.ecommerce.all_sessions`
WHERE visitId = 1501570398
GROUP BY fullVisitorId, date
ORDER BY date
```
- Querying datasets that already have ARRAYs
  - We need to `UNNEST()` arrays to bring the array elements back into rows.
  - `UNNEST()` always follows the table name in your `FROM` clause (think of it conceptually like a pre-joined table)
```sql
SELECT DISTINCT
  visitId,
  h.page.pageTitle
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`,
UNNEST(hits) AS h
WHERE visitId = 1501570398
LIMIT 10
```

- `STRUCT`
  - a STRUCT can have:
    - one or many fields in it
    - the same or different data types for each field
    - it's own alias
  - The main advantages of having STRUCTs in a single table is it allows you to run queries like this one without do any JOINs:
```sql
SELECT
  visitId,
  totals.*,
  device.*
FROM `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
WHERE visitId = 1501570398
LIMIT 10
```
  - Note: The `.*` syntax tells BigQuery to return all fields for that STRUCT (much like it would if totals.* was separable table we joined against)

### Data Catalog Connectors
- sample:
```sh
#!/usr/bin/env bash
root_dir=$(pwd)
cd infrastructure/terraform

project=$(gcloud config get-value project)

test_machine_ip=$(curl https://myip.dnsomatic.com./)

if [ -z "$project" ]; then
    echo "GCloud project must be set! Run: gcloud config set project [MY_PROJECT]"
    exit 2
fi

# Create TF environment file
cat > .tfvars << EOF
project_id="$project"
test_machine_ip="$test_machine_ip"
EOF

echo -e "\033[1;42m [STEP 1] Enable required APIs \033[0m"

gcloud services enable datacatalog.googleapis.com sqladmin.googleapis.com --project $project

echo -e "\033[1;42m [STEP 2] Create Cloud SQL - SQLServer environment \033[0m"
# download utility tootls directly into ~/
curl http://stedolan.github.io/jq/download/linux64/jq -o ~/jq
# give it executable permissions
chmod a+x ~/jq

# Initialise the configuration
terraform init -input=false

# Plan and deploy
terraform plan -input=false -out=tfplan -var-file=".tfvars" > /dev/null 2>&1
terraform apply tfplan

public_ip_address=$(cat terraform.tfstate | jq '.outputs.public_ip_address.value')
username=$(cat terraform.tfstate | jq '.outputs.username.value')
password=$(cat terraform.tfstate | jq '.outputs.password.value')
database=$(cat terraform.tfstate | jq '.outputs.db_name.value')

# Remove quotes
public_ip_address=${public_ip_address//\"/}
username=${username//\"/}
password=${password//\"/}
database=${database//\"/}

export public_ip_address=$public_ip_address
export username=$username
export password=$password
export database=$database

if [ -z "$public_ip_address" ]; then
    echo "Cloud SQL instance creation failed"
    exit 3
fi

echo $public_ip_address $username $password

echo -e "\033[1;42m [STEP 3] POPULATE DATABASE \033[0m"

# Generate Metadata
docker run --rm --tty \
mesmacosta/sqlserver-metadata-generator:stable  \
--sqlserver-host=$public_ip_address \
--sqlserver-user=$username \
--sqlserver-pass=$password \
--sqlserver-database=$database \
--number-schemas=5 \
--number-tables=5

cd $root_dir
echo -e "\033[1;42m COMPLETED \033[0m"
```


- Challenges:
```sql
UPDATE
    covid_955.oxford_policy_tracker_197 t0
SET
    t0.mobility.avg_retail = t2.avg_retail,
    t0.mobility.avg_grocery = t2.avg_grocery,
    t0.mobility.avg_parks = t2.avg_parks,
    t0.mobility.avg_transit = t2.avg_transit,
    t0.mobility.avg_workplace = t2.avg_workplace,
    t0.mobility.avg_residential = t2.avg_residential
FROM
    (
      SELECT country_region, date,
      AVG(retail_and_recreation_percent_change_from_baseline) as avg_retail,
      AVG(grocery_and_pharmacy_percent_change_from_baseline)  as avg_grocery,
      AVG(parks_percent_change_from_baseline) as avg_parks,
      AVG(transit_stations_percent_change_from_baseline) as avg_transit,
      AVG( workplaces_percent_change_from_baseline ) as avg_workplace,
      AVG( residential_percent_change_from_baseline)  as avg_residential
      FROM `bigquery-public-data.covid19_google_mobility.mobility_report`
      GROUP BY country_region, date
    ) AS t2
WHERE t0.country_name = t2.country_region AND t0.date = t2.date;
```
