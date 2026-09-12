def warning_alert(warning):
    print("------ WARNING-------")
    print("The flood what comes here")
    #print(f"the score is {warning["location"]}")
    #print(f"The severity is {warning["sweverity"]}")
    #write_score=warning["score"]
    if "rise_warning" in warning:
        print(f"The rise score and warning will be:{warning["rise_warning"]}")
    #print(f"warning score is the answer:{warning["location"]}")
