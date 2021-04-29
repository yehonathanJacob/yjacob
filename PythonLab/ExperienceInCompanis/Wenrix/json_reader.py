import json

x = {"reservation":{"passengers":[{"first_name":"JOHN","last_name":"DOE","age":18}],"flights":[{"origin":"Tel-Aviv","destination":"New York","flight_number":725,"depart_at":"2021-02-15T15:00"},{"origin":"New York","destination":"Tel-Aviv","flight_number":726,"depart_at":"2021-02-25T07:00"}],"price":{"total":{"amount":"700.00","currency":"USD"},"base":{"amount":"600.00","currency":"USD"},"taxes":{"T1":{"amount":"20.00","currency":"USD"},"T2":{"amount":"30.00","currency":"USD"},"T3":{"amount":"50.00","currency":"USD"}}}}}

def json_dump(root,depth=1):
    command_to_separate = "#" +","*depth+"#"
    json_string = ""
    if isinstance(root, dict):
        json_string += "{"
        list_to_join = []
        for key in root.keys():
            list_to_join.append('"'+str(key)+'":' + json_dump(root[key], depth=depth+1))

        json_string += command_to_separate.join(list_to_join)
        json_string += "}"
    elif isinstance(root, list):
        json_string += "["
        list_ro_join = []
        for value in root:
            list_ro_join.append(json_dump(value, depth=depth+1))
        json_string += command_to_separate.join(list_ro_join)
        json_string += "]"
    elif type(root) in [float, int]:
        json_string += str(root)
    else:
        json_string += '"'+str(root)+'"'

    return json_string


def json_loads(json_string, depth=1):
    command_to_separate = "#" + "," * depth + "#"
    if json_string[0] == "[":
        json_obj = []
        json_string = json_string[1:-1]
        list_of_json_string = json_string.split(command_to_separate)
        for json_sub_string in list_of_json_string:
            json_obj.append(json_loads(json_sub_string, depth=depth+1))

    elif json_string[0] == "{":
        json_obj = dict()
        json_string = json_string[1:-1]
        list_of_json_string = json_string.split(command_to_separate)
        for json_sub_string in list_of_json_string:
            key_string, value_string = json_sub_string.split(":", maxsplit=1)
            key = json_loads(key_string, depth=depth+1)
            value = json_loads(value_string, depth=depth+1)
            json_obj[key] = value

    elif json_string[0] == '"':
        json_obj = json_string[1:-1]
    else:
        json_obj = float(json_string)

    return json_obj

json_string = json_dump(x)
print(json_string)
json_obj_test = json_loads(json_string)
print("json_obj_test: ")
print(json_obj_test)
print(json_obj_test==x)


