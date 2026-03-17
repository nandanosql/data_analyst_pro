# Data Sources Configuration

Configure your data sources below. The analysis scripts will use these settings.

---

## Databases

### Primary Database
- **Type:** `sqlite` | `postgresql` | `mysql`
- **Connection:** `sqlite:///data/local.db`
- **Notes:** Default is SQLite for local analysis

### Secondary Database (Optional)
- **Type:** `[database type]`
- **Connection:** `[connection string]`
- **Notes:** `[any notes]`

---

## File Sources

### Local Files
- **Directory:** `./data/`
- **Formats:** CSV, Excel (.xlsx, .xls), JSON, Parquet
- **Encoding:** UTF-8 (default)

### Remote Files (Optional)
- **Google Sheets:** `[URL]`
- **S3 Bucket:** `[s3://bucket/path]`
- **API Endpoint:** `[URL]`

---

## Data Warehouse (Optional)

- **Platform:** `[BigQuery / Snowflake / Redshift]`
- **Project/Account:** `[identifier]`
- **Dataset/Schema:** `[name]`
- **Credentials:** `[path to service account / env var]`

---

## Environment Variables

Set these in your shell or `.env` file:

```bash
# Database
export DB_TYPE="sqlite"
export DB_CONNECTION="sqlite:///data/local.db"

# Optional: PostgreSQL
# export DB_TYPE="postgresql"
# export DB_HOST="localhost"
# export DB_PORT="5432"
# export DB_NAME="analytics"
# export DB_USER="analyst"
# export DB_PASSWORD="your-password"

# Optional: Data warehouse
# export BQ_PROJECT="my-project"
# export BQ_DATASET="analytics"
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

---

## Output Configuration

- **Reports Directory:** `./reports/`
- **Charts Directory:** `./output/charts/`
- **Cleaned Data:** `./output/cleaned/`
- **Default Chart DPI:** `150`
- **Default Chart Format:** `png`
