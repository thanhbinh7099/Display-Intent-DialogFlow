import pycommon
import json
from graphviz import Digraph
from graphviz import Graph

load_curl = """curl --request GET \
              --url 'https://api.dialogflow.com/v1/intents?v=20150910' \
              --header 'authorization: Bearer {token}' \
              --header 'content-type: application/json'"""

# Vẽ sơ đồ đầy đủ

def draw_table (model,intent, option):
    name_intent = "#I: " + intent["name"]
    xxx = '{' + name_intent   #Vẽ bảng theo mẫu:  node('Intent','{I:|{E: | A: }|CIs |COs }')
    if option != "context":
        event_intent = "E: "
        for event in intent["events"]:
            event_intent += event["name"]

        action_intent = "A: "
        for action in intent["actions"]:
            action_intent += action
        xxx += "|{" + event_intent + "|" + action_intent + "}"
    if option != "event-action":
        contextIn_list = ""
        for contextIn in intent["contextIn"]:
            contextIn_list += "|"+ "<"+ contextIn+">"+ "In: " + contextIn

        contextOut_list = ""
        for contextOut in intent["contextOut"]:
            contextOut_list += "|" + "<" + contextOut["name"]+">" + "Out: " + str(contextOut["lifespan"]) +"."+ contextOut["name"]
        xxx += "|" + contextIn_list + "|" + contextOut_list
    xxx += "}"
    model.node(str(intent["id"]), xxx)


    return model

def create_link (model, intent, dialogflow_model_data, option):
    for checked_intent in dialogflow_model_data:
        if checked_intent == intent:
            continue
        else:
            for contextOut in intent['contextOut']:
                for check_contextIn_name in checked_intent["contextIn"]:
                    if contextOut["lifespan"] != 0 and contextOut["name"] == check_contextIn_name:
                        if option == "event-action":
                            arr = [(intent["id"], checked_intent["id"])]
                        else:
                            arr = [(""+intent["id"]+":" +contextOut["name"]+"",""+checked_intent["id"]+":" +check_contextIn_name+"")]
                        model.edges(arr)       #('a:b','c:d')

    return model


def display_intent(token, option):
    repaced = pycommon.keymap_replace(load_curl,{"token": token})
    dialogflow_model_data = pycommon.execute_curl(repaced)

    src_pdf = "static/display_pdf/"+token+ "_" + option +".gv"
    model = Digraph('structs', filename=src_pdf, node_attr={'shape': 'record'})
    # Vẽ Bảng
    for intent in dialogflow_model_data:
        model = draw_table(model, intent, option)
   # Nối theo Context
    for intent in dialogflow_model_data:
        model = create_link(model, intent, dialogflow_model_data, option)
    model.render(src_pdf)
    return src_pdf + '.pdf'

