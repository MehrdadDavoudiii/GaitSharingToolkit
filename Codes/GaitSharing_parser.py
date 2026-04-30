from __future__ import annotations
import re
from pathlib import Path

try:
    import fitz          # PyMuPDF
except ImportError:
    fitz = None

# Redaction terms (Anonymizer)
REDACTION_TERMS_DEFAULT: list[str] = [
    # English
    "Name","Last Name","Family Name","First Name","Middle Name",
    "Address","Street Address","City","State","Zip","County",
    "Date of Birth","birthdate","DOB","Age","Date of Admission",
    "Admission Date","Date of Discharge","Discharge Date",
    "Date of Death","Date Measured","Telephone Number","Phone",
    "Telephone","Fax Number","Fax","Email Address","Email",
    "Social Security Number","SSN","Medical Record Number","MRN",
    "Patient ID","Patient Number","Health Plan Beneficiary Number",
    "Member ID","Insurance ID","Account Number",
    "Certificate/License Number","Vehicle Identifier","License Plate",
    "Device Identifier","Serial Number","Sex","Gender",
    "Attending Physician","Referring Physician",
    
    # Deutsch & Swiss Region Specifics
    "Ganglabor ID", "BW:", "Datum", "Basel", "Schweiz", "spitalstrasse", "Spitalstrasse",
    "Nachname","Vorname","Adresse","Straße","Stadt","Ort","Land",
    "PLZ","Postleitzahl","Geburtsdatum","Geburtstag","Geb.","Alter",
    "Aufnahmedatum","Entlassungsdatum","Todesdatum","Messdatum",
    "Telefonnummer","Tel","Faxnummer","E-Mail",
    "Sozialversicherungsnummer","SV-Nummer","Patienten-ID",
    "Patientennummer","Krankenversicherungsnummer","Versichertennummer",
    "Kontonummer","Lizenznummer","Kennzeichen","Geräte-ID",
    "Seriennummer","Geschlecht","Behandelnder Arzt","Überweisender Arzt",
    "Arzt","Klinik","Krankenhaus",
    
    # Français
    "Nom","Nom de naissance","Nom de famille","Prénom","Rue","Ville",
    "Code Postal","Date de naissance","Né(e) le","Âge",
    "Date d'admission","Date d'entrée","Date de sortie",
    "Date de décès","Date de la mesure","Numéro de téléphone","Tél",
    "Numéro de fax","Adresse e-mail","Courriel",
    "Numéro de Sécurité Sociale","N° SS","N° Dossier","ID Patient",
    "Numéro d'assurance maladie","Numéro de compte","Numéro de licence",
    "Plaque d'immatriculation","Numéro de série","Sexe","Genre",
    "Médecin traitant","Médecin référent",
    
    # Italiano
    "Cognome","Nome","Indirizzo","Via","Città","CAP",
    "Data di nascita","Nato/a il","Età","Data di ammissione",
    "Data di dimissione","Data di morte","Data di misurazione",
    "Numero di telefono","Numero di fax","Indirizzo email",
    "Codice fiscale","Numero cartella clinica","ID paziente",
    "Numero assicurazione","Numero conto","Sesso","Genere",
    "Medico curante","Medico referente",
]

# Section headers — used to build the STOP lookahead
_SECTION_HEADERS: list[str] = [
    r"Diagnose",       r"Diagnosis",      r"Diagnostic",   r"Diagnosi",
    r"Messungen",      r"Measurements",   r"Mesures",      r"Misure",
    r"Bedingungen",    r"Conditions",     r"Condizioni",
    r"Modell?",        r"Model",          r"Mod[eè]le",    r"Modello",
    r"GMFCS",          r"FMS",
    r"Fragestellung",  r"Clinical\s+[Qq]uestion",
    r"Untersucher",    r"Examiner",       r"Examinateur",  r"Esaminatore",
    r"EMG",
    r"Ganglabor",      r"Gait\s*Lab",
    r"Geburtsdatum",   r"Date\s+of\s+Birth", r"Geschlecht", r"Gender",
    r"Datum",          r"Date",
]

_STOP = (
    r"(?=\n[ \t]*(?:"
    + "|".join(_SECTION_HEADERS)
    + r")\s*[:\s])"
)

# PDF filename patterns

_PDF_PRIORITY = re.compile(r"\b(CGM|PiG|FOM)\b", re.IGNORECASE)
_PDF_EXCLUDE = re.compile(r"\b(Comparison|Model)\b", re.IGNORECASE)

_PATIENT_FIELD_PAT = re.compile(
    r"(?:"
    r"Datum[:\s]|"
    r"Messungen[:\s]|"
    r"Bedingungen[:\s]|"
    r"Ganglabor\s*(?:ID|Nr)[:\s]|"
    r"Name\s*,\s*Vorname[:\s]|"
    r"Modell?[:\s]|"
    r"Geschlecht[:\s]|"
    r"Geburtsdatum[:\s]"
    r")",
    re.IGNORECASE,
)
_MIN_PATIENT_FIELDS = 3

# Field regex patterns
FIELD_PATTERNS: dict[str, list[str]] = {

    "ganglabor_id": [
        r"Gang(?:labor|lab)\s*(?:ID|Nr\.?|Number)[:\s]+([^\n\r]+)",
        r"Gait\s*Lab(?:oratory)?\s*(?:ID|Number)[:\s]+([^\n\r]+)",
        r"\b(v\d{4,6}[a-z])\b",
    ],

    "exam_date": [
        r"(?:Untersuchungs)?[Dd]atum[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
        r"Date[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
        r"Data[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
        r"Date\s+d.examen[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
        r"Data\s+(?:dell[a']?)?esame[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
    ],

    "last_name": [
        r"Name,\s*Vorname[:\s]+([^,\n\r]+),",
        r"Nachname[:\s]+([^\n\r,]+)",
        r"Last\s*Name[:\s]+([^\n\r,]+)",
        r"Family\s*Name[:\s]+([^\n\r,]+)",
        r"Nom(?:\s+de\s+famille)?[:\s]+([^\n\r,/]+)",
        r"Cognome[:\s]+([^\n\r,]+)",
    ],

    "first_name": [
        r"Name,\s*Vorname[:\s]+[^,\n\r]+,\s*([^\n\r]+)",
        r"Vorname[:\s]+([^\n\r,]+)",
        r"First\s*Name[:\s]+([^\n\r,]+)",
        r"Pr[eé]nom[:\s]+([^\n\r,]+)",
        r"Nome[:\s]+([^\n\r,]+)",
    ],

    "birth_date": [
        r"Geburtsdatum[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
        r"Date\s+of\s+Birth[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
        r"Date\s+de\s+naissance[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
        r"Data\s+di\s+nascita[:\s]+(\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4})",
    ],

    "gender": [
        r"Geschlecht[:\s]+([^\n\r,]+)",
        r"Sex(?:e)?[:\s]+([^\n\r,]+)",
        r"Sesso[:\s]+([^\n\r,]+)",
        r"Gender[:\s]+([^\n\r,]+)",
    ],

    "diagnosis": [
        r"Diagnose[:\s]+([\s\S]+?)" + _STOP,
        r"Diagnosis[:\s]+([\s\S]+?)" + _STOP,
        r"Diagnostic[:\s]+([\s\S]+?)" + _STOP,
        r"Diagnosi[:\s]+([\s\S]+?)" + _STOP,
    ],

    "measurements": [
        r"Messungen[:\s]+([\s\S]+?)" + _STOP,
        r"Measurements[:\s]+([\s\S]+?)" + _STOP,
        r"Mesures[:\s]+([\s\S]+?)" + _STOP,
        r"Misure[:\s]+([\s\S]+?)" + _STOP,
        r"Messungen[:\s]+([^\n\r]+)",
        r"Measurements[:\s]+([^\n\r]+)",
    ],

    "conditions_raw": [
        r"Bedingungen[:\s]+([\s\S]+?)" + _STOP,
        r"Conditions[:\s]+([\s\S]+?)" + _STOP,
        r"Condizioni[:\s]+([\s\S]+?)" + _STOP,
    ],

    "model": [
        r"Modell?[:\s]+([^\n\r]+)",
        r"Model[:\s]+([^\n\r]+)",
        r"Mod[eè]le[:\s]+([^\n\r]+)",
        r"Modello[:\s]+([^\n\r]+)",
    ],
}

def _score_pdf_fields(pdf_path: Path) -> int:
    if fitz is None:
        return 0
    try:
        doc  = fitz.open(str(pdf_path))
        text = "\n".join(page.get_text("text") for page in doc)
        doc.close()
        return len(_PATIENT_FIELD_PAT.findall(text))
    except Exception:
        return 0

def find_report_pdf(subject_folder: Path) -> Path | None:
    all_pdfs = [
        p for p in subject_folder.iterdir()
        if p.is_file() and p.suffix.lower() == ".pdf"
    ]

    if not all_pdfs:
        return None

    candidates = [p for p in all_pdfs if not _PDF_EXCLUDE.search(p.name)]

    if not candidates:
        candidates = all_pdfs

    priority = sorted(
        [p for p in candidates if _PDF_PRIORITY.search(p.name)],
        key=lambda p: p.name,
    )
    if priority:
        return priority[0]

    if fitz is not None:
        scored = [(p, _score_pdf_fields(p)) for p in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        best_path, best_score = scored[0]
        if best_score >= _MIN_PATIENT_FIELDS:
            return best_path

    return None

def extract_text_from_pdf(pdf_path: Path) -> str:
    if fitz is None:
        return ""
    try:
        doc  = fitz.open(str(pdf_path))
        text = "\n".join(page.get_text("text") for page in doc)
        doc.close()
        return text
    except Exception:
        return ""

def _match(text: str, patterns: list[str]) -> str | None:
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.MULTILINE)
        if m:
            return m.group(1).strip()
    return None

def _parse_conditions(raw: str | None) -> tuple[str, str]:
    if not raw:
        return "", ""
    left  = re.search(r"(?:Links|Left|Gauche|Sinistra)[:\s]+([^\n\r,;]+)", raw, re.I)
    right = re.search(r"(?:Rechts|Right|Droite|Destra)[:\s]+([^\n\r,;]+)",  raw, re.I)
    lv = left.group(1).strip()  if left  else raw.strip()
    rv = right.group(1).strip() if right else ""
    return lv, rv

def parse_pdf_fields(text: str) -> dict:
    result: dict[str, str] = {}
    for field, patterns in FIELD_PATTERNS.items():
        val = _match(text, patterns)
        if val:
            result[field] = val.strip()

    cond_l, cond_r = _parse_conditions(result.pop("conditions_raw", None))
    result["condition_left"]  = cond_l
    result["condition_right"] = cond_r

    for f in ("diagnosis", "measurements"):
        if f in result:
            result[f] = re.sub(r"\s+", " ", result[f]).strip()

    return result