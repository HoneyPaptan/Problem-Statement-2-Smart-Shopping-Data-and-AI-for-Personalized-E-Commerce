import sqlite3
import json
from datetime import datetime


class DatabaseManager:

    def __init__(self, db_path="database/recommendations.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create recommendations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            customer_id TEXT PRIMARY KEY,
            recommendations TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        conn.commit()
        conn.close()
        print("Database initialized successfully")

    def get_recommendations(self, customer_id):
        """Fetch recommendations for a customer if they exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT recommendations, timestamp FROM recommendations WHERE customer_id = ?",
            (customer_id, ))
        result = cursor.fetchone()
        conn.close()

        if result:
            recommendations = json.loads(result[0])
            timestamp = result[1]
            return recommendations, timestamp
        return None, None

    def save_recommendations(self, customer_id, recommendations):
        """Save or update recommendations for a customer."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Convert recommendations to JSON string
        recommendations_json = json.dumps(recommendations)

        # Insert or replace
        cursor.execute(
            "INSERT OR REPLACE INTO recommendations (customer_id, recommendations, timestamp) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (customer_id, recommendations_json))

        conn.commit()
        conn.close()
        print(f"Recommendations saved for customer {customer_id}")
