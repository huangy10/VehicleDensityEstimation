# coding=utf-8
import json


def save_variables_to_json(output_file='output.json', **kwargs):
    file_name_elements = output_file.split('.')
    if len(file_name_elements) == 1:
        output_file += '.json'
    elif file_name_elements[-1] != 'json':
        raise TypeError('目前只支持json输出')
    output = open('data/' + output_file, 'w')
    output.write(json.dumps(kwargs))
    output.close()


def load_variables_from_json(input_file='input_file'):
    input_file = open(input_file)
    data = input_file.readall()
    result_dict = json.loads(data)
    input_file.close()
    return result_dict
