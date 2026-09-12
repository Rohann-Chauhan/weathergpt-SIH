import joblib
import numpy as np
#from sklearn.metrics import pr
model=joblib.load("second_model.pkl")

print(type(model))
print("MODEL:", type(model))
#print("DATA:", type(output_data))
print("MODEL HAS PREDICT:", hasattr(model, "predict"))

print("Model output came succusfully")
# getting inputs 
rainfall_1h_mm=float(input("ENter the 1h rainfall:"))
rainfall_6h_mm=float(input("ENter the 6h rainfall:"))
rainfall_24h_mm=float(input("ENter the 24h rainfall:"))
rainfall_3day_mm=float(input("ENter the 3day rainfall:"))
temperature=float(input("Enter The tempreture:"))
humidity=float(input("enter the Humidity:"))
pressure=float(input("Enter the pressure:"))
wing_speed=float(input("enter The wind speed:"))
cloud_cover=float(input("Enter The cloud_cover:"))
output_data=np.array(
    [
    [
        rainfall_1h_mm,
        rainfall_6h_mm,
        rainfall_24h_mm,
        rainfall_3day_mm,
        temperature,
        humidity,
        pressure,
        wing_speed,
        cloud_cover
    ]
])
print("data of output_data:",type(output_data))
#output_answer=model.predict(output_data)[0]
#output_data_scaled=scaler.transform(output_data)
#output_data_scaled=scale.transform(output_data)
output_ans=model.predict(output_data)[0]
print(output_ans)
output_answer = model.predict_proba(output_data)[0][1]
print(output_answer)
#print()
print(f"probility of flood :{output_answer*100:.2f}%")
if output_answer < 0.30:
    print("LOW")
elif output_answer < 0.50:
    print("Medium")
elif output_answer < 0.80:
    print("HIGH")
else :
    print("Extrime")
