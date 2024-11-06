"""
@author: AMA
@title: Ardenius
@nickname: Ardenius
@description: CPlus Combine Images combines 4 or 2 images into 1 and outputs an image and a mask.
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

MAX_RESOLUTION = 8192


class ARD_4CROP_LATENT:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples": ("LATENT",),
                              "width_full_image": ("INT", {"default": 512, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                              "height_full_image": ("INT", {"default": 512, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                              }}

    RETURN_NAMES = ("TL_latent", "TR_latent", "BL_latent", "BR_latent",)
    RETURN_TYPES = ("LATENT", "LATENT", "LATENT", "LATENT",)
    FUNCTION = "crop_latent_function"

    CATEGORY = "Ardenius"
    #my_code_start
    def crop_latent_function(self, samples, width_full_image, height_full_image):

        width = int(width_full_image/2)
        height = int(height_full_image/2)
        x1 = 0
        y1 = 0
        s1 = self.crop_box(samples, width, height, x1, y1)
        x2 = width
        y2 = 0
        s2 = self.crop_box(samples, width, height, x2, y2)
        x3 = 0
        y3 = height
        s3 = self.crop_box(samples, width, height, x3, y3)
        x4 = width
        y4 = height
        s4 = self.crop_box(samples, width, height, x4, y4)
        return s1, s2, s3, s4

    def crop_box(s, samples, width, height, x, y):
        s_in = samples.copy()
        samples = samples['samples']
        x =  x // 8
        y = y // 8

        #enfonce minimum size of 64
        if x > (samples.shape[3] - 8):
            x = samples.shape[3] - 8
        if y > (samples.shape[2] - 8):
            y = samples.shape[2] - 8

        new_height = height // 8
        new_width = width // 8
        to_x = new_width + x
        to_y = new_height + y
        s_in['samples'] = samples[:,:,y:to_y, x:to_x]
        s_out = s_in
        return s_out
#my_code_end

