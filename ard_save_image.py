"""
@author: initials AMAA
@title: Ardenius
@nickname: Ardenius
@description: ARD Save Image is a ComfyUI work organizer which allows you to save images in custom directories and meta tag them with custom information.
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
import json
import numpy as np
from PIL import Image
import datetime
from PIL.PngImagePlugin import PngInfo
import folder_paths
from comfy.cli_args import args
import ard_lib
from custom_nodes.comfyui_controlnet_aux.src.custom_detectron2.config import instantiate

current_directory = os.path.dirname(os.path.abspath(__file__))
ard_data = os.path.join(current_directory, "/ard_data")


class ARD_SAVE_IMAGE:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0

    #   my_code_start
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images_in": ("IMAGE", ),
                    },
                "optional": {
                    "saving_images": (["enabled", "disabled"], {"default": "enabled"}),
                    "save_txtprompt": (["enabled", "disabled"], {"default": "disabled"}),
                    "author_info_to_metadata": ("STRING", {"default": ""}),
                    "filename_prefix": ("STRING", {"default": ""}),
                    "filename_postfix": ("STRING", {"default": ""}),
                    "create_date_folders": (["enabled", "disabled"], {"default": "disabled"}),
                    "files_dir": ("STRING", {"default": "output"}),
                    "img_popup": (["enabled", "disabled"], {"default": "disabled"}),
                    "optimize_saved_image": (["enabled", "disabled"], {"default": "enabled"}),
                    "file_extension":  (["png", "webp", "jpeg", "bmp", "gif", "mpg", "mpeg", "hdf", "eps", "ps", "tif", "ico"], {"default": "png"}),
                    "save_basic_metadata": (["enabled", "disabled"], {"default": "enabled"}),
                    "civitai_metadata": (["enabled", "disabled"], {"default": "enabled"}),
                    "save_standard_metadata": (["enabled", "disabled"], {"default": "disabled"}),
                    "save_workflow_to_metadata": (["enabled", "disabled"], {"default": "disabled"}),
                    "show_terminal_notifications": (["enabled", "disabled"], {"default": "disabled"}),
                    },
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_NAMES = ("images_out",)
    RETURN_TYPES = ("IMAGE",)

    FUNCTION = "ard_save_images"

    OUTPUT_NODE = True

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Save Image is a ComfyUI work organizer which allows you to save images in custom directories and meta tag them with custom information."

    def ard_save_images(self, images_in, filename_prefix, save_standard_metadata, files_dir, author_info_to_metadata, save_txtprompt, optimize_saved_image, filename_postfix, saving_images, file_extension, show_terminal_notifications, img_popup, save_workflow_to_metadata, create_date_folders, save_basic_metadata, civitai_metadata, prompt=None, extra_pnginfo=None):
        basic_meta = None
        if saving_images.strip() == 'enabled':
            d_now = datetime.date.today()
            date_str = str(d_now)

            filename_prefix += self.prefix_append

            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images_in[0].shape[1], images_in[0].shape[0])
            results = list()

            if os.path.exists(files_dir):
                full_output_folder = files_dir
            else:
                try:
                    os.mkdir(os.path.join(os.getcwd(), files_dir))
                    full_output_folder = os.path.join(os.getcwd(), files_dir)
                except Exception as e:
                    print(f'\n---\nError: you can not create (nested new directories) (ex. new_folder/new_sub_folder). you can create the top folder then create new folders inside it.\n---\n')

            cust_nodes_dir = self.output_dir.replace('/output', '/custom_nodes')

            if file_extension != "png" and (save_workflow_to_metadata.strip() == 'enabled' or save_standard_metadata.strip() == 'enabled' or save_basic_metadata.strip() == 'enabled'):
                if show_terminal_notifications == 'enabled':
                    print("\nARD Save Image: no metadata or workflow will be saved in the image since image format is not (png)\n---\ns")

            if create_date_folders.strip() == 'enabled':
                full_output_folder = os.path.join(full_output_folder, date_str)
                if not os.path.exists(full_output_folder):
                    os.mkdir(full_output_folder)

            counter = 1

            read_file = os.path.join(ard_data, 'temp_data.json')
            if os.path.exists(read_file):
                loaded_img_info = ard_lib.read_dict_from_json(read_file)
            else:
                loaded_img_info = None

            if loaded_img_info is not None or loaded_img_info != {}:
                try:
                    initial_meta = self.prompt_get_values(prompt)
                    initial_keys = initial_meta.keys()
                    loaded_meta = loaded_img_info
                    basic_meta = initial_meta
                    for keys in loaded_meta:
                        if keys not in initial_keys:
                            basic_meta[keys] = loaded_meta[keys]
                        if keys == 'seed' and (initial_meta['seed'] < 100 or initial_meta['seed'] is not int):
                            basic_meta['seed'] = loaded_meta['seed']
                        if keys == 'positive' and initial_meta['positive'] == '':
                            basic_meta['positive'] = loaded_meta['positive']
                        if keys == 'negative' and initial_meta['negative'] == '':
                            basic_meta['negative'] = loaded_meta['negative']
                except Exception as e:
                    if show_terminal_notifications == 'enabled':
                        print(f"ARD Save Image: no info in image metadata. checking ComfyUI standard metadata\n{e}")
                    else:
                        pass
            else:
                basic_meta = self.prompt_get_values(prompt)

            for image in images_in:
                i = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                metadata = None
                width = img.width
                height = img.height
                if not args.disable_metadata:
                    metadata = PngInfo()
                    if author_info_to_metadata.strip() != '':
                        metadata.add_text("owner_info", json.dumps(author_info_to_metadata.strip()))
                    if save_basic_metadata.strip() == 'enabled':
                        metadata.add_text("basic_metatags", json.dumps(basic_meta))
                        if show_terminal_notifications == 'enabled':
                            print(f"\nARD Save Image: basic metadata added to image {counter}\n")

                    if civitai_metadata == 'enabled':
                        if basic_meta.get("ckpt_name", "") != "" and os.path.exists(basic_meta.get("ckpt_name", "")):
                            model_hash = ard_lib.sha256_hash_file(str(basic_meta.get("ckpt_name", "")))
                            # print("**************************")
                            # print(f"model hash: {model_hash}")
                            # print("**************************")
                        else:
                            model_path = basic_meta.get("ckpt_name", "")
                            # print("**************************")
                            # print(f"no model hash generated: {model_path}")
                            # print("**************************")
                            model_hash = ""

                        parameters_str = str(basic_meta.get('positive', "")) + ' Negative prompt: ' + str(basic_meta.get('negative', "")) + "."
                        # second_str = "Steps: " + str(basic_meta["steps"]) + ", Sampler: " + str(basic_meta.get('sampler_name', '')) + ", CFG scale: " + str(basic_meta['cfg']) + ", Seed: " + str(basic_meta['seed']) + f", Size: {img.width}x{img.height}" + ", Denoising strength: " + str(basic_meta['denoise']) + ", Model: " + str(os.path.basename(basic_meta['ckpt_name'].replace('.safetensors', '')))
                        second_str = "Steps: " + str(basic_meta.get("steps", 7)) + ", Sampler: " + str(basic_meta.get('sampler_name', '')) + ", CFG scale: " + str(basic_meta['cfg']) + ", Seed: " + str(basic_meta.get('seed', 1234)) + f", Size: {img.width}x{img.height}" + ", Denoising strength: " + str(basic_meta.get('denoise', 1.0)) + f", VAE: " + str(basic_meta.get("vae", "")) + ", Model hash: " + str(model_hash) + ", Model: " + str(os.path.basename(str(basic_meta.get('ckpt_name', '')).replace('.safetensors', '')))
                        metadata.add_text("parameters", parameters_str + '\n' + second_str)

                    if save_standard_metadata.strip() == 'enabled':
                        metadata.add_text("prompt", json.dumps(prompt))
                        if show_terminal_notifications == 'enabled':
                            print(f"\nARD Save Image: standard ComfyUI metadata added to image {counter} \n---\n")

                    if extra_pnginfo is not None and save_workflow_to_metadata.strip() == "enabled":
                        for xi in extra_pnginfo:
                            metadata.add_text(xi, json.dumps(extra_pnginfo[xi]))
                        if show_terminal_notifications == 'enabled':
                            print(f"\nARD Save Image: workflow metadata added to image {counter} ")

                    metadata.add_text("generation software", 'generated using Ardenius AI ARD ComfyUI Nodes found at https://ko-fi.com/ardenius email: ardenius7@gmail.com')
                    if show_terminal_notifications == 'enabled':
                        print("ARD Save Image: generation software info added to image")
                else:
                    if show_terminal_notifications == 'enabled':
                        print(f'ARD Save Image: no meta data was saved in the image. disabled from main ComfyUI settings')

                file = f"{filename_prefix}{counter}{filename_postfix}.{file_extension}"
                image_path = os.path.join(full_output_folder, file)

                if os.path.exists(image_path):
                    while os.path.exists(image_path):
                        counter += 1
                        file = f"{filename_prefix}{counter}{filename_postfix}.{file_extension}"
                        image_path = os.path.join(full_output_folder, file)

                if optimize_saved_image.strip() == 'enabled':
                    optimize = True
                else:
                    optimize = False

                img.save(image_path, pnginfo=metadata, optimize=optimize, compress_level=self.compress_level)
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })
                if show_terminal_notifications == 'enabled':
                    print(f"\n---\nimage {counter} file saved")
                if img_popup.strip() == 'enabled':
                    img.show(image_path)

                if save_txtprompt.strip() == 'enabled':
                    txt_prompt_file = f"{filename_prefix}{counter}{filename_postfix}.txt"
                    txt_prompt_file_path = os.path.join(full_output_folder, txt_prompt_file)
                    with open(txt_prompt_file_path, 'w', buffering=1) as f_txt:
                        prompt_txt = str(basic_meta.get("positive", ""))
                        f_txt.write(prompt_txt)
                counter += 1

        if basic_meta is not None and save_basic_metadata == "enabled" and show_terminal_notifications == "enabled":
            print(f"\n*********************\nARD Save Image: saved image info")
            for key in basic_meta.keys():
                print(f"{key}: {basic_meta.get(key)}")
            print("*********************")
        return (images_in,)

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
        positive = ""
        negative = ""
        positive_not_found = True
        negative_not_found = True
        for keys in prompt_keys1:
            for sub_keys in prompt_in[keys].keys():
                if sub_keys == 'inputs':
                    for sub_sub_keys in prompt_in[keys][sub_keys]:
                        # print(f'sub sub key: {sub_sub_keys}')
                        if sub_sub_keys == 'seed':
                            seed = prompt_in[keys][sub_keys].get('seed', None)
                            seed = s.if_list(seed)
                            if isinstance(seed, int) and seed is not None:
                                prompt_dict.update({"seed": seed})
                        if sub_sub_keys == 'steps':
                            steps = prompt_in[keys][sub_keys].get('steps', None)
                            steps = s.if_list(steps)
                            if steps is not None and isinstance(steps, int):
                                prompt_dict.update({"steps": steps})
                        if sub_sub_keys == 'cfg':
                            cfg = prompt_in[keys][sub_keys].get('cfg', None)
                            cfg = s.if_list(cfg)
                            if cfg is not None and isinstance(cfg, float):
                                prompt_dict.update({"cfg": cfg})
                        if sub_sub_keys == 'sampler_name':
                            sampler_name = prompt_in[keys][sub_keys].get('sampler_name', None)
                            sampler_name = s.if_list(sampler_name)
                            if sampler_name is not None and isinstance(sampler_name, str):
                                prompt_dict.update({"sampler_name": sampler_name})
                        if sub_sub_keys == 'scheduler':
                            scheduler = prompt_in[keys][sub_keys].get('scheduler', None)
                            scheduler = s.if_list(scheduler)
                            if scheduler is not None and isinstance(scheduler, str):
                                prompt_dict.update({"scheduler": scheduler})
                        if sub_sub_keys == 'denoise':
                            denoise = prompt_in[keys][sub_keys].get('denoise', None)
                            denoise = s.if_list(denoise)
                            if denoise is not None and isinstance(denoise, float):
                                prompt_dict.update({"denoise": denoise})
                        if sub_sub_keys == 'ckpt_name':
                            ckpt_name = prompt_in[keys][sub_keys].get('ckpt_name', None)
                            ckpt_name = s.if_list(ckpt_name)
                            if ckpt_name is not None and isinstance(ckpt_name, str):
                                prompt_dict.update({"ckpt_name": str(ckpt_name)})
                        if sub_sub_keys == 'MODEL':
                            ckpt_name = prompt_in[keys][sub_keys].get("MODEL", "not_found")
                            ckpt_name = s.if_list(ckpt_name)
                            prompt_dict.update({"ckpt_name": str(ckpt_name)})
                        if sub_sub_keys == 'lora_name':
                            lora_name = prompt_in[keys][sub_keys]['lora_name']
                            lora_name = s.if_list(lora_name)
                            prompt_dict.update({"lora_name": lora_name})
                        if sub_sub_keys == 'vae':
                            if isinstance(prompt_in[keys][sub_keys]['vae'], str):
                                vae = prompt_in[keys][sub_keys]['vae']
                                vae = s.if_list(vae)
                                prompt_dict.update({"vae": vae})
                        if sub_sub_keys == 'pos_text' or sub_sub_keys == "text" or sub_sub_keys == "positive" or "positive" in sub_sub_keys or "pos" in sub_sub_keys or sub_sub_keys == "add_text" or sub_sub_keys == "input_text":
                            search_keys = ["pos_text", "positive", "text", "add_text", "input_text"]
                            found_in_text = False
                            for search_item in search_keys:
                                get_value = prompt_in[keys][sub_keys].get(search_item, None)
                                if get_value is not None :
                                    if isinstance(get_value, str) and get_value != "" and "negative" not in get_value and "neg" not in get_value and "ugly" not in get_value and "blur" not in get_value:
                                        if get_value not in positive:
                                            if positive != "" and search_item == "text":
                                                pass
                                            else:
                                                positive += str(get_value) + " "
                                                prompt_dict.update({"positive": positive})
                                                positive_not_found = False
                                            if search_item == "text":
                                                found_in_text = True
                                            print(f'\npositive in search: {positive}')

                            if positive == "" and positive_not_found and sub_sub_keys == "text":
                                positive_init = prompt_in[keys][sub_keys].get("text", "")
                                if isinstance(positive_init, str) and positive_init != "":
                                    positive = positive_init + " "
                                    prompt_dict.update({"positive": positive})
                                    positive_not_found = False
                                    print(f'\npositive in text: {positive}')

                        if sub_sub_keys == 'neg_text' or sub_sub_keys == 'text' or sub_sub_keys == "negative" or "negative" in sub_sub_keys or "neg" in sub_sub_keys or sub_sub_keys == "add_text" or sub_sub_keys == "input_text":
                            search_keys = ["neg_prompt", "negative", "text", "neg_text", "add_text", "input_text"]

                            for search_item in search_keys:
                                get_value = prompt_in[keys][sub_keys].get(search_item, None)
                                if get_value is not None:
                                    if isinstance(get_value, str) and get_value != "" and get_value not in positive and "positive" not in get_value and "pos" not in get_value or "negative" in get_value or "neg" in get_value:
                                        negative += str(get_value) + " "
                                        if negative in positive:
                                            positive = positive.replace(negative, "")
                                            prompt_dict.update({"positive": positive})
                                        prompt_dict.update({"negative": negative})
                                        if search_item != "neg_text":
                                            negative_not_found = False
                                        print(f'\nnegative in search: {negative}\n')

                            if negative == "" and not positive_not_found and negative_not_found and sub_sub_keys == "text":
                                negative_init = prompt_in[keys][sub_keys].get("text", "")
                                if isinstance(negative_init, str) and negative_init != "":
                                    negative += negative_init + " "
                                    prompt_dict.update({"negative": negative})
                                    negative_not_found = False
                                    print(f'\nnegative in text: {negative}\n')
        return prompt_dict
    # my_code_end
