#  licensed under General Public License v3.0 all rights reserved © 2024
#  ( author initials AMAA Nickname Ardenius contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium Ardeniusai.com prompt engineer, text to image Models, ComfyUI custom nodes, and more to come)
#  below code is based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user as per the GPL V3.0 terms.

import os
import sys
import folder_paths
import importlib
ard_root_dir = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ard_root_dir)
# folder_paths.folder_names_and_paths["ComfyUI-Ardenius"] = os.path.dirname(os.path.abspath(__file__))

# Initialize dictionaries to store node mappings
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Iterate over files in the node directory
for file_name in os.listdir(ard_root_dir):
    if file_name.endswith('.py') and file_name != '__init__.py' and file_name != 'ard_lib.py':
        module_name = file_name[:-3]  # Remove the .py extension
        # print(f"\n{module_name}\n")
        try:
            module = importlib.import_module(module_name)
            for name, obj in module.__dict__.items():
                if callable(obj):  # Check if the object is a class
                    NODE_CLASS_MAPPINGS[name] = obj
                    NODE_DISPLAY_NAME_MAPPINGS[name] = f'{name.replace("_", " ").title()}'
        except Exception as e:
            print(f'Error importing module {module_name}: {e}')

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
#
# import os
# import sys
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# node_dir = os.path.dirname(parent_dir)
# sys.path.append(node_dir)
#
# # free nodes
# from .ard_nodes.ard_control_box import ARD_CONTROL_BOX
# from .ard_nodes.ard_text_box import ARD_TEXT_BOX
# from .ard_nodes.ard_dual_prompt import ARD_DUAL_PROMPT
#
# # premium nodes
# from .ard_nodes.ard_resize import ARD_RESIZE
# from .ard_nodes.ard_4latent_upscale import ARD_4LATENT_UPSCALE
# from .ard_nodes.ard_4img_combine import ARD_4IMG_COMBINE
# from .ard_nodes.ard_4crop_latent import ARD_4CROP_LATENT
# from .ard_nodes.ard_save_image import ARD_SAVE_IMAGE
# from .ard_nodes.ard_load_image import ARD_LOAD_IMAGE
# from .ard_nodes.ard_4vae_decode import ARD_4VAE_DECODE
# from .ard_nodes.ard_position import ARD_POSITION
# from .ard_nodes.ard_xy_scripts import ARD_XY_SCRIPTS
#
# NODE_CLASS_MAPPINGS = {
#     "ARD_CONTROL_BOX": ARD_CONTROL_BOX,
#     "ARD_TEXT_BOX": ARD_TEXT_BOX,
#     "ARD_DUAL_PROMPT": ARD_DUAL_PROMPT,
#     "ARD_RESIZE": ARD_RESIZE,
#     "ARD_4LATENT_UPSCALE": ARD_4LATENT_UPSCALE,
#     "ARD_4IMG_COMBINE": ARD_4IMG_COMBINE,
#     "ARD_4CROP_LATENT": ARD_4CROP_LATENT,
#     "ARD_SAVE_IMAGE": ARD_SAVE_IMAGE,
#     "ARD_LOAD_IMAGE": ARD_LOAD_IMAGE,
#     "ARD_4VAE_DECODE": ARD_4VAE_DECODE,
#     "ARD_POSITION": ARD_POSITION,
#     "ARD_XY_SCRIPTS": ARD_XY_SCRIPTS
# }
#
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "ARD_CONTROL_BOX": "ARD Control Box",
#     "ARD_TEXT_BOX": "ARD Text Box",
#     "ARD_DUAL_PROMPT": "ARD Dual Prompt",
#     "ARD_RESIZE": "ARD Resize",
#     "ARD_4LATENT_UPSCALE": "ARD Upscale 4 Latents",
#     "ARD_4IMG_COMBINE": "ARD Combine Images",
#     "ARD_4CROP_LATENT": "ARD 4 Crop Latent",
#     "ARD_SAVE_IMAGE": "ARD Save Image",
#     "ARD_LOAD_IMAGE": "ARD Load Image",
#     "ARD_4VAE_DECODE": "ARD 4 VAE Decode",
#     "ARD_POSITION": "ARD Position",
#     "ARD_XY_SCRIPTS": "ARD XY Scripts"
# }
#
# __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
