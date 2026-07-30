# ==========================================
# FILE ORGANIZER SETTINGS
# ==========================================

DEFAULT_SETTINGS = {
    "Images": True,
    "Documents": True,
    "PDFs": True,
    "Videos": True,
    "Audio": True,
    "Archives": True,
    "Programs": True,
    "Others": True
}


def get_default_settings():
    return DEFAULT_SETTINGS.copy()