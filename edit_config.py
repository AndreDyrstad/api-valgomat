import json
from database_folder import sql_queries

def update_config_file(data, entity_type):

    print(data)

    save_to_config = {}

    for key in data.keys():
        save_to_config[key] = []
        for question in data[key]:
            save_to_config[key].append({"id":question["id"],"displayAs":question["displayAs"]})

    if entity_type == "patient":
        with open('config_files/test_config.json', 'w') as output_file:
            json.dump(save_to_config, output_file)
    else:
        with open('config_files/test_config.json', 'w') as output_file:
            json.dump(save_to_config, output_file)


def read_config_file(entity_type):
    json_file = sql_queries.get_questions_by_id(entity_type)

    print(json_file)
