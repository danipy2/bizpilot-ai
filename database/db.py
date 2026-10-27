"""
BizPilot AI — Database Manager
SQLite database for business data: inventory, sales, customers, and conversation history.
Includes seed data so the demo works out of the box.
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional

import config

DB_PATH = str(config.DB_PATH)


def get_connection() -> sqlite3.Connection:
    """Get a database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize database tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            sku TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            customer_name TEXT,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            tool_calls TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
        CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
        CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id);
    """)

    conn.commit()
    conn.close()


def seed_data() -> None:
    """Populate the database with realistic sample business data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # --- Seed Products ---
    products = [
        ("Laptop Dell Inspiron 15", "Electronics", 45000.00, 25, "ELEC-001", "15.6 inch, 8GB RAM, 256GB SSD"),
        ("Samsung Galaxy A54", "Electronics", 18500.00, 40, "ELEC-002", "6.4 inch, 128GB, 5G capable"),
        ("HP LaserJet Printer", "Electronics", 12000.00, 15, "ELEC-003", "Monochrome laser printer"),
        ("Office Desk Chair", "Furniture", 8500.00, 30, "FURN-001", "Ergonomic mesh back, adjustable height"),
        ("Standing Desk", "Furniture", 15000.00, 12, "FURN-002", "Electric height adjustable, 140cm"),
        ("Filing Cabinet", "Furniture", 4500.00, 20, "FURN-003", "3-drawer steel cabinet"),
        ("A4 Paper (5 Ream)", "Supplies", 850.00, 100, "SUP-001", "80gsm white paper, 500 sheets per ream"),
        ("Ballpoint Pen Box", "Supplies", 250.00, 200, "SUP-002", "Box of 50 blue pens"),
        ("Whiteboard Marker Set", "Supplies", 180.00, 150, "SUP-003", "4 colors, erasable"),
        ("USB-C Hub", "Accessories", 2500.00, 45, "ACC-001", "7-in-1 USB-C hub with HDMI"),
        ("Wireless Mouse", "Accessories", 800.00, 60, "ACC-002", "Ergonomic wireless mouse"),
        ("Monitor Stand", "Accessories", 3200.00, 18, "ACC-003", "Adjustable aluminum monitor riser"),
        ("Ethiopian Coffee (1kg)", "Beverages", 450.00, 80, "BEV-001", "Premium Yirgacheffe whole bean"),
        ("Bottled Water Case", "Beverages", 180.00, 120, "BEV-002", "24 bottles, 500ml each"),
        ("Notebook A5", "Supplies", 120.00, 300, "SUP-004", "Ruled notebook, 200 pages"),
    ]

    cursor.executemany(
        "INSERT INTO products (name, category, price, stock_quantity, sku, description) VALUES (?, ?, ?, ?, ?, ?)",
        products,
    )

    # --- Seed Customers ---
    customers = [
        ("Abebe Kebede", "abebe@example.com", "+251911234567", "Bole, Addis Ababa"),
        ("Sara Mohammed", "sara.m@example.com", "+251922345678", "Kazanchis, Addis Ababa"),
        ("Dawit Haile", "dawit.h@example.com", "+251933456789", "Piassa, Addis Ababa"),
        ("Tigist Alemu", "tigist@example.com", "+251944567890", "Megenagna, Addis Ababa"),
        ("Yonas Bekele", "yonas.b@example.com", "+251955678901", "CMC, Addis Ababa"),
        ("Meron Tadesse", "meron@example.com", "+251966789012", "Sarbet, Addis Ababa"),
    ]

    cursor.executemany(
        "INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?, ?)",
        customers,
    )

    # --- Seed Sales (last 30 days) ---
    customer_names = [c[0] for c in customers]
    rng = random.Random(42)  # Fixed seed for reproducible demo data
    sales = []
    for day_offset in range(30, 0, -1):
        # 2-5 sales per day
        num_sales = rng.randint(2, 5)
        sale_date = (datetime.now() - timedelta(days=day_offset)).strftime("%Y-%m-%d %H:%M:%S")
        for _ in range(num_sales):
            product_idx = rng.randint(0, len(products) - 1)
            product = products[product_idx]
            quantity = rng.randint(1, 5)
            unit_price = product[2]
            total = unit_price * quantity
            customer = rng.choice(customer_names)
            sales.append((product_idx + 1, quantity, unit_price, total, customer, sale_date))

    cursor.executemany(
        "INSERT INTO sales (product_id, quantity, unit_price, total_amount, customer_name, sale_date) VALUES (?, ?, ?, ?, ?, ?)",
        sales,
    )

    conn.commit()
    conn.close()


