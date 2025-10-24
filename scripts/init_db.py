"""
Initialize PENGUIN database
Creates all necessary tables
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from penguin.data.storage.database import db
from penguin.data.storage.models import Base


def main():
    """Initialize database"""
    print("=" * 70)
    print("PENGUIN Database Initialization")
    print("=" * 70)
    print()

    try:
        # Connect to database
        print(f"Connecting to database...")
        db.connect()
        print("Connected!")

        # Create tables
        print("\nCreating tables...")
        db.create_tables()

        print("\nDatabase initialized successfully!")
        print("\nTables created:")
        print("  - stocks (stock metadata)")
        print("  - data_points (time-series data)")
        print("  - signals (detected signals)")
        print("  - recommendations (AI recommendations)")
        print("  - collector_status (collector health tracking)")

        print("\nYou can now run: penguin collect <collector_name>")

    except Exception as e:
        print(f"\nError initializing database: {e}")
        print("\nMake sure PostgreSQL is running and DATABASE_URL is set correctly.")
        sys.exit(1)


if __name__ == '__main__':
    main()
