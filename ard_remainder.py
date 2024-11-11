"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: ARD remainder: adds to Ix to make it divisible by Dx and outputs the integer
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

class ARD_REMAINDER:
    # def __init__(self):
    #     pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Ix": ("INT", {"default": 1024, "tooltip": "input an integer"}),
                "Dx": ("INT", {"default": 8, "tooltip": "if integer Ix is not divisible by Dx it will add to it to make it divisible"}),
            },
        }

    RETURN_NAMES = ("integer",)
    RETURN_TYPES = ("INT",)
    FUNCTION = "ard_remainder"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD remainder: adds to Ix to make it divisible by Dx and outputs the integer"

    def ard_remainder(self, Ix, Dx):
        try:
            if not isinstance(Dx, int):
                Dx = int(Dx)

            if Dx == 0:
                print("*****************************************")
                print("ARD remainder: ERROR Dx can not be Zero")
                print("*****************************************")
                output_integer = Ix
                return (output_integer,)

            if not isinstance(Ix, int):
                output_integer = int(Ix)
            else:
                output_integer = Ix

            remainder = output_integer % Dx
            if remainder != 0:
                output_integer = output_integer + (Dx - remainder)
            else:
                pass

            return (output_integer,)
        except Exception as e:
            print("*****************************************")
            print(f"ARD remainder: ERROR {e}")
            print("*****************************************")
            output_integer = Ix
            return (output_integer,)