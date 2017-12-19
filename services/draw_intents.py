import pycommon
import json
from graphviz import Digraph
from graphviz import Graph


def draw_table (model,intent):
    name_intent = "#I: " + intent["name"]
    event_intent = "E: "
    for event in intent["events"]:
        event_intent += event["name"]

    action_intent = "A: "
    for action in intent["actions"]:
        action_intent += action

    contextIn_list = ""
    for contextIn in intent["contextIn"]:
        contextIn_list += "|"+ "<"+ contextIn+">"+ "In: " + contextIn

    contextOut_list = ""
    for contextOut in intent["contextOut"]:
        contextOut_list += "|" + "<" + contextOut["name"]+">" + "Out: " + str(contextOut["lifespan"]) +"."+ contextOut["name"]
    #Vẽ bảng theo mẫu:  node('Intent','{I:|{E: | A: }|CIs |COs }')
    model.node(str(intent["id"]), '{' + name_intent + \
            '|{' + event_intent + '|' + action_intent + '}|\
            ' + contextIn_list + '|' + contextOut_list + ' }')


    return model

def create_link_context(model, intent, dialogflow_model_data):
    for check_intent in dialogflow_model_data:
        if check_intent == intent:
            continue
        else:
            for contextOut in intent['contextOut']:
                for check_contextIn_name in check_intent["contextIn"]:
                    if contextOut["lifespan"] != 0 and contextOut["name"] == check_contextIn_name:
                        # xxx = "[('" + str(intent["id"])+":"+[contextOut]["name"] + "'", "'" + str(check_intent["id"])+":"+check_contextIn_name+"')]"
                        # model.edges([("'" + intent[id]+":"+[contextOut]["name"] + "'", "'" + check_intent["id"]+":"+check_contextIn_name+"'")])
                        arr = [(""+intent["id"]+":" +contextOut["name"]+"",""+check_intent["id"]+":" +check_contextIn_name+"")]
                        model.edges(arr)
                        # print(arr)
                        # arr = [(intent["id"]: contextOut["name"], check_intent["id"]: check_contextIn_name)]


                        print(intent["id"])         #('a:b','c:d')

    return model


if __name__ == '__main__':
    s = "curl --request GET \
      --url 'https://api.dialogflow.com/v1/intents?v=20150910' \
      --header 'authorization: Bearer 7e81a0339f8f4211bf6f17a4ee77295d' \
      --header 'content-type: application/json'"
    dialogflow_model_data = pycommon.execute_curl(s)


    from graphviz import Digraph

    model = Digraph('structs',  filename='structs_revisited.gv', node_attr={'shape': 'record'})
# Vẽ Bảng
    for intent in dialogflow_model_data:
        model = draw_table(model,intent)
# Nối theo Context
    for intent in dialogflow_model_data:
        model = create_link_context(model, intent, dialogflow_model_data)

    # model.edges([('[SN_1NV]LAY_LOI_CHUC:SN-LAY_LOI_CHUC','[SN]_HOI_SINH_NHAT - CO - Chua-Co-Mau-Tin:SN-LAY_LOI_CHUC')])

    model.view()










    ####Def

    # s.node('struct1', '<f0> left|<f1> middle|<f2> right')
    # s.node('struct2', '<f0> one|<f1> two')
    # s.node('struct3', r'hello\nworld |{ b |{c|<here> d|e}| f}| g | h\nk')
    # s.edges([('struct1:f1', 'struct2:f0'), ('struct1:f2', 'struct3:here')])



