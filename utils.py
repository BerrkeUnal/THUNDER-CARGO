def get_progress_value(status):
    status = str(status).lower()
    if "hazır" in status or "pending" in status: return 25
    elif "yol" in status or "transit" in status: return 50
    elif "dağıtım" in status or "delivery" in status: return 75
    elif "teslim" in status or "delivered" in status: return 100
    return 0