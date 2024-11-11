"""
@author: initials AMAA
@title: Ardenius
@nickname: Ardenius
@description: ARD 4VAE Decode takes in 4 latent images and decodes them.
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


class ARD_4VAE_DECODE:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"samples_1": ("LATENT",),
                             "vae": ("VAE", ),
                             "tile_size": ("INT", {"default": 512, "min": 320, "max": 4096, "step": 64}),
                             },
                "optional": {"samples_2": ("LATENT",),
                             "samples_3": ("LATENT",),
                             "samples_4": ("LATENT",),
                             },
                }
    RETURN_NAMES = ("image_1", "image_2", "image_3", "image_4",)
    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE",)
    FUNCTION = "ard_4vae_decode"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD 4VAE Decode takes in 4 latent images and decodes them"

    # my_code_start
    def ard_4vae_decode(self, vae, tile_size, samples_1, samples_2, samples_3, samples_4):
        result1 = self.decode(vae, samples_1, tile_size)
        result2 = self.decode(vae, samples_2, tile_size)
        result3 = self.decode(vae, samples_3, tile_size)
        result4 = self.decode(vae, samples_4, tile_size)
        return (result1, result2, result3, result4,)
    # my_code_end
    def decode(self, vae, sample_n, tile_size):
        return vae.decode_tiled(sample_n["samples"], tile_x=tile_size // 8, tile_y=tile_size // 8,)
