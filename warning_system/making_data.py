import pandas as pd
dataset={
    "huminiity":[ 10,230,34,56,7,56],
    "work_day":[21,34,55,64,21,4],
    "system":[2,3,4,5,62,7],
    "flood":[0,0,0,1,0,1]
}
output=pd.DataFrame(dataset)
print(output)
output.to_csv("data_frame.csv",index=False)