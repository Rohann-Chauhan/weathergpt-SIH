import pandas as pd 
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score,classification_report
output=pd.read_csv("flood_predicts/weather_flood_synthetic_10000.csv")
print(output.head())
print(output.info())
# Now get x and y from here for pandas use iloc

x=output.iloc[:,1:10]
y=output["flood"]
print(x)
print(y)
# Now train test and split
x_train,x_test ,y_train,y_test =train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
print(x_train.shape)
# Now use the logo 
output_predict=RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
output_predict.fit(x_train,y_train)
output_predit=output_predict.predict(x_test)

# Now get accuracy
actual_predict=accuracy_score(y_test,output_predit)
classification_repo=classification_report(y_test,output_predit)
print("prediction score:",actual_predict)
print(classification_repo)
joblib.dump(output_predict,"second_model.pkl")
print("Model save success")
print(type(output_predict))
print(type(output_predit))