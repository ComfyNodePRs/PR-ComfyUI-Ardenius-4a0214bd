"""
@author: initials AMAA
@title: Ardenius
@nickname: Ardenius
@description: ARD Resize aids in image resizing.
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

class ARD_RESIZE:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                    "width": ("INT", {"default": 1024}),
                    "height": ("INT", {"default": 1024}),
                    "upscale_multiplier": ("FLOAT", {"default": 2.0}),
                    },
                "optional": {
                    "width_ratio": ("INT", {"default": 16}),
                    "height_ratio": ("INT", {"default": 9}),
                    },
                }

    RETURN_NAMES = ("latent_width", "latent_height", "x_pos", "y_pos")
    RETURN_TYPES = ("INT", "INT", "INT", "INT")

    FUNCTION = "ard_resize"

    OUTPUT_NODE = True

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Resize aids in image resizing"
    # my_code_start
    def ard_resize(self, width, height, width_ratio, height_ratio, upscale_multiplier):
        if width_ratio >= height_ratio:
            std_dimension = width
            std_ratio = height_ratio/width_ratio
            width_latent = int(std_dimension * upscale_multiplier)
            height_latent = int(std_dimension * std_ratio * upscale_multiplier)
        else:
            std_dimension = height
            std_ratio = width_ratio/height_ratio
            height_latent = int(std_dimension * upscale_multiplier)
            width_latent = int(std_dimension * std_ratio * upscale_multiplier)

        remainder = width_latent % 8
        width_latent = width_latent + remainder

        remainder = height_latent % 8
        height_latent = height_latent + remainder

        if width_latent > width:
            x_pos = int((width_latent - width)/2)
        else:
            x_pos = 0

        if height_latent > height:
            y_pos = int((height_latent - height)/2)
        else:
            y_pos = 0

        return (width_latent, height_latent, x_pos, y_pos)
    # my_code_end