# --- Query Functions (used by agent tools) ---

def search_inventory(query: str = "", category: str = "") -> List[Dict]:
    """Search products by name or category."""
    conn = get_connection()
    cursor = conn.cursor()

    if query and category:
        cursor.execute(
            "SELECT * FROM products WHERE name LIKE ? AND category LIKE ?",
            (f"%{query}%", f"%{category}%"),
        )
    elif query:
        cursor.execute("SELECT * FROM products WHERE name LIKE ? OR sku LIKE ?", (f"%{query}%", f"%{query}%"))
    elif category:
        cursor.execute("SELECT * FROM products WHERE category LIKE ?", (f"%{category}%",))
    else:
        cursor.execute("SELECT * FROM products")

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_product_by_sku(sku: str) -> Optional[Dict]:
    """Get a single product by SKU."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_low_stock_products(threshold: int = 15) -> List[Dict]:
    """Get products with stock below threshold."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM products WHERE stock_quantity <= ? ORDER BY stock_quantity ASC",
        (threshold,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_sales_summary(days: int = 7) -> Dict:
    """Get sales summary for the last N days."""
    conn = get_connection()
    cursor = conn.cursor()

    date_filter = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Total revenue
    cursor.execute(
        "SELECT SUM(total_amount), COUNT(*) FROM sales WHERE sale_date >= ?",
        (date_filter,),
    )
    total_revenue, total_orders = cursor.fetchone()

    # Top products by revenue
    cursor.execute("""
        SELECT p.name, SUM(s.total_amount) as revenue, SUM(s.quantity) as units_sold
        FROM sales s JOIN products p ON s.product_id = p.id
        WHERE s.sale_date >= ?
        GROUP BY p.name
        ORDER BY revenue DESC
        LIMIT 5
    """, (date_filter,))
    top_products = [
        {"name": row[0], "revenue": row[1], "units_sold": row[2]}
        for row in cursor.fetchall()
    ]

    # Revenue by category
    cursor.execute("""
        SELECT p.category, SUM(s.total_amount) as revenue
        FROM sales s JOIN products p ON s.product_id = p.id
        WHERE s.sale_date >= ?
        GROUP BY p.category
        ORDER BY revenue DESC
    """, (date_filter,))
    by_category = [
        {"category": row[0], "revenue": row[1]}
        for row in cursor.fetchall()
    ]

    # Daily trend
    cursor.execute("""
        SELECT DATE(sale_date) as date, SUM(total_amount) as revenue, COUNT(*) as orders
        FROM sales WHERE sale_date >= ?
        GROUP BY DATE(sale_date)
        ORDER BY date
    """, (date_filter,))
    daily_trend = [
        {"date": row[0], "revenue": row[1], "orders": row[2]}
        for row in cursor.fetchall()
    ]

    conn.close()

    return {
        "period_days": days,
        "total_revenue": round(total_revenue or 0, 2),
        "total_orders": total_orders or 0,
        "average_order_value": round((total_revenue or 0) / max(total_orders or 1, 1), 2),
        "top_products": top_products,
        "revenue_by_category": by_category,
        "daily_trend": daily_trend,
    }


def get_customer_list() -> List[Dict]:
    """Get all customers."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# --- Conversation History ---

def save_message(session_id: str, role: str, content: str, tool_calls: str = None) -> None:
    """Save a conversation message."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (session_id, role, content, tool_calls) VALUES (?, ?, ?, ?)",
        (session_id, role, content, tool_calls),
    )
    conn.commit()
    conn.close()


def get_conversation_history(session_id: str, limit: int = 20) -> List[Dict]:
    """Get conversation history for a session."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content, created_at FROM conversations WHERE session_id = ? ORDER BY created_at ASC LIMIT ?",
        (session_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# Initialize and seed on import
init_db()
seed_data()
