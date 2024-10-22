#  licensed under General Public License v3.0 all rights reserved © 2024
#  ( author initials AMAA Nickname Ardenius contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium SD Models, ComfyUI custom nodes, and more to come)
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
