from __future__ import annotations
import shutil
from datetime import datetime
from pathlib import Path

from GaitSharing_config import DATA_DIR
from GaitSharing_parser  import find_report_pdf, extract_text_from_pdf, parse_pdf_fields

def _import_one(folder: Path, db, direct_mode: bool) -> str:
    """
    Import a single subject folder.
    Returns "imported" or "updated". Raises on failure.
    """
    pdf = find_report_pdf(folder)
    if pdf is None:
        raise ValueError("No qualifying PDF found in folder")

    raw_text = extract_text_from_pdf(pdf)
    fields   = parse_pdf_fields(raw_text)

    if direct_mode:
        dest     = folder
        pdf_dest = pdf
    else:
        dest = DATA_DIR / folder.name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(str(folder), str(dest))
        pdf_dest = dest / pdf.name

    existing = db.get_by_folder(folder.name)
    db.upsert_subject({
        "folder_name":   folder.name,
        "folder_path":   str(dest),
        "source_folder": str(folder),
        "pdf_path":      str(pdf_dest),
        "import_date":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "raw_pdf_text":  raw_text,
        **fields,
    })
    return "updated" if existing else "imported"

def import_dataset(
    dataset_folder: Path,
    db,
    progress_cb,
    done_cb,
    direct_mode: bool = False,
) -> None:
    """Scan *dataset_folder* and upsert ALL matching subjects into *db*."""
    subfolders = sorted(
        [p for p in dataset_folder.iterdir() if p.is_dir()],
        key=lambda p: p.name,
    )
    total    = len(subfolders)
    imported = updated = skipped = 0
    failed: list[tuple[str, str]] = []

    for i, folder in enumerate(subfolders):
        progress_cb(i, total, folder.name)
        pdf = find_report_pdf(folder)
        if pdf is None:
            skipped += 1
            continue
        try:
            result = _import_one(folder, db, direct_mode)
            if result == "updated":
                updated += 1
            else:
                imported += 1
        except Exception as exc:
            failed.append((folder.name, str(exc)))

    progress_cb(total, total, "Done")
    done_cb(imported, updated, skipped, failed)

def import_selected_folders(
    folder_paths: list[Path],
    db,
    progress_cb,
    done_cb,
    direct_mode: bool = False,
) -> None:
    """Import a specific list of subject folder Paths."""
    total    = len(folder_paths)
    imported = updated = skipped = 0
    failed: list[tuple[str, str]] = []

    for i, folder in enumerate(folder_paths):
        progress_cb(i, total, folder.name)
        pdf = find_report_pdf(folder)
        if pdf is None:
            skipped += 1
            continue
        try:
            result = _import_one(folder, db, direct_mode)
            if result == "updated":
                updated += 1
            else:
                imported += 1
        except Exception as exc:
            failed.append((folder.name, str(exc)))

    progress_cb(total, total, "Done")
    done_cb(imported, updated, skipped, failed)

def sync_dataset(
    dataset_folder: Path,
    db,
) -> tuple[list[Path], list[str]]:
    """
    Compare *dataset_folder* subfolders against the database.
    Respects archived subjects (they are not considered "new").
    """
    # Fetch ALL names from db directly (including archived ones)
    cur = db.conn.execute("SELECT folder_name FROM subjects")
    db_names = {row[0] for row in cur.fetchall()}

    all_sub = sorted(
        [p for p in dataset_folder.iterdir() if p.is_dir()],
        key=lambda p: p.name,
    )
    source_names = {p.name for p in all_sub}

    # If it's in db_names (even if archived), it is NOT new.
    new_folders   = [p for p in all_sub  if p.name not in db_names]
    
    # We only want to flag active DB records as "deleted from source"
    active_records = db.get_all()
    active_names = {r["folder_name"] for r in active_records}
    deleted_names = [n for n in active_names if n not in source_names]

    return new_folders, deleted_names