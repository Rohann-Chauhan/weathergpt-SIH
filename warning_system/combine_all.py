#from tools.parc import weather_tool
from data import weather_data
from notify import warning_alert
from rise_engine import rise_enginer
from rise_engine import getting_alert
from validatio_data import validation
from warning_data import warning_generate

if not validation(weather_data):
    print("Invalid data")
    exit()
score=rise_enginer(weather_data)
sweverity=getting_alert(score)
warning=warning_generate(
    weather_data,score,sweverity
)
warning_alert(warning)