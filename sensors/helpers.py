# General view helping functions


# generate comment for air quality
def air_comment(air):
    if air < 50:
        return 'Healthy'
    elif air < 100:
        return 'Moderate'
    elif air < 150:
        return 'Unhealthy for Sensitive Groups'
    elif air < 200:
        return 'Unhealthy'
    elif air < 300:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'


# generate comment for temperature
def temperature_comment(temperature):
    if temperature < 0:
        return 'Very Cold'
    elif temperature < 10:
        return 'Cold'
    elif temperature < 20:
        return 'Cool'
    elif temperature < 30:
        return 'Warm'
    elif temperature < 40:
        return 'Hot'
    else:
        return 'Very Hot'


# generate comment for humidity
def humidity_comment(humidity):
    if humidity < 20:
        return 'Very Dry'
    elif humidity < 40:
        return 'Dry'
    elif humidity < 60:
        return 'Comfortable'
    elif humidity < 80:
        return 'Humid'
    else:
        return 'Very Humid'