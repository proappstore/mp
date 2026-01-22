def find_earliest_open_order(db, exclude_order_id=None):
    # Orders are stored in db["orders"], preserve insertion order (list)
    for o in db.get("orders", []):
        if exclude_order_id and o.get("order_id") == exclude_order_id:
            continue
        if o.get("status") != "open":
            continue
        needed = int(o.get("target", 0)) - int(o.get("received", 0))
        if needed > 0:
            return o
    return None