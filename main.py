from datetime import datetime, timedelta
from db_timetable_api import timetable
from config import settings

# --- Einstellungen ---
CLIENT_ID = settings.db_client_id
CLIENT_SECRET = settings.db_client_secret
EVA = "8012253"  # Ludwigsfelde-Struveshof
TARGET_HOUR = "06"
TARGET_MINUTE = "26"

# --- Init ---
db = timetable.timetable_api(clientid=CLIENT_ID, clientsecret=CLIENT_SECRET)

# Datum für morgen im Format YYYY-MM-DD
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# 1) Geplante Fahrten im Slot 06:00–06:59 abrufen
try:
    plan = db.get_timetable(EVA, tomorrow, TARGET_HOUR)  # klar definierte Signatur
except Exception as e:
    # Falls der Timetables-Plan-Slot (selten) 404 liefert, behandeln wir das als "keine Plan-Daten"
    print(f"Plan-Daten nicht verfügbar ({e}).")
    plan = {"timetable": []}

# 2) Änderungen für den Bahnhof (z. B. Ausfälle/Verspätungen) abrufen
try:
    changes = db.get_changes(EVA)
except Exception as e:
    print(f"Änderungen nicht verfügbar ({e}).")
    changes = {"timetable": []}

def normalize_events(container):
    """Extrahiert Events aus den API-Objekten und harmonisiert Zeitfelder."""
    events = container.get("timetable", []) if isinstance(container, dict) else (container or [])
    norm = []
    for ev in events:
        # Mögliche Zeitfelder der Wrapper: 'plannedDateTime' (ISO) oder HAFAS-ähnlich 'pt' (HH:MM), evtl. 'ct' (geändert)
        iso = ev.get("plannedDateTime") or ev.get("changedDateTime")
        hhmm = None
        if iso and "T" in iso:
            hhmm = iso.split("T", 1)[1][:5]  # "HH:MM"
        else:
            hhmm = ev.get("ct") or ev.get("pt")  # bevorzugt geänderte Zeit, sonst geplante
        norm.append({
            "raw": ev,
            "hhmm": hhmm,
            "train_no": (ev.get("train") or {}).get("number") or ev.get("tnr"),
            "type": ev.get("type") or ev.get("eventType"),  # "DEPARTURE"/"ARRIVAL"
            "canceled": ev.get("canceled") is True or ev.get("status") == "CANCELLED",
        })
    return norm

plan_ev = normalize_events(plan)
chg_ev  = normalize_events(changes)

# Ziel: Abfahrten exakt 06:26 finden (inkl. geänderte Zeiten)
def is_target_dep(e):
    return (e["type"] or "").upper().startswith("DEP") and e["hhmm"] == f"{TARGET_HOUR}:{TARGET_MINUTE}"

hits_plan = [e for e in plan_ev if is_target_dep(e)]
# Änderungen können eine Fahrt auf 06:26 verschoben oder gestrichen haben
hits_chg  = [e for e in chg_ev  if is_target_dep(e)]

# Zusammenführen nach Zugnummer (falls vorhanden)
by_train = {}
for e in hits_plan + hits_chg:
    key = e["train_no"] or id(e)
    by_train.setdefault(key, {"plan": None, "chg": None})
    if e in hits_plan: by_train[key]["plan"] = e
    if e in hits_chg:  by_train[key]["chg"]  = e

if not by_train:
    print(f"Am {tomorrow} gibt es in {EVA} keine Abfahrt exakt um {TARGET_HOUR}:{TARGET_MINUTE}.")
else:
    for train_no, rec in by_train.items():
        canceled = (rec["chg"] and rec["chg"]["canceled"]) or (rec["plan"] and rec["plan"]["canceled"])
        status = "fällt aus" if canceled else "geplant/aktiv"
        print(f"Zug {train_no or '?'} um {TARGET_HOUR}:{TARGET_MINUTE}: {status}")
