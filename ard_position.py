"""
@author: initials AMAA
@title: Ardenius
@nickname: Ardenius
@description: ARD Position positions images in latent space correctly.
"""
#  licensed under General Public License v3.0 all rights reserved © 2024
#  ( author initials AMAA Nickname Ardenius contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium Ardeniusai.com prompt engineer, text to image Models, ComfyUI custom nodes, and more to come)
#  below code is based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user as per the GPL V3.0 terms.

import folder_paths
MAX_RESOLUTION = 8192

class ARD_POSITION:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                    "width": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "height": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "upscale_multiplier": ("FLOAT", {"default": 1.5, "step": 0.1}),
                    },
                }

    RETURN_NAMES = ("latent_width", "latent_height", "x_1", "y_1", "x_2", "y_2", "x_3", "y_3", "x_4", "y_4")
    RETURN_TYPES = ("INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT", "INT")

    FUNCTION = "ard_position"

    OUTPUT_NODE = True

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Position positions images in latent space correctly"
    # my_code_start
    def ard_position(self, width, height, upscale_multiplier):
        width_latent = int(width * upscale_multiplier)
        height_latent = int(height * upscale_multiplier)

        width_latent = int(self.with_remainder(width_latent))

        height_latent = int(self.with_remainder(height_latent))

        x_1 = 0
        y_1 = 0
        x_2 = int(width_latent/2)
        y_2 = 0
        x_3 = 0
        y_3 = int(height_latent/2)
        x_4 = int(width_latent/2)
        y_4 = int(height_latent/2)

        return (width_latent, height_latent, x_1, y_1, x_2, y_2, x_3, y_3, x_4, y_4)

    @classmethod
    def with_remainder(s, input_num):
        if input_num % 8 != 0:
            output_num = input_num + (8 - (input_num % 8))
        else:
            output_num = input_num
        return output_num
    # my_code_end
