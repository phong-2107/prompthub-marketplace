#!/bin/bash
# =============================================
# Script setup Database PromptHub - Linux/macOS
# =============================================

set -e  # Exit on error

echo ""
echo "========================================"
echo "   SETUP DATABASE PROMPTHUB"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}[ERROR] Python not found! Please install Python first.${NC}"
    exit 1
fi

# Menu
echo "Chọn phương thức setup:"
echo ""
echo "1. Django Migrations (Khuyến nghị)"
echo "2. Import SQL trực tiếp"
echo "3. Reset database và setup lại"
echo ""

read -p "Nhập lựa chọn (1-3): " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}[INFO] Chạy Django migrations...${NC}"
        echo ""
        
        # Create migrations
        echo "[STEP 1/4] Creating migrations..."
        python manage.py makemigrations prompthub
        
        # Review migrations
        echo ""
        echo "[STEP 2/4] Reviewing migrations..."
        python manage.py showmigrations prompthub
        
        # Apply migrations
        echo ""
        echo "[STEP 3/4] Applying migrations..."
        python manage.py migrate prompthub
        
        # Import seed data
        echo ""
        read -p "Import dữ liệu mẫu? (y/n): " seed
        if [ "$seed" = "y" ] || [ "$seed" = "Y" ]; then
            echo "[STEP 4/4] Importing seed data..."
            python manage.py setup_prompthub_db --seed
        else
            echo "[STEP 4/4] Skipped seed data import"
        fi
        ;;
        
    2)
        echo ""
        echo -e "${GREEN}[INFO] Import SQL trực tiếp...${NC}"
        echo ""
        
        # Check psql
        if ! command -v psql &> /dev/null; then
            echo -e "${RED}[ERROR] psql not found! Please install PostgreSQL client.${NC}"
            exit 1
        fi
        
        # Get database credentials
        read -p "Database name (default: prompthub): " DB_NAME
        DB_NAME=${DB_NAME:-prompthub}
        
        read -p "Database user (default: postgres): " DB_USER
        DB_USER=${DB_USER:-postgres}
        
        read -p "Database host (default: localhost): " DB_HOST
        DB_HOST=${DB_HOST:-localhost}
        
        echo ""
        echo "[STEP 1/3] Creating database..."
        createdb -U $DB_USER -h $DB_HOST $DB_NAME || echo "Database may already exist"
        
        echo ""
        echo "[STEP 2/3] Importing schema..."
        psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f database/schema.sql
        
        echo ""
        read -p "Import dữ liệu mẫu? (y/n): " seed
        if [ "$seed" = "y" ] || [ "$seed" = "Y" ]; then
            echo "[STEP 3/3] Importing seed data..."
            psql -U $DB_USER -h $DB_HOST -d $DB_NAME -f database/seed_data.sql
        else
            echo "[STEP 3/3] Skipped seed data import"
        fi
        
        echo ""
        echo -e "${GREEN}[INFO] Đồng bộ Django với database...${NC}"
        python manage.py migrate --fake-initial
        ;;
        
    3)
        echo ""
        echo -e "${YELLOW}[WARNING] CẢNH BÁO: Thao tác này sẽ XÓA TẤT CẢ dữ liệu PromptHub!${NC}"
        echo ""
        read -p "Bạn có chắc chắn muốn tiếp tục? (yes/no): " confirm
        if [ "$confirm" != "yes" ]; then
            echo "Hủy thao tác."
            exit 0
        fi
        
        echo ""
        echo -e "${GREEN}[INFO] Resetting database...${NC}"
        python manage.py setup_prompthub_db --reset --seed
        ;;
        
    *)
        echo -e "${RED}[ERROR] Lựa chọn không hợp lệ!${NC}"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "   SETUP HOÀN THÀNH!"
echo "========================================"
echo ""
echo "Các bước tiếp theo:"
echo "1. Chạy development server: python manage.py runserver"
echo "2. Truy cập admin: http://localhost:8000/admin"
echo "3. Xem database guide: DATABASE_GUIDE.md"
echo ""
