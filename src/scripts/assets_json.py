import json

if __name__=="__main__":
    """Create mapping address -> name, decimals
        Iterate through assets_2.json and do :
        a["tokens"][i]["address"] : (a["tokens"][i]["name"], ..decimals)
    """
    
    
    FILENAME = "utils/assets_2.json"