import sqlite3
from datetime import datetime
from pathlib import Path
import threading


DB_PATH = "captures.db"
IMAGES_BASE = Path("images")


class CaptureDB:
    def __init__(self):
        self.db_path = DB_PATH
        self.images_base = IMAGES_BASE
        self.lock = threading.Lock()

    def init_db(self):
        conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operator TEXT NOT NULL,
                magazine_from TEXT NOT NULL,
                magazine_to TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                magazine_id INTEGER NOT NULL REFERENCES magazines(id) ON DELETE CASCADE,
                package_number INTEGER NOT NULL,
                UNIQUE(magazine_id, package_number)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stripes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
                stripe_number INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                description TEXT,
                saved_at TEXT NOT NULL,
                UNIQUE(package_id, stripe_number)
            )
        """)
        conn.commit()
        conn.close()

    def save_capture_set(self, operator, mag_from, mag_to, images_and_descriptions):
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
            conn.execute("PRAGMA foreign_keys = ON;")
            cur = conn.cursor()
            created_at = datetime.utcnow().isoformat()

            try:
                cur.execute("BEGIN")
                # Insert magazine
                cur.execute(
                    "INSERT INTO magazines(operator, magazine_from, magazine_to, created_at) VALUES (?, ?, ?, ?)",
                    (operator, mag_from, mag_to, created_at)
                )
                magazine_id = cur.lastrowid

                # Create 20 packages
                for package_num in range(1, 21):
                    cur.execute(
                        "INSERT INTO packages(magazine_id, package_number) VALUES (?, ?)",
                        (magazine_id, package_num)
                    )

                # Fetch packages to get their IDs
                cur.execute("SELECT id, package_number FROM packages WHERE magazine_id = ?", (magazine_id,))
                packages = {row[1]: row[0] for row in cur.fetchall()}

                # Insert stripes: map images (10 per package)
                inserts = []
                for idx, (img_bytes, desc) in enumerate(images_and_descriptions, start=1):
                    package_number = ((idx - 1) // 10) + 1
                    stripe_number = ((idx - 1) % 10) + 1

                    package_id = packages.get(package_number)
                    if package_id is None:
                        raise Exception(f"Package number {package_number} not found for magazine {magazine_id}")

                    # Save image file on disk
                    date_folder = datetime.utcnow().strftime("%Y-%m-%d")
                    capture_dir = self.images_base / date_folder / str(magazine_id) / f"package_{package_number}"
                    capture_dir.mkdir(parents=True, exist_ok=True)
                    filename = capture_dir / f"stripe_{stripe_number:02d}.jpg"
                    with open(filename, "wb") as f:
                        f.write(img_bytes)
                    inserts.append((
                        package_id,
                        stripe_number,
                        str(filename),
                        desc,
                        datetime.utcnow().isoformat()
                    ))

                cur.executemany(
                    "INSERT INTO stripes(package_id, stripe_number, file_path, description, saved_at) VALUES (?, ?, ?, ?, ?)",
                    inserts
                )

                cur.execute("COMMIT")
                return magazine_id

            except Exception:
                cur.execute("ROLLBACK")
                # Optional: Clean up files created before failure
                raise

            finally:
                cur.close()
                conn.close()


    def retrieve_capture_set(self, magazine_id):
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
            magazine = cur.fetchone()
            if not magazine:
                cur.close()
                conn.close()
                return None

            cur.execute("""
                SELECT p.id as package_id, p.package_number, s.id as stripe_id, s.stripe_number, s.file_path, s.description
                FROM packages p
                LEFT JOIN stripes s ON s.package_id = p.id
                WHERE p.magazine_id = ?
                ORDER BY p.package_number ASC, s.stripe_number ASC
            """, (magazine_id,))

            rows = cur.fetchall()

            cur.close()
            conn.close()

            # Organize data by packages and stripes
            packages = {}
            for row in rows:
                pnum = row['package_number']
                if pnum not in packages:
                    packages[pnum] = {
                        "package_id": row['package_id'],
                        "stripes": []
                    }
                if row['stripe_id'] is not None:
                    packages[pnum]["stripes"].append({
                        "stripe_id": row['stripe_id'],
                        "stripe_number": row['stripe_number'],
                        "file_path": row['file_path'],
                        "description": row['description'],
                    })

            return {
                "magazine": dict(magazine),
                "packages": packages
            }

    def delete_capture_set(self, magazine_id):
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON;")
            cur = conn.cursor()

            cur.execute("""
                SELECT s.file_path FROM stripes s
                JOIN packages p ON s.package_id = p.id
                WHERE p.magazine_id = ?
            """, (magazine_id,))
            files = cur.fetchall()

            try:
                cur.execute("BEGIN")
                cur.execute("DELETE FROM magazines WHERE id = ?", (magazine_id,))
                cur.execute("COMMIT")
            except Exception as e:
                cur.execute("ROLLBACK")
                cur.close()
                conn.close()
                raise e

            # Delete files
            for (file_path,) in files:
                try:
                    p = Path(file_path)
                    if p.exists():
                        p.unlink()
                except Exception:
                    pass

            # Optionally remove empty folders (not guaranteed)
            base_dir = self.images_base / datetime.utcnow().strftime("%Y-%m-%d") / str(magazine_id)
            try:
                if base_dir.exists() and not any(base_dir.iterdir()):
                    base_dir.rmdir()
            except Exception:
                pass

            cur.close()
            conn.close()

    def update_stripe_description(self, magazine_id, package_number, stripe_number, description):
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(
                "SELECT id FROM packages WHERE magazine_id = ? AND package_number = ?",
                (magazine_id, package_number)
            )
            row = cur.fetchone()
            if not row:
                cur.close()
                conn.close()
                raise Exception(f"Package {package_number} not found for magazine {magazine_id}")

            package_id = row[0]

            cur.execute(
                "UPDATE stripes SET description = ? WHERE package_id = ? AND stripe_number = ?",
                (description, package_id, stripe_number)
            )
            conn.commit()
            cur.close()
            conn.close()
