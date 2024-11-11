"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: ARD float: outputs an float number
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

class ARD_FLOAT:
    # def __init__(self):
    #     pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Fx": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 999999.0, "step": 0.0001, "tooltip": "float variable"}),
            },
        }

    RETURN_NAMES = ("float",)
    RETURN_TYPES = ("FLOAT",)
    FUNCTION = "ard_float"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD float: outputs a float number"

    def ard_float(self, Fx):

        if not isinstance(Fx, float):
            output_float = float(Fx)
        else:
            output_float = Fx

        return (output_float,)