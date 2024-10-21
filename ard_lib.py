#  this software and code © 2024 initals AMAA nickname Ardenius is licensed under GPL V3.0
#  ( author contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius on the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Premium Memebers only Perks (Premium SD Models, ComfyUI custom nodees, and more to come)
#  the below code is in part or in full based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI

import os
import sys
import json
import inspect
import importlib.util


def save_dict_to_json(data_dict, json_file_path):
    try:
        with open(json_file_path, 'w') as file:
            json.dump(data_dict, file, indent=4)
            # print(f"\nJSON file created and data saved successfully to: \n{json_file_path}")
    except:
        pass


def read_dict_from_json(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data_dict = json.load(file)
            # print(f'\nreturned dict: \n{data_dict}')
    else:
        data_dict = {}
    return data_dict


def is_utf8(text):
    try:
        text.encode('utf-8').decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def ard_text_to_cond(clip, pos_text):
    pos_tokens = clip.tokenize(pos_text)
    pos_output = clip.encode_from_tokens(pos_tokens, return_pooled=True, return_dict=True)
    pos_cond = pos_output.pop("cond")
    return [[pos_cond, pos_output]]


def scan_nodes_folder(nodes_path):
    file_list = []

    for file in os.listdir(nodes_path):
        if file.endswith(".py"):
            module_name = os.path.splitext(file)[0]
            module_path = os.path.join(nodes_path, file)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                file_list.append([module_name, obj])

            return file_list
