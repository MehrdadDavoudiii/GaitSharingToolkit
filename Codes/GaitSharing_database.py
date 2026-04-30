from __future__ import annotations
import sqlite3, threading
from pathlib import Path
from datetime import datetime
from GaitSharing_config import DB_PATH

# Schema
SCHEMA = """
CREATE TABLE IF NOT EXISTS subjects (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    folder_name     TEXT    UNIQUE NOT NULL,
    folder_path     TEXT    NOT NULL,
    source_folder   TEXT,
    ganglabor_id    TEXT,
    last_name       TEXT,
    first_name      TEXT,
    birth_date      TEXT,
    gender          TEXT,
    diagnosis       TEXT,
    condition_left  TEXT,
    condition_right TEXT,
    measurements    TEXT,
    model           TEXT,
    exam_date       TEXT,
    pdf_path        TEXT,
    import_date     TEXT,
    raw_pdf_text    TEXT,
    is_archived     INTEGER DEFAULT 0
);
"""

COLS = [
    "id", "folder_name", "folder_path", "source_folder", "ganglabor_id",
    "last_name", "first_name", "birth_date", "gender",
    "diagnosis", "condition_left", "condition_right",
    "measurements", "model", "exam_date",
    "pdf_path", "import_date", "raw_pdf_text", "is_archived"
]

class Database:

    def __init__(self, path: Path = DB_PATH):
        self.path = str(path)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.executescript(SCHEMA)
        self._migrate()
        self._ensure_app_state()
        self.conn.commit()
        self._lock = threading.Lock()

    def _migrate(self) -> None:
        cur = self.conn.execute("PRAGMA table_info(subjects)")
        existing = {row[1] for row in cur.fetchall()}
        for col in COLS:
            if col not in existing and col not in ("id",):
                try:
                    if col == "is_archived":
                        self.conn.execute(f"ALTER TABLE subjects ADD COLUMN {col} INTEGER DEFAULT 0")
                    else:
                        self.conn.execute(f"ALTER TABLE subjects ADD COLUMN {col} TEXT")
                except Exception:
                    pass

    def _ensure_app_state(self) -> None:
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        self.conn.commit()

    def bump_version(self) -> None:
        ts = datetime.utcnow().isoformat()
        self.conn.execute(
            "INSERT OR REPLACE INTO app_state (key, value) VALUES ('data_version', ?)",
            (ts,)
        )
        self.conn.commit()

    def get_version(self) -> str:
        cur = self.conn.execute(
            "SELECT value FROM app_state WHERE key='data_version'"
        )
        row = cur.fetchone()
        return row[0] if row else ""         

    # backups
    def create_backup(self, backup_dir: Path) -> Path:
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"gait_dataset_backup_{timestamp}.db"
        
        with self._lock:
            bck = sqlite3.connect(str(backup_path))
            self.conn.backup(bck)
            bck.close()
            return backup_path

    # writes
    def upsert_subject(self, data: dict) -> int:
        with self._lock:
            cur  = self.conn.cursor()
            cols = [c for c in COLS[1:] if c in data and c != "is_archived"]
            vals = [data[c] for c in cols]
            ph   = ", ".join("?" * len(cols))
            
            # When updating, we ensure is_archived is reset to 0 in case an archived patient is re-imported
            upd  = ", ".join(f"{c}=excluded.{c}" for c in cols) + ", is_archived=0"
            
            cur.execute(
                f"INSERT INTO subjects ({', '.join(cols)}) VALUES ({ph}) "
                f"ON CONFLICT(folder_name) DO UPDATE SET {upd}",
                vals,
            )
            self.conn.commit()
            self.bump_version()
            return cur.lastrowid

    def update_subject(self, subject_id: int, data: dict) -> None:
        with self._lock:
            cols = [c for c in COLS[1:] if c in data and c not in ("folder_name", "is_archived")]
            vals = [data[c] for c in cols] + [subject_id]
            sets = ", ".join(f"{c}=?" for c in cols)
            self.conn.execute(f"UPDATE subjects SET {sets} WHERE id=?", vals)
            self.conn.commit()
            self.bump_version()

    def delete_subject(self, subject_id: int) -> None:
        with self._lock:
            self.conn.execute("DELETE FROM subjects WHERE id=?", (subject_id,))
            self.conn.commit()
            self.bump_version()

    def archive_subject(self, subject_id: int) -> None:
        with self._lock:
            self.conn.execute("UPDATE subjects SET is_archived = 1 WHERE id=?", (subject_id,))
            self.conn.commit()
            self.bump_version()

    # reads
    def get_all(self) -> list[dict]:
        cur = self.conn.execute("SELECT * FROM subjects WHERE is_archived = 0 ORDER BY folder_name")
        return [dict(zip(COLS, r)) for r in cur.fetchall()]

    def get_by_id(self, subject_id: int) -> dict | None:
        cur = self.conn.execute("SELECT * FROM subjects WHERE id=? AND is_archived = 0", (subject_id,))
        row = cur.fetchone()
        return dict(zip(COLS, row)) if row else None

    def get_by_folder(self, folder_name: str) -> dict | None:
        cur = self.conn.execute(
            "SELECT * FROM subjects WHERE folder_name=?", (folder_name,))
        row = cur.fetchone()
        return dict(zip(COLS, row)) if row else None

    def search(self, filters: dict, logic: str = "AND") -> list[dict]:
        """
        filters: {field: [kw1, kw2, …]}  — multiple kws = OR within field
        logic:   "AND" | "OR"            — between fields
        """
        if not filters:
            return self.get_all()

        field_clauses, params = [], []
        for field, keywords in filters.items():
            if not keywords:
                continue
            if field == "_date_from":
                field_clauses.append("exam_date >= ?"); params.append(keywords[0]); continue
            if field == "_date_to":
                field_clauses.append("exam_date <= ?"); params.append(keywords[0]); continue
            kw_parts = []
            for kw in keywords:
                kw_parts.append(f"({field} LIKE ? OR raw_pdf_text LIKE ?)")
                params += [f"%{kw}%", f"%{kw}%"]
            field_clauses.append("(" + " OR ".join(kw_parts) + ")")

        if not field_clauses:
            return self.get_all()

        joiner = " AND " if logic == "AND" else " OR "
        where  = f"({joiner.join(field_clauses)}) AND is_archived = 0"
        
        cur = self.conn.execute(
            f"SELECT * FROM subjects WHERE {where} ORDER BY folder_name", params)
        return [dict(zip(COLS, r)) for r in cur.fetchall()]

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM subjects WHERE is_archived = 0").fetchone()[0]

    def close(self) -> None:
        self.conn.close()
