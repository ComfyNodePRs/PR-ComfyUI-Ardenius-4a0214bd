"""
@author: initials AMAA
@title: Ardenius
@nickname: Ardenius
@description: ARD 4 Latent Upscale upscales 4 latent images by a set factor.
"""
#  licensed under General Public License v3.0 all rights reserved © 2024
#  ( author initials AMAA Nickname Ardenius contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium SD Models, ComfyUI custom nodes, and more to come)
#  below code is based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user as per the GPL V3.0 terms.

import folder_paths
import comfy


class ARD_4LATENT_UPSCALE:

    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "latent1": ("LATENT",), "upscale_method": (s.upscale_methods,),
                              "latent2": ("LATENT",), "upscale_method": (s.upscale_methods,),
                              "latent3": ("LATENT",), "upscale_method": (s.upscale_methods,),
                              "latent4": ("LATENT",), "upscale_method": (s.upscale_methods,),
                              "scale_by": ("FLOAT", {"default": 1.5, "min": 0.5, "max": 4.0, "step": 0.01}),}}
    RETURN_TYPES = ("LATENT", "LATENT", "LATENT", "LATENT",)
    FUNCTION = "ard_4latent_upscale"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD 4 Latent Upscale upscales 4 latent images by a set factor"

    # my_code_start
    def ard_4latent_upscale(self, latent1, latent2, latent3, latent4, upscale_method, scale_by):
        s1 = self.upscale(latent1, upscale_method, scale_by)
        s2 = self.upscale(latent2, upscale_method, scale_by)
        s3 = self.upscale(latent3, upscale_method, scale_by)
        s4 = self.upscale(latent4, upscale_method, scale_by)
        return s1, s2, s3, s4

    def upscale(self, samples, upscale_method, scale_by):
        s = samples.copy()
        width = round(samples["samples"].shape[3] * scale_by)
        height = round(samples["samples"].shape[2] * scale_by)
        s["samples"] = comfy.utils.common_upscale(samples["samples"], width, height, upscale_method, "disabled")
        return s
    # my_code_end




