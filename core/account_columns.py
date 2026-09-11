# app/core/account_columns.py
from core.utils import get_time_ago
SIMPLE_COLUMNS = [
    {"header": "ID", "key": "id"},
    {"header": "Name", "key": "name"},
    {"header": "Category", "key": "category"},
    {"header": "Noted", "key": "notes"},
    {"header": "Status", "key": "status"},
    {"header": "Account Status", "key": "account_status"},
    {"header": "Page", "key": "page"},
    {"header": "Friends", "key": "friends"},

    # GPS
    {
        "header": "Fake GPS",
        "key": "gps",
        "formatter": lambda v: "\ud83d\udfe2 ON" if v and v.get("enable") else "\ud83d\udd34 OFF"
    },
    {
        "header": "Set Fake GPS",
        "key": "gps",
        "formatter": lambda v: (
            f"{v.get('lat','')}, {v.get('long','')}"
            if v and v.get("enable") else ""
        )
    },

    # VPN
    {
        "header": "VPN",
        "key": "vpn",
        "formatter": lambda v: "\ud83d\udfe2 ON" if v and v.get("enable") else "\ud83d\udd34 OFF"
    },
    {
        "header": "Set VPN",
        "key": "vpn",
        "formatter": lambda v: (
            f"{v.get('name','')} ({v.get('city','')})"
            if v and v.get("enable") else ""
        )
    },
    {"header": "Created Date", "key": "date_created"},
    {
        "header": "Time Ago", 
        "key": "last_date", 
        "formatter": lambda v: get_time_ago(v) # Direct, high-performance call
    },
    {"header": "Last Date", "key": "last_date"},

    
]

DETAIL_COLUMNS = [
    {"header": "ID", "key": "id"},
    {"header": "Name", "key": "name"},
    {"header": "Category", "key": "category"},
    {"header": "Noted", "key": "notes"},
    {"header": "Status", "key": "status"},
    {"header": "Account Status", "key": "account_status"},
    {"header": "Page", "key": "page"},
    {"header": "Friends", "key": "friends"},

    {
        "header": "Fake GPS",
        "key": "gps",
        "formatter": lambda v: "\ud83d\udfe2 ON" if v and v.get("enable") else "\ud83d\udd34 OFF"
    },
    {
        "header": "Set Fake GPS",
        "key": "gps",
        "formatter": lambda v: (
            f"{v.get('lat','')}, {v.get('long','')}"
            if v and v.get("enable") else ""
        )
    },

    {
        "header": "VPN",
        "key": "vpn",
        "formatter": lambda v: "\ud83d\udfe2 ON" if v and v.get("enable") else "\ud83d\udd34 OFF"
    },
    {
        "header": "Set VPN",
        "key": "vpn",
        "formatter": lambda v: (
            f"{v.get('name','')} ({v.get('city','')})"
            if v and v.get("enable") else ""
        )
    },

    

    {"header": "UID", "key": "uid"},
    {"header": "Email", "key": "email"},
    {"header": "Password", "key": "password"},
    {"header": "Cookies", "key": "cookies"},
    {"header": "Two Factor(2FA)", "key": "two_fa"},
    {"header": "Phone Number", "key": "phone_number"},
    {"header": "Birthday", "key": "birthday"},

    {"header": "Model Name", "key": "model"},
    {"header": "Device Name", "key": "market_name"},

    {"header": "MAC Address", "key": "mac"},
    {"header": "IMSI", "key": "imsi"},
    {"header": "SIM ID", "key": "simid"},

    {"header": "Created Date", "key": "date_created"},
    {
        "header": "Time Ago", 
        "key": "last_date", 
        "formatter": lambda v: get_time_ago(v) # Direct, high-performance call
    },
    {"header": "Last Date", "key": "last_date"},
]