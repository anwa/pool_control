# topics.py
cmnd_topics = {
    "pumpe": "GTN/Pool/Pumpe/cmnd/Power1",
    "uv": "GTN/Pool/UV/cmnd/Power1",
    "salz": "GTN/Pool/Salz/cmnd/Power1",
    "wp": "GTN/Pool/WP/cmnd/Power1",
    "licht": "GTN/Pool/Licht/cmnd/Power1",
    "haus_licht": "GTN/Pool/Haus-Licht/cmnd/Power1",
}

relay_topics = {
    "pumpe_state": "GTN/Pool/Pumpe/stat/POWER",
    "pumpe_power": "GTN/Pool/Pumpe/tele/SENSOR",
    "uv_state": "GTN/Pool/UV/stat/POWER",
    "uv_power": "GTN/Pool/UV/tele/SENSOR",
    "elektrolyse_state": "GTN/Pool/Salz/stat/POWER",
    "elektrolyse_power": "GTN/Pool/Salz/tele/SENSOR",
    "wp_state": "GTN/Pool/WP/stat/POWER",
    "wp_power": "GTN/Pool/WP/tele/SENSOR",
    "licht_state": "GTN/Pool/Licht/stat/POWER",
    "hlicht_state": "GTN/Pool/Haus-Licht/stat/POWER",
}

mess_topics = {
    "wp_target_temp": "GTN/Pool/Controller/stat/target_temp",
    "wp_current_temp": "GTN/Pool/Controller/tele/current_temp",
}
