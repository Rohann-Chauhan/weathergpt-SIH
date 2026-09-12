# Now make the flood making full 
data={
    "tempreture":32,
    "flood_blow":50.4,
    "wind_blow":16,
    "winter_cold":2,
    "rainning":45
}
def alert_system(data):
    alert=[]
    if data["tempreture"] >= 45:
        alert.append("Tempreture HIGH")
    if data["flood_blow"] >= 50.2:
        alert.append("Flood_blow alert")
    if data["wind_blow"] >= 15:
        alert.append("Wind Flow Alert")
    if data["winter_cold"] >= 3:
        alert.append("winter_cold ALert")
    if data["rainning"] >= 43:
        alert.append("Rain Data Alert")
    return alert

output=alert_system(data)
print(output)
# Now make the tool output here and get answer or use
from tools.parc import weather_tool
                                                                                                    