from typing import List, Dict, Any, Optional
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
from config import cred

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })



def pickProperty(property_id: str) -> dict | None:
    all_properties = db.reference('test_all_banks').get() or {}

    for prop in all_properties.values():
        if str(prop.get("id")) == str(property_id):
            return prop
    return None

def parse_brazilian_currency(value_str):
    if not value_str:
        return 0.0

    value_str = value_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(value_str)
    except ValueError:
        return 0.0

def filter_bradesco(
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    city: Optional[str] = None,
    area: Optional[str] = None,  # em m²
    date: Optional[str] = None   # 'YYYY-MM-DD'
) -> List[Dict[str, Any]]:
    ref = db.reference('test_all_banks')
    data = ref.get() or []

    filtered = []
    items = data.items() if isinstance(data, dict) else enumerate(data)
    for item_id, item in items:
        if not item:
            continue

        item_value = parse_brazilian_currency(item.get("price", 0))
        if min_value is not None and item_value < min_value:
            continue
        if max_value is not None and item_value > max_value:
            continue
        if city is not None and item.get("city", "").lower() != city.lower():
            continue
        if area is not None and item.get("area", "").lower() != area.lower():
            continue
        if date is not None:
            item_date = item.get("date")
            if item_date != date:
                try:
                    item_date_obj = datetime.strptime(item_date, "%Y-%m-%d")
                    filter_date_obj = datetime.strptime(date, "%Y-%m-%d")
                    if item_date_obj != filter_date_obj:
                        continue
                except Exception:
                    continue
        filtered.append(item)
    print(filtered)
    return filtered