# Rise The if tempreture > 23 increse score and if score > 60 then alert also understand
from data import weather_data
def rise_enginer(data):
    score=0
    if data["tempreture"] >=100:
        score+=30
        return score
    if data["humadity"] >=34:
        score+=15
        return score
    if data["rain_flow"] >=32:
        score+=23
        return score
    if data["water_level"] >=4.5:
        score+=13
        return score
    else:
        return score

output_alert=rise_enginer(weather_data)

def getting_alert(output_alert):
    if output_alert >= 100:
        print("HIGH ALERT")
    if output_alert >=80:
        print("Alert getting")
    if output_alert >=50:
        print("Warning")
    if output_alert >=30:
        print("NORMAL")
    return output_alert
output_a=getting_alert(output_alert)
print(output_a)
