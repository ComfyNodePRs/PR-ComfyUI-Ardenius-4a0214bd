"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: ARD upscale latent by: adds width and height output and up scales a latent input by a float factor that is more accurate than original node
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

import comfy


class ARD_LATENT_UPSCALE_BY:
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":
            {
                "samples": ("LATENT",),
                "upscale_method": (s.upscale_methods,),
                "scale_by": ("FLOAT", {"default": 1.5, "min": 0.01, "max": 8.0, "step": 0.0001}),
                "divx": ("INT", {"default": 8, "min": 8, "max": 4096, "step": 8})
            },
        }
    RETURN_TYPES = ("LATENT", "INT", "INT",)
    RETURN_NAMES = ("latent", "width", "height")
    FUNCTION = "ard_latent_upscale_by"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD upscale latent by: adds width and height output and up scales a latent input by a float factor that is more accurate than original node"

    def ard_latent_upscale_by(self, samples, upscale_method, scale_by, divx):
        s = samples.copy()
        width = round(samples["samples"].shape[3] * scale_by)
        height = round(samples["samples"].shape[2] * scale_by)

        width = self.fix_dimensions(width, divx)
        height = self.fix_dimensions(height, divx)

        s["samples"] = comfy.utils.common_upscale(samples["samples"], width, height, upscale_method, "disabled")
        return (s, width, height, )

    def fix_dimensions(self, dimension_in, divx):
        real_dimension = int(dimension_in * 8)
        d_remainder = real_dimension % divx
        d_remainder_fix = int(divx - d_remainder)
        if d_remainder != 0:
            real_dimension += d_remainder_fix
        if real_dimension == 1648:
            real_dimension = 1664
        if real_dimension == (1136 or 1128):
            real_dimension = 1152
        real_dimension = int(real_dimension/8)
        return real_dimension
