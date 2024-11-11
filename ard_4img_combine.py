"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: CPlus Combine Images combines 4 or 2 images into 1 and outputs an image and a mask.
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


import folder_paths
from PIL import Image, ImageOps, ImageSequence
import torch
import numpy as np

class ARD_4IMG_COMBINE:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "image_1": ("IMAGE",),
                    "image_2": ("IMAGE",),
                    "oreintation": (['over', 'beside'], {"default": 'beside'}),
                    "input_images": (['1 and 2 only', '4 images'], {"default": '4 images'}),
                    },
                "optional": {
                    "image_3": ("IMAGE",),
                    "image_4": ("IMAGE",),
                    },
                }

    RETURN_NAMES = ("Combined Image", "Image Mask",)
    RETURN_TYPES = ("IMAGE", "IMAGE",)

    FUNCTION = "combine_images_function"

    OUTPUT_NODE = True

    CATEGORY = "Ardenius"
    #my_code_start
    def combine_images_function(self, image_1, image_2, oreintation, input_images, image_3=None, image_4=None):
        if input_images == '4 images':
            imgs = [image_1, image_2, image_3, image_4]
        elif input_images == '1 and 2 only':
            imgs = [image_1, image_2]

        required_values = [image_1, image_2, oreintation, input_images]
        if None not in required_values and '' not in required_values:
            img_list = []
            for (batch_number, image) in enumerate(imgs):
                img_list.append(self.img_in_to_pil(image))
            if oreintation == 'beside' and input_images == '1 and 2 only':
                container_image_width = img_list[0].width + img_list[1].width
                if img_list[0].height > img_list[1].height:
                    container_image_height = img_list[0].height
                else:
                    container_image_height = img_list[1].height
            elif oreintation == 'over' and input_images == '1 and 2 only':
                container_image_height = img_list[0].height + img_list[1].height
                if img_list[0].width > img_list[1].width:
                    container_image_width = img_list[0].width
                else:
                    container_image_width = img_list[1].width
            else:
                container_image_width = img_list[0].width + img_list[1].width
                container_image_height = img_list[0].height + img_list[2].height

            init_image = Image.new('RGB', (container_image_width, container_image_height), 0)
            init_image.paste(img_list[0], box=tuple((0, 0, img_list[0].width, img_list[0].height)))
            if oreintation == 'beside' and input_images == '1 and 2 only':
                init_image.paste(img_list[1], box=tuple((img_list[0].width, 0, container_image_width, img_list[1].height)))
            elif oreintation == 'over' and input_images == '1 and 2 only':
                init_image.paste(img_list[1], box=tuple((0, img_list[0].height, img_list[1].width, img_list[0].height + img_list[1].height)))
            else:
                init_image.paste(img_list[1], box=tuple((img_list[0].width, 0, container_image_width, img_list[1].height)))

            if input_images == '4 images' and oreintation == 'beside':
                init_image.paste(img_list[2], box=tuple((0, img_list[0].height, img_list[2].width, img_list[0].height + img_list[2].height)))
                init_image.paste(img_list[3], box=tuple((img_list[2].width, img_list[0].height, img_list[2].width + img_list[3].width, img_list[1].height + img_list[3].height)))

            img_out, img_out_mask = self.pilimg_to_imgout(init_image)
        else:
            print('\n---\nCPlus Combine Images: required input values are not connected or provided correctly.\n---\n')
            img_out = None
            img_out_mask = None
        return (img_out, img_out_mask,)

    def img_in_to_pil(s, image_in):
        image_np = image_in.cpu().numpy().squeeze()
        image_np = (image_np * 255.0).astype(np.uint8)
        img = Image.fromarray(image_np, mode='RGB')
        return img

    def pilimg_to_imgout(s, img):
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))
        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]
        return output_image, output_mask
    #my_code_end
