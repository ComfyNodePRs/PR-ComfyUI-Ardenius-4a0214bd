"""
@author: initials AMAA
@title: Ardenius AI
@nickname: Ardenius
@description: ARD Text Box Counter to be used with ARD Counter - text box takes input text outputs a string of text..
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

class ARD_TEXT_BOX_COUNTER:
    # def __init__(self):
    #     pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True, "dynamicPrompts": True, "tooltip": "enter your text here"}),
                "ard_counter": ("FLOAT",{"default": 1.0})
            }
        }

    RETURN_NAMES = ("string_out", "ard_counter")
    RETURN_TYPES = ("STRING", "FLOAT")
    FUNCTION = "ard_text_box_counter"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Text Box Counter to be used with ARD Counter - text box takes input text outputs a string of text."

    def ard_text_box_counter(self, input_text, ard_counter):

        return (input_text, ard_counter)