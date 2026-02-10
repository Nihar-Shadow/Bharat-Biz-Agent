
import sqlite3
import os

DB_FILE = "smb_business.db"

def migrate():
    if not os.path.exists(DB_FILE):
        print("Database not found. Skipping migration (tables will be created fresh).")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "status" not in columns:
            print("Adding 'status' column to 'orders' table...")
            cursor.execute("ALTER TABLE orders ADD COLUMN status VARCHAR DEFAULT 'pending'")
            conn.commit()
            print("✅ Migration successful: 'status' column added.")
        else:
            print("ℹ️ 'status' column already exists.")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
