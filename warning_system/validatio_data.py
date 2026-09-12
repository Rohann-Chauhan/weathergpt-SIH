# now make validation someone not make or give vlaue in -45 etc
def validation(data):
    if data["tempreture"] < 0 and data["tempreture"] > 100:
        return False
    if data["humadity"] < 0 :
        return  False
    if data["rain_flow"] < 0:
        return False
    if data["winter_c"] < 0:
        return False
    if data["water_level"] <0:
        return False
    else:
        return True
    