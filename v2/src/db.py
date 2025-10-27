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
            CREATE TABLE IF NOT EXISTS capture_set (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operator TEXT NOT NULL,
                magazine_from TEXT NOT NULL,
                magazine_to TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS capture_image (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                capture_set_id INTEGER NOT NULL REFERENCES capture_set(id) ON DELETE CASCADE,
                image_index INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                description TEXT,
                saved_at TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save_capture_set(self, operator, mag_from, mag_to, images_and_descriptions):
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            cur = conn.cursor()
            created_at = datetime.utcnow().isoformat()
            try:
                cur.execute("BEGIN")
                cur.execute(
                    "INSERT INTO capture_set(operator, magazine_from, magazine_to, created_at) VALUES (?, ?, ?, ?)",
                    (operator, mag_from, mag_to, created_at)
                )
                capture_id = cur.lastrowid

                date_folder = datetime.utcnow().strftime("%Y-%m-%d")
                capture_dir = self.images_base / date_folder / str(capture_id)
                capture_dir.mkdir(parents=True, exist_ok=True)

                inserts = []
                for idx, (img_bytes, desc) in enumerate(images_and_descriptions, start=1):
                    filename = capture_dir / f"image_{idx:02d}.jpg"
                    with open(filename, "wb") as f:
                        f.write(img_bytes)
                    inserts.append((capture_id, idx, str(filename), desc, datetime.utcnow().isoformat()))

                cur.executemany(
                    "INSERT INTO capture_image(capture_set_id, image_index, file_path, description, saved_at) VALUES (?, ?, ?, ?, ?)",
                    inserts
                )

                cur.execute("COMMIT")
                return capture_id

            except Exception:
                cur.execute("ROLLBACK")
                if capture_dir.exists():
                    for f in capture_dir.iterdir():
                        try:
                            f.unlink()
                        except Exception:
                            pass
                    try:
                        capture_dir.rmdir()
                    except Exception:
                        pass
                raise

            finally:
                cur.close()
                conn.close()

    def retrieve_capture_set(self, capture_id):
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute("SELECT * FROM capture_set WHERE id = ?", (capture_id,))
            capture_set = cur.fetchone()
            if not capture_set:
                cur.close()
                conn.close()
                return None

            cur.execute("""
                SELECT image_index, file_path, description FROM capture_image
                WHERE capture_set_id = ? ORDER BY image_index ASC
            """, (capture_id,))
            images = cur.fetchall()

            cur.close()
            conn.close()

            return {
                "capture_set": dict(capture_set),
                "images": [dict(img) for img in images]
            }

    def delete_capture_set(self, capture_id):
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON;")
            cur = conn.cursor()

            cur.execute("SELECT file_path FROM capture_image WHERE capture_set_id = ?", (capture_id,))
            files = cur.fetchall()

            try:
                cur.execute("BEGIN")
                cur.execute("DELETE FROM capture_set WHERE id = ?", (capture_id,))
                cur.execute("COMMIT")
            except Exception as e:
                cur.execute("ROLLBACK")
                cur.close()
                conn.close()
                raise e

            for (file_path,) in files:
                try:
                    p = Path(file_path)
                    if p.exists():
                        p.unlink()
                except Exception:
                    pass

            if files:
                parent_dir = Path(files[0][0]).parent
                try:
                    if parent_dir.exists() and not any(parent_dir.iterdir()):
                        parent_dir.rmdir()
                except Exception:
                    pass

            cur.close()
            conn.close()
