def warning_generate(  data,score,sweverity):
    if score == "NORMAL":
        return {
                "place":data["location"],
                "output_messge":f"The weather is ok and high alert"
                ""

        }
    else:
        return {
                "place":data["location"],
                "output_message":"The messge should be under Warning Zone ",
                "score":score,
                "servity":sweverity,
                "message":{
                    "final_message":"the final message will be servity and explain it ",
                    "output_message":"The real message according to given output"
                }
            
        }