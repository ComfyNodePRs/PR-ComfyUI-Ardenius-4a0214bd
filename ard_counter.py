"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: ARD Counter: keeps increasing x_count by x_input until x_total is reached then resets to zero
"""

#  licensed under General Public License v3.0 all rights reserved © 2024
#  Owner initials: AMAA
#  nickname: Ardenius
#  email: ardenius7@gmail.com
#  website: https://ko-fi.com/ardenius
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium SD Models, ComfyUI custom nodes, and more to come)
#  below code is based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user as per the GPL V3.0 terms.

import os.path
import ard_lib
current_directory = os.path.dirname(os.path.abspath(__file__))
ard_data = os.path.join(current_directory, "ard_data")

class ARD_COUNTER:
    # def __init__(self):
    #     pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "x_input": ("FLOAT", {"default": 1, "tooltip": "input a float that increments to be added to x_count"}),
                "x_total": ("FLOAT", {"default": 1, "tooltip": "total a float when reached resets x_count to zeros"})
            }
        }

    RETURN_NAMES = ("x_count_int", "x_count_float",)
    RETURN_TYPES = ("INT", "FLOAT",)
    FUNCTION = "ard_counter"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Counter: keeps counting integer number increasing by Cx and zeros if total is reached"

    def ard_counter(self, x_input, x_total):

        x_count_int = 0
        x_count_float = 0.0

        if isinstance(x_input, float) or isinstance(x_input, int):
            x_input = float(x_input)
        else:
            print("ARD Counter: ERROR x_input is not a float nor an integer")
            x_count_int = 0
            x_count_float = 0.0

        if isinstance(x_input, float) or isinstance(x_input, int):
            x_input = float(x_input)
        else:
            print("ARD Counter: ERROR x_input is not a float nor an integer")
            x_count_int = 0
            x_count_float = 0.0

        ard_counter_json = os.path.join(ard_data, "ard_counter.json")
        counter_dict = {}
        x_input_old = 0.0
        x_total_old = 0.0
        x_count_float_old = 0.0
        x_count_int_old = 0

        if not os.path.exists(ard_counter_json):
            counter_dict = {"x_input": x_input, "x_total": x_total, "x_count_int": 0, "x_count_float": 0.0}
            ard_lib.save_dict_to_json(counter_dict, ard_counter_json)
        else:
            counter_dict = ard_lib.read_dict_from_json(ard_counter_json)
            x_input_old = counter_dict.get("x_input", 0.0)
            x_total_old = counter_dict.get("x_total_old", 0.0)
            x_count_float_old = counter_dict.get("x_count_float", 0.0)
            x_count_int_old = counter_dict.get("x_count_int_old", 0)

        if x_input is not None and 0.0 < x_input < x_total:
            x_count_float = x_count_float_old + x_input

            if x_count_float > x_total:
                x_input = 0.0
                x_total = 0.0
                x_count_float = 0.0
                x_count_int = 0
                print(f'\n***\nard_counter reset to zero:\nx count float: {x_count_float}\nx input: {x_input}\nx total: {x_total}\n***\n')

            x_count_int = int(x_count_float)
            counter_dict["x_input"] = x_input
            counter_dict["x_total"] = x_total
            counter_dict["x_count_int"] = x_count_int
            counter_dict["x_count_float"] = x_count_float
            ard_lib.save_dict_to_json(counter_dict, ard_counter_json)
            print(f'\n***\nx count float: {x_count_float}\nx input: {x_input}\nx total: {x_total}\n***\n')
        else:
            x_count_float = x_count_float_old
            x_count_int = x_count_int_old

        return (x_count_int, x_count_float)
