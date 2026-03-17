#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# query.sh — SQL Query Runner
# Execute SQL queries against SQLite, PostgreSQL, or MySQL databases.
#
# Usage:
#   ./query.sh "SELECT COUNT(*) FROM users"
#   ./query.sh --file queries/daily.sql
#   ./query.sh --file queries/export.sql --output data/export.csv
#   ./query.sh --db postgresql --host localhost --dbname analytics "SELECT * FROM users"
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Defaults
DB_TYPE="${DB_TYPE:-sqlite}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-}"
DB_USER="${DB_USER:-}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_FILE="${DB_FILE:-data/local.db}"
OUTPUT_FILE=""
SQL_FILE=""
SQL_QUERY=""

# ─── Usage ─────────────────────────────────────────────────────────────────────

usage() {
    echo -e "${CYAN}📊 SQL Query Runner${NC}"
    echo ""
    echo "Usage:"
    echo "  $0 [options] \"SQL QUERY\""
    echo ""
    echo "Options:"
    echo "  --db TYPE          Database type: sqlite, postgresql, mysql (default: sqlite)"
    echo "  --host HOST        Database host (default: localhost)"
    echo "  --port PORT        Database port (default: 5432)"
    echo "  --dbname NAME      Database name"
    echo "  --user USER        Database user"
    echo "  --password PASS    Database password"
    echo "  --file FILE        Read SQL from file"
    echo "  --output FILE      Save output to CSV file"
    echo "  --db-file FILE     SQLite database file (default: data/local.db)"
    echo "  --help             Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 \"SELECT COUNT(*) FROM users\""
    echo "  $0 --file queries/daily-report.sql"
    echo "  $0 --file queries/export.sql --output data/export.csv"
    echo "  $0 --db postgresql --dbname analytics \"SELECT * FROM users LIMIT 10\""
    echo ""
    echo "Environment Variables:"
    echo "  DB_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, DB_FILE"
}

# ─── Parse Arguments ──────────────────────────────────────────────────────────

while [[ $# -gt 0 ]]; do
    case $1 in
        --db)       DB_TYPE="$2"; shift 2 ;;
        --host)     DB_HOST="$2"; shift 2 ;;
        --port)     DB_PORT="$2"; shift 2 ;;
        --dbname)   DB_NAME="$2"; shift 2 ;;
        --user)     DB_USER="$2"; shift 2 ;;
        --password) DB_PASSWORD="$2"; shift 2 ;;
        --file)     SQL_FILE="$2"; shift 2 ;;
        --output)   OUTPUT_FILE="$2"; shift 2 ;;
        --db-file)  DB_FILE="$2"; shift 2 ;;
        --help)     usage; exit 0 ;;
        -*)         echo -e "${RED}Unknown option: $1${NC}"; usage; exit 1 ;;
        *)          SQL_QUERY="$1"; shift ;;
    esac
done

# ─── Get SQL Query ────────────────────────────────────────────────────────────

if [ -n "$SQL_FILE" ]; then
    if [ ! -f "$SQL_FILE" ]; then
        echo -e "${RED}ERROR: SQL file not found: $SQL_FILE${NC}"
        exit 1
    fi
    SQL_QUERY=$(cat "$SQL_FILE")
    echo -e "${CYAN}→ Reading query from $SQL_FILE${NC}"
fi

if [ -z "$SQL_QUERY" ]; then
    echo -e "${RED}ERROR: No SQL query provided${NC}"
    echo "Use: $0 \"SELECT ...\" or $0 --file query.sql"
    exit 1
fi

echo -e "${CYAN}→ Database: $DB_TYPE${NC}"

# ─── Execute Query ────────────────────────────────────────────────────────────

case "$DB_TYPE" in
    sqlite)
        if ! command -v sqlite3 &>/dev/null; then
            echo -e "${RED}ERROR: sqlite3 not installed${NC}"
            echo "Install: sudo apt-get install sqlite3  (Linux)"
            echo "         brew install sqlite3           (macOS)"
            exit 1
        fi

        if [ ! -f "$DB_FILE" ]; then
            echo -e "${YELLOW}WARNING: Database file not found: $DB_FILE${NC}"
            echo -e "${YELLOW}Creating new SQLite database...${NC}"
            mkdir -p "$(dirname "$DB_FILE")"
            touch "$DB_FILE"
        fi

        if [ -n "$OUTPUT_FILE" ]; then
            sqlite3 -header -csv "$DB_FILE" "$SQL_QUERY" > "$OUTPUT_FILE"
            echo -e "${GREEN}✓ Results saved to $OUTPUT_FILE${NC}"
        else
            sqlite3 -header -column "$DB_FILE" "$SQL_QUERY"
        fi
        ;;

    postgresql|postgres|pg)
        if ! command -v psql &>/dev/null; then
            echo -e "${RED}ERROR: psql not installed${NC}"
            echo "Install: sudo apt-get install postgresql-client  (Linux)"
            echo "         brew install postgresql                  (macOS)"
            exit 1
        fi

        PGPASSWORD="$DB_PASSWORD" psql \
            -h "$DB_HOST" \
            -p "$DB_PORT" \
            -U "$DB_USER" \
            -d "$DB_NAME" \
            ${OUTPUT_FILE:+--csv -o "$OUTPUT_FILE"} \
            -c "$SQL_QUERY"

        if [ -n "$OUTPUT_FILE" ]; then
            echo -e "${GREEN}✓ Results saved to $OUTPUT_FILE${NC}"
        fi
        ;;

    mysql)
        if ! command -v mysql &>/dev/null; then
            echo -e "${RED}ERROR: mysql client not installed${NC}"
            echo "Install: sudo apt-get install mysql-client  (Linux)"
            echo "         brew install mysql-client           (macOS)"
            exit 1
        fi

        mysql \
            -h "$DB_HOST" \
            -P "$DB_PORT" \
            -u "$DB_USER" \
            ${DB_PASSWORD:+-p"$DB_PASSWORD"} \
            "$DB_NAME" \
            -e "$SQL_QUERY" \
            ${OUTPUT_FILE:+| tee "$OUTPUT_FILE"}

        if [ -n "$OUTPUT_FILE" ]; then
            echo -e "${GREEN}✓ Results saved to $OUTPUT_FILE${NC}"
        fi
        ;;

    *)
        echo -e "${RED}ERROR: Unsupported database type: $DB_TYPE${NC}"
        echo "Supported: sqlite, postgresql, mysql"
        exit 1
        ;;
esac

echo -e "${GREEN}✓ Query executed successfully${NC}"
