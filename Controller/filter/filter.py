from typing import List, Dict, Any, Optional
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db
from config import cred

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://lobotomia-18768-default-rtdb.firebaseio.com/'
    })



def filter_bradesco(
    value: Optional[float] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    area: Optional[str] = None,
    date: Optional[str] = None  # 'YYYY-MM-DD'
) -> List[Dict[str, Any]]:
  
    ref = db.reference('test_bradesco')
    data = ref.get() or []

    filtered = []
    items = data.items() if isinstance(data, dict) else enumerate(data)
    for item_id, item in items:
        if not item:
            continue
        if value is not None and float(item.get("value", 0)) != value:
            continue
        if state is not None and item.get("state", "").lower() != state.lower():
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
    return filtered

