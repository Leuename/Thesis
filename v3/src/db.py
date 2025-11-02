import sqlite3
import threading
from typing import Optional, List, Tuple

DB_PATH = "captures.db"

class CaptureDB:
    def __init__(self):
        self.db_path = DB_PATH
        self.lock = threading.Lock()
        
        # Define limits
        self.packages_per_magazine = 20
        self.stripes_per_package = 10

        # Current state, will be populated by _init_state
        self.current_magazine_id: Optional[int] = None
        self.current_package_id: Optional[int] = None
        self.current_stripe_number: int = 0  # 0 means package is empty or non-existent

        # Initialize DB tables and then load the current state
        self.init_db()
        self._init_state()

    def init_db(self):
        """Initializes the database schema."""
        # Use a non-locked connection for setup
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                magazine_id INTEGER NOT NULL REFERENCES magazines(id) ON DELETE CASCADE,
                package_number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(magazine_id, package_number)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stripes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
                stripe_number INTEGER NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(package_id, stripe_number)
            )
        """)
        conn.commit()
        conn.close()

    def _init_state(self):
        """
        Queries the DB on startup to find the last write position.
        This allows the application to resume exactly where it left off.
        """
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30)
            cur = conn.cursor()
            try:
                # 1. Find the last-created magazine
                cur.execute("SELECT id FROM magazines ORDER BY id DESC LIMIT 1")
                mag_row = cur.fetchone()
                if mag_row is None:
                    # Database is completely empty
                    return  # All state variables are already None/0

                self.current_magazine_id = mag_row[0]

                # 2. Find how many packages are in this magazine
                cur.execute("SELECT COUNT(id) FROM packages WHERE magazine_id = ?", 
                            (self.current_magazine_id,))
                package_count = cur.fetchone()[0]

                if package_count == 0:
                    # Magazine exists but has no packages
                    return  # Ready to create package 1

                # 3. Find the last-created package in this magazine
                cur.execute("SELECT id FROM packages WHERE magazine_id = ? ORDER BY package_number DESC LIMIT 1",
                            (self.current_magazine_id,))
                pkg_row = cur.fetchone()
                if pkg_row is None:
                     # Should not happen if package_count > 0, but as a safeguard
                     return

                self.current_package_id = pkg_row[0]

                # 4. Find how many stripes are in this package
                cur.execute("SELECT COUNT(id) FROM stripes WHERE package_id = ?", 
                            (self.current_package_id,))
                stripe_count = cur.fetchone()[0]

                if stripe_count < self.stripes_per_package:
                    # Last package is not full, resume filling it
                    self.current_stripe_number = stripe_count
                else:
                    # Last package is full. We are ready for a new package.
                    self.current_package_id = None
                    self.current_stripe_number = 0

                    # 5. Check if that full package also filled the magazine
                    if package_count >= self.packages_per_magazine:
                        # Magazine is full. We are ready for a new magazine.
                        self.current_magazine_id = None
                        
            except Exception as e:
                print(f"Error initializing DB state: {e}")
                # Reset to be safe, will force creation of new magazine
                self.current_magazine_id = None
                self.current_package_id = None
                self.current_stripe_number = 0
            finally:
                cur.close()
                conn.close()

    def get_all_capture_data(self) -> List[Tuple]:
        """
        Fetches all captured data (magazines, packages, stripes)
        in a flat, joined structure for export.
        
        Returns:
            List of tuples, where each tuple is a row containing:
            (mag_id, operator, mag_from, mag_to, pkg_num, stripe_num, description)
        """
        print("Fetching all data for export...")
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30)
            cur = conn.cursor()
            try:
                # Corrected query without timestamp columns
                cur.execute("""
                    SELECT
                        m.id,
                        m.operator,
                        m.magazine_from,
                        m.magazine_to,
                        p.package_number,
                        s.stripe_number,
                        s.description
                    FROM magazines m
                    JOIN packages p ON m.id = p.magazine_id
                    JOIN stripes s ON p.id = s.package_id
                    ORDER BY m.id, p.package_number, s.stripe_number
                """)
                return cur.fetchall()
            except Exception as e:
                print(f"Error fetching data for export: {e}")
                return []
            finally:
                cur.close()
                conn.close()
                
    def add_stripe(self, description: str, operator: str = "default_operator", 
                   mag_from: str = "A", mag_to: str = "Z") -> Tuple[int, int, int]:
        """
        Adds a single stripe to the database, automatically handling the
        creation of new packages and magazines as limits are reached.
        
        This is the single, thread-safe entry point for adding data.

        Returns:
            Tuple[int, int, int]: (magazine_id, package_id, new_stripe_number)
        """
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30)
            cur = conn.cursor()
            conn.execute("PRAGMA foreign_keys = ON;")

            try:
                # --- NEW LOGIC: Check for session data mismatch ---
                if self.current_magazine_id is not None:
                    # A magazine is active. Check if its data matches the new data.
                    # This is a read-only query, so it's fine to run outside the transaction.
                    cur.execute("SELECT operator, magazine_from, magazine_to FROM magazines WHERE id = ?", 
                                (self.current_magazine_id,))
                    row = cur.fetchone()
                    if row:
                        old_operator, old_mag_from, old_mag_to = row
                        if (old_operator != operator or 
                            old_mag_from != mag_from or 
                            old_mag_to != mag_to):
                            # Data mismatch! User changed session info.
                            # Force a new magazine to be created.
                            print(f"--- Session data changed (from '{old_operator}' to '{operator}'). Forcing new magazine. ---")
                            self.current_magazine_id = None # This forces Step 1 to run
                            self.current_package_id = None
                            self.current_stripe_number = 0
                
                # --- End of new logic ---

                conn.execute("BEGIN") # Start transaction *after* the read-check

                # --- Step 1: Ensure current magazine exists ---
                if self.current_magazine_id is None:
                    # (This will now run if it's the first run, or if session data changed)
                    cur.execute("INSERT INTO magazines(operator, magazine_from, magazine_to) VALUES (?, ?, ?)",
                                (operator, mag_from, mag_to))
                    self.current_magazine_id = cur.lastrowid
                    self.current_package_id = None
                    self.current_stripe_number = 0
                    print(f"--- Created new Magazine {self.current_magazine_id} (Op: {operator}) ---")


                # --- Step 2: Ensure current package exists ---
                if self.current_package_id is None:
                    # Need to create a new package. First, check if magazine is full.
                    cur.execute("SELECT COUNT(id) FROM packages WHERE magazine_id = ?", 
                                (self.current_magazine_id,))
                    package_count = cur.fetchone()[0]

                    if package_count >= self.packages_per_magazine:
                        # Magazine is full! Create a new one.
                        # This also correctly uses the new session data
                        cur.execute("INSERT INTO magazines(operator, magazine_from, magazine_to) VALUES (?, ?, ?)",
                                    (operator, mag_from, mag_to))
                        self.current_magazine_id = cur.lastrowid
                        self.current_package_id = None
                        self.current_stripe_number = 0
                        package_count = 0  # Reset count for new mag
                        print(f"--- Magazine full. Created new Magazine {self.current_magazine_id} (Op: {operator}) ---")

                    # Create the new package
                    new_package_number = package_count + 1
                    cur.execute("INSERT INTO packages (magazine_id, package_number) VALUES (?, ?)",
                                (self.current_magazine_id, new_package_number))
                    self.current_package_id = cur.lastrowid
                    self.current_stripe_number = 0  # Reset for new package
                    print(f"--- Created new Package {self.current_package_id} (Num: {new_package_number}) in Mag {self.current_magazine_id} ---")


                # --- Step 3: Insert the new stripe ---
                new_stripe_number = self.current_stripe_number + 1
                
                cur.execute("""
                    INSERT INTO stripes (package_id, stripe_number, description)
                    VALUES (?, ?, ?)
                """, (self.current_package_id, new_stripe_number, description))
                
                self.current_stripe_number = new_stripe_number
                
                mag_id = self.current_magazine_id
                pkg_id = self.current_package_id
                stripe_num = self.current_stripe_number

                # --- Step 4: Check for package/magazine completion ---
                if self.current_stripe_number >= self.stripes_per_package:
                    print(f"--- Completed Package {self.current_package_id} ---")
                    self.current_package_id = None
                    self.current_stripe_number = 0
                    
                    cur.execute("SELECT COUNT(id) FROM packages WHERE magazine_id = ?", 
                                (self.current_magazine_id,))
                    final_package_count = cur.fetchone()[0]
                    
                    if final_package_count >= self.packages_per_magazine:
                        print(f"--- Completed Magazine {self.current_magazine_id} ---")
                        self.current_magazine_id = None

                conn.commit()
                return (mag_id, pkg_id, stripe_num)

            except Exception as e:
                conn.rollback()
                print(f"Transaction failed: {e}")
                raise
            finally:
                cur.close()
                conn.close()

# --- Example Usage (Sequential) ---
if __name__ == "__main__":
    print("--- Starting database test ---")
    db = CaptureDB()
    
    # Simulate adding 210 stripes (2 magazines, 1 package, 0 stripes)
    # This will create:
    # 1 Magazine
    # 20 Packages
    # 200 Stripes
    # ... then ...
    # 1 New Magazine
    # 1 New Package
    # 10 New Stripes
    
    total_stripes_to_add = (20 * 10) + (1 * 10) + 5 # 2 Magazines, 1 Package, 5 Stripes
    
    for i in range(1, total_stripes_to_add + 1):
        try:
            desc = f"Stripe Data {i}"
            mag_id, pkg_id, stripe_num = db.add_stripe(desc)
            print(f"Added Stripe {i}: (Mag: {mag_id}, Pkg: {pkg_id}, Stripe: {stripe_num})")
        except Exception as e:
            print(f"Failed to add stripe {i}: {e}")
            break

    print("\n--- Simulating application restart ---")
    # Create a new instance of the DB.
    # It should pick up exactly where the last one left off.
    db_restart = CaptureDB()
    print(f"Restarted DB state: MagID={db_restart.current_magazine_id}, PkgID={db_restart.current_package_id}, StripeNum={db_restart.current_stripe_number}")

    # Add 5 more stripes to complete the package
    for i in range(total_stripes_to_add + 1, total_stripes_to_add + 6):
        desc = f"Stripe Data {i}"
        mag_id, pkg_id, stripe_num = db_restart.add_stripe(desc)
        print(f"Added Stripe {i}: (Mag: {mag_id}, Pkg: {pkg_id}, Stripe: {stripe_num})")

    print(f"Final DB state: MagID={db_restart.current_magazine_id}, PkgID={db_restart.current_package_id}, StripeNum={db_restart.current_stripe_number}")
    print("--- Test complete ---")
    