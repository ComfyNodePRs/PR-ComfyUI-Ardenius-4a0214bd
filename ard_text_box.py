"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: ARD text box outputs a string of text
"""
#  licensed under General Public License v3.0 all rights reserved © 2024
#  ( author initials AMAA Nickname Ardenius contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium SD Models, ComfyUI custom nodes, and more to come)
#  below code is based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user as per the GPL V3.0 terms.

class ARD_TEXT_BOX:
    # def __init__(self):
    #     pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "dynamicPrompts": True, "tooltip": "enter your text here output is a string not a prompt input"}),
            },
        }

    RETURN_NAMES = ("string_out",)
    RETURN_TYPES = ("STRING",)
    FUNCTION = "ard_text_box"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD text box outputs a string of text."

    def ard_text_box(self, text):

        return (text)