# topics.py
cmnd_topics = {
    "pumpe": "GTN/Pool/Pumpe/cmnd/Power1",
    "uv": "GTN/Pool/UV/cmnd/Power1",
    "salz": "GTN/Pool/Salz/cmnd/Power1",
    "wp": "GTN/Pool/WP/cmnd/Power1",
    "licht": "GTN/Pool/Licht/cmnd/Power1",
    "hlicht": "GTN/Pool/Haus-Licht/cmnd/Power1",
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
    "pool_temp":            "GTN/Pool/Controller/tele/sensor.gtn_pool_control_pool_temperatur",
    "poolhaus_in_temp":     "GTN/Pool/Controller/tele/sensor.gtn_pool_control_poolhaus_in_temperatur",
    "waermepumpe_out_temp": "GTN/Pool/Controller/tele/sensor.gtn_pool_control_waermepumpe_out_temperatur",
    "poolhaus_out_temp":    "GTN/Pool/Controller/tele/sensor.gtn_pool_control_poolhaus_out_temperatur",
    "poolhaus_temp":        "GTN/Pool/Controller/tele/sensor.gtn_pool_control_poolhaus_temperatur",
    "wp_current_temp":      "GTN/Pool/Controller/tele/sensor.pool_wp_current_temp",
    "wp_target_temp":       "GTN/Pool/Controller/stat/target_temp",
    "power":                "GTN/Pool/Controller/tele/sensor.gtn_pool_active_power_total",
    "p_in":                 "GTN/Pool/Controller/tele/sensor.gtn_pool_control_poolhaus_in_druck",
    "p_out":                "GTN/Pool/Controller/tele/sensor.gtn_pool_control_poolhaus_out_druck",
    "energy_today":         "GTN/Pool/Controller/tele/sensor.gtn_pool_import_daily",
    "out_temp":             "GTN/Pool/Controller/tele/sensor.rain_gauge_temperature",
    "out_hum":              "GTN/Pool/Controller/tele/sensor.rain_gauge_humidity",
    "out_press":            "GTN/Pool/Controller/tele/sensor.rain_gauge_pressure",
}
