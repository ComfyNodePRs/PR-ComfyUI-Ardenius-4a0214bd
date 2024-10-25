"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: ARD Integer variable
"""
#  licensed under General Public License v3.0 all rights reserved © 2024
#  ( author initials AMAA Nickname Ardenius contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium Ardeniusai.com prompt engineer, text to image Models, ComfyUI custom nodes, and more to come)
#  below code is based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user as per the GPL V3.0 terms.

class ARD_MATH:
    # def __init__(self):
    #     pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Ix": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 9999999, "step": 0.0001, "tooltip": "input float if you want to input integer use ARD integer to float node"}),
                "Iy": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 9999999, "step": 0.0001, "tooltip": "input float if you want to input integer use ARD integer to float node"}),
                "operation": (["multiply", "divide", "subtract", "add"],  {"default": "divide", "tooltip": "pick math operation"}),
            },
        }

    RETURN_NAMES = ("result_integer", "result_float")
    RETURN_TYPES = ("INT", "FLOAT")
    FUNCTION = "ard_math"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD math node mathematical operations node."

    def ard_math(self, Ix, Iy, operation):
        try:
            if isinstance(Ix, int):
                Ix = float(Ix)
            elif isinstance(Ix, float):
                pass
            else:
                print("ARD math node ERROR: inputs need to be either integer or float")
                return (0, 0.0)
            if isinstance(Iy, int):
                Iy = float(Iy)
            elif isinstance(Iy, float):
                pass
            else:
                print("ARD math node ERROR: inputs need to be either integer or float")
                return (0, 0.0)

            if operation == "multiply":
                result_integer = int(Ix * Iy)
            elif operation == "divide":
                result_integer = int(Ix/Iy)
            elif operation == "subtract":
                result_integer = int(Ix - Iy)
            elif operation == "add":
                result_integer = int(Ix + Iy)
            else:
                print("pick a math operation")
                result_integer = 0

            if operation == "multiply":
                result_float = float(Ix * Iy)
            elif operation == "divide":
                result_float = float(Ix / Iy)
            elif operation == "subtract":
                result_float = float(Ix - Iy)
            elif operation == "add":
                result_float = float(Ix + Iy)
            else:
                print("ARD Math ERROR: pick a math operation")
                result_float = 0.0

            return (result_integer, result_float)
        except Exception as e:
            print("*****************************************")
            print(f"ARD math: check inputs ERROR {e}")
            print("*****************************************")
            return (0, 0.0)
