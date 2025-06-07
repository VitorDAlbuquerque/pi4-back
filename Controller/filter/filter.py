from typing import List, Dict, Any, Optional
from datetime import datetime

def filter_bradesco(
    data: List[Dict[str, Any]],
    value: Optional[float] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    area: Optional[str] = None,
    date: Optional[str] = None  #'YYYY-MM-DD'
) -> List[Dict[str, Any]]:
   
    filtered = []
    for item in data:
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