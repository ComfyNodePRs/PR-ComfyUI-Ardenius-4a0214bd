"""
@author: initials AMAA
@title: Ardenius AI
@nickname: Ardenius
@description: ARD Load Image outputs images generation information when saved through ARD Save Image or ComfyUI.
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

import os
import folder_paths
import node_helpers
import torch
import json
import numpy as np
from PIL import Image, ImageOps, ImageSequence
import random
import hashlib
import ard_lib
ard_data = "/ard_data"


class ARD_LOAD_IMAGE:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                {
                    "image": (sorted(files), {"image_upload": True}),
                },
                "optional":
                {
                    "get_img_info": (["enabled", "disabled"], {"default": "enabled", "tooltip": "if saved by CPlus Save Image will extract its info - if disabled disables outputs except image, mask, width, and height"}),
                    "seed_from": (["loaded image", "random"], {"default": "loaded image", "tooltip": "pick random seed or the image seed if saved by CPlus Save Image"}),
                    "terminal_info": (["print", "dont print"], {"default": "print", "tooltip": "print image information to the terminal window or not"}),
                }
                }

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Load Image outputs images generation information when saved through ARD Save Image or ComfyUI"
    RETURN_NAMES = ("Image", "Mask", "pos_text", "neg_text", "seed", "steps", "cfg", "denoise", "Width", "Height")
    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "INT", "INT", "FLOAT", "FLOAT", "INT", "INT")
    FUNCTION = "ard_load_image"

    # my_code_start
    def ard_load_image(self, image, get_img_info, seed_from, terminal_info):
        checkpoint_p = "no check point"
        seed_p = 123
        positive_p = "error terminal"
        negative_p = "blur, distortion"
        steps_p = 10
        cfg_p = 3.0
        width = 1024
        height = 1024
        sampler_name_p = "dpmpp_sde_gpu"
        scheduler_p = "sgm uniform"
        denoise_p = 1.0

        image_path = folder_paths.get_annotated_filepath(image)

        img = node_helpers.pillow(Image.open, image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ['MPO']

        for i in ImageSequence.Iterator(img):
            i = node_helpers.pillow(ImageOps.exif_transpose, i)

            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            if len(output_images) == 0:
                w = image.size[0]
                h = image.size[1]
                width = w
                height = h

            if image.size[0] != w or image.size[1] != h:
                continue

            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        # my_code_start
        info_found = False
        meta_info = None

        try:
            meta_info = json.loads(img.info["basic_metatags"])
            info_found = True
            if terminal_info == "print":
                print("\nARD Load Image: found image info basic metatags\n")
        except Exception as e:
            if terminal_info == "print":
                print(f"\nARD Load Image: image not saved using ARD Save Image no info extracted.\n")

        if meta_info is None and not info_found:
            try:
                meta_info = self.prompt_get_values(json.loads(img.info["prompt"]))
                info_found = True
                if terminal_info == "print":
                    print("\nARD Load Image: found image info standard ComfyUI metadata\n")
            except Exception as e:
                if terminal_info == "print":
                    print(f"\nARD Load Image: not saved using ComfyUI standard metadata or workflow no info extracted.\n")

        if meta_info is not None and info_found:
            if "png" in str(os.path.basename(image_path)) and get_img_info == "enabled":
                try:
                    checkpoint_p = meta_info.get("ckpt_name", "no check point")
                    if "/" in checkpoint_p:
                        try:
                            checkpoint_p = os.path.basename(checkpoint_p).split(".")[0]
                        except:
                            pass
                    seed_p = meta_info.get("seed", 1234)
                    positive_p = meta_info.get("positive", "error terminal")
                    negative_p = meta_info.get("negative", "blur, distortion")
                    steps_p = meta_info.get("steps", 7)
                    cfg_p = meta_info.get("cfg", 3.0)
                    sampler_name_p = meta_info.get("sampler_name", "euler") # this was sampler_name
                    scheduler_p = meta_info.get("scheduler", "normal")
                    denoise_p = meta_info.get("denoise", 1.0)
                    json_file_path = os.path.join(ard_data, 'temp_data.json')
                    # print(f"\njson file: {json_file_path}\n")
                    image_info_dict = {"checkpoint": checkpoint_p, "seed": seed_p, "positive": positive_p, "negative": negative_p, "steps": steps_p, "cfg": cfg_p, "sampler_name": sampler_name_p, "scheduler": scheduler_p, "denoise": denoise_p}
                    try:
                        ard_lib.save_dict_to_json(image_info_dict, json_file_path)
                    except:
                        pass
                    if terminal_info == "print":
                        print(f"\n*********************\nARD Load Image: Information extracted from the image\nImage path: {image_path}\ncheckpoint: {checkpoint_p}\nseed: {seed_p}\npositive: {positive_p}\nnegative:{negative_p}\nsteps: {steps_p}\ncfg: {cfg_p}\nsampler_name: {sampler_name_p}\nscheduler: {scheduler_p}\ndenoise: {denoise_p}\n*********************\n")
                    info_found = True
                except Exception as e:
                    info_found = False
                    if terminal_info == "print":
                        print(f"\nARD Load Image: no info found in the image \nonly use image, mask, width , height\nmake sure to save using ARD Save Image\n{e}")
            else:
                info_found = False
                if terminal_info == "print":
                    print(f"\nARD Load Image: no generation info found in image setting defaults\nskipping info extraction\nonly use image, mask, width , height\n")
        else:
            info_found = False
            # setting defaults
            checkpoint_p = "no check point"
            seed_p = 1234
            positive_p = "error terminal"
            negative_p = "blur, distortion"
            steps_p = 7
            cfg_p = 3.0
            sampler_name_p = "euler"
            scheduler_p = "normal"
            denoise_p = 1.0

        if (seed_from == "random") or not info_found or meta_info is None:
            seed_p = int(random.random() * 1e10)
        positive_t = positive_p
        negative_t = negative_p

        return (output_image, output_mask, positive_t, negative_t, seed_p, steps_p, cfg_p, denoise_p, width, height)

    @classmethod
    def if_list(s, variable_in):
        if type(variable_in) is list:
            output_value = variable_in[-1]
        else:
            output_value = variable_in
        return output_value

    @classmethod
    def prompt_get_values(s, prompt_in):
        prompt_keys1 = prompt_in.keys()
        prompt_dict = {}
        positive_not_found = True
        negative_not_found = True
        for keys in prompt_keys1:
            # print(f'{keys}\n')
            for sub_keys in prompt_in[keys].keys():
                # print(f'sub key: {sub_keys}')
                if sub_keys == 'inputs':
                    for sub_sub_keys in prompt_in[keys][sub_keys]:
                        # print(f'sub sub key: {sub_sub_keys}')
                        if sub_sub_keys == 'seed':
                            seed = prompt_in[keys][sub_keys]['seed']
                            seed = s.if_list(seed)
                            prompt_dict.update({"seed": seed})
                        if sub_sub_keys == 'steps':
                            steps = prompt_in[keys][sub_keys]['steps']
                            steps = s.if_list(steps)
                            prompt_dict.update({"steps": steps})
                        if sub_sub_keys == 'cfg':
                            cfg = prompt_in[keys][sub_keys]['cfg']
                            cfg = s.if_list(cfg)
                            prompt_dict.update({"cfg": cfg})
                        if sub_sub_keys == 'sampler_name':
                            sampler_name = prompt_in[keys][sub_keys]['sampler_name']
                            sampler_name = s.if_list(sampler_name)
                            prompt_dict.update({"sampler_name": sampler_name})
                        if sub_sub_keys == 'scheduler':
                            scheduler = prompt_in[keys][sub_keys]['scheduler']
                            scheduler = s.if_list(scheduler)
                            prompt_dict.update({"scheduler": scheduler})
                        if sub_sub_keys == 'denoise':
                            denoise = prompt_in[keys][sub_keys]['denoise']
                            denoise = s.if_list(denoise)
                            prompt_dict.update({"denoise": denoise})
                        if sub_sub_keys == 'ckpt_name':
                            ckpt_name = prompt_in[keys][sub_keys]['ckpt_name']
                            ckpt_name = s.if_list(ckpt_name)
                            prompt_dict.update({"ckpt_name": ckpt_name})
                        if sub_sub_keys == 'vae':
                            if isinstance(prompt_in[keys][sub_keys]['vae'], str):
                                vae = prompt_in[keys][sub_keys]['vae']
                                vae = s.if_list(vae)
                                prompt_dict.update({"vae": vae})
                        # if sub_sub_keys == ('text' or 'pos_text') and positive_not_found:
                        if sub_sub_keys == 'pos_text':
                            pos_init = prompt_in[keys][sub_keys]['pos_text']
                            if isinstance(pos_init, str):
                                positive = prompt_in[keys][sub_keys]['pos_text']
                                positive = s.if_list(positive)
                                prompt_dict.update({"positive": positive})
                                positive_not_found = False
                        if (sub_sub_keys == 'text' and positive_not_found):
                            positive = prompt_in[keys][sub_keys]['text']
                            positive = s.if_list(positive)
                            prompt_dict.update({"positive": positive})
                            positive_not_found = False
                            # print(f'\n---\nsub sub key input text: {sub_sub_keys}\n---\n')
                        if sub_sub_keys == 'neg_text':
                            neg_init = prompt_in[keys][sub_keys]['neg_text']
                            if isinstance(neg_init, str):
                                negative = prompt_in[keys][sub_keys]['neg_text']
                                negative = s.if_list(negative)
                                prompt_dict.update({"negative": negative})
                                negative_not_found = False
                        if sub_sub_keys == 'text' and negative_not_found:
                            negative = prompt_in[keys][sub_keys]['text']
                            negative = s.if_list(negative)
                            prompt_dict.update({"negative": negative})
                            negative_not_found = False
        # print(f'output of the function: {prompt_dict}')
        return prompt_dict

    # my_code_end
    @classmethod
    def IS_CHANGED(s, image, get_img_info='', seed_from='', terminal_info=''):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True