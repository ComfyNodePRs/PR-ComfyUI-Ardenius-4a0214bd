"""
@author: initials AMAA
@title: Ardenius AI
@nickname: Ardenius
@description: ARD Empty latent image allows for entering divisor for image dimension
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

import torch
import comfy

MAX_RESOLUTION = 8192

class ARD_Empty_Latent_Image:
    def __init__(self):
        self.device = comfy.model_management.intermediate_device()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8, "tooltip": "The width of the latent images in pixels."}),
                "height": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 8, "tooltip": "The height of the latent images in pixels."}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096, "tooltip": "The number of latent images in the batch."}),
                "divx": ("INT", {"default": 8, "min": 8, "max": 4096, "step": 8, "tooltip": "image dimensions divx."})
            }
        }
    RETURN_TYPES = ("LATENT",)
    OUTPUT_TOOLTIPS = ("The empty latent image batch.",)
    FUNCTION = "ard_empty_latent_image"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Empty latent image allows for entering divx for image dimension"

    def ard_empty_latent_image(self, width, height, batch_size=1, divx=8):
        latent = torch.zeros([batch_size, 4, height // divx, width // divx], device=self.device)
        return ({"samples": latent}, )
