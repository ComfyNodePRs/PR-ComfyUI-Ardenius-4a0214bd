"""
@author: initials AMAA
@title: Ardenius
@nickname: Ardenius
@description: ARD XY Tester is for testing images using a range of steps, cfg, or denoise in ComfyUI.
"""
#  licensed under General Public License v3.0 all rights reserved © 2024
#  ( author initials AMAA Nickname Ardenius contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius in the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Support me by getting Premium Members only Perks (Premium Ardeniusai.com prompt engineer, text to image Models, ComfyUI custom nodes, and more to come)
#  below code is based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user as per the GPL V3.0 terms.


import os.path
import folder_paths
import json

MAX_RESOLUTION = 8192


class ARD_XY_SCRIPTS:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
                    "activate": (["On", "Off"], {"default": "On"}),
                    "trigger_seed": ("INT", {"default": 1234}),
                    },
                "optional": {
                    "width": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "height": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "start_cfg": ("FLOAT", {"default": 1, "min": 0.1, "max": 15, "step": 0.1}),
                    "end_cfg": ("FLOAT", {"default": 8, "min": 0.1, "max": 15, "step": 0.1}),
                    "step_cfg": ("FLOAT", {"default": 1, "min": 0.1, "max": 15, "step": 0.1}),
                    "start_steps": ("INT", {"default": 1, "min": 1, "max": 100, "step": 1}),
                    "end_steps": ("INT", {"default": 20, "min": 1, "max": 100, "step": 1}),
                    "step_steps": ("INT", {"default": 1, "min": 1, "max": 100, "step": 1}),
                    "start_denoise": ("FLOAT", {"default": 0.1, "min": 0.01, "max": 1.0, "step": 0.01}),
                    "end_denoise": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 1.0, "step": 0.01}),
                    "step_denoise": ("FLOAT", {"default": 0.1, "min": 0.01, "max": 1.0, "step": 0.01}),
                    },
                }

    RETURN_NAMES = ("width", "height", "cfg", "steps", "denoise", "seed_out")
    RETURN_TYPES = ("INT", "INT", "FLOAT", "INT", "FLOAT", "INT",)

    FUNCTION = "ard_xy_scripts"

    OUTPUT_NODE = True

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD XY Tester is for testing images using a range of steps, cfg, or denoise in ComfyUI."
    # my_code_start
    def ard_xy_scripts(self, activate, width, height, start_cfg, end_cfg, step_cfg, start_steps, end_steps, step_steps, start_denoise, end_denoise, step_denoise, trigger_seed):

        if activate == 'On':
            xy_dict = {}
            xy_dict_in = {}
            cfg = start_cfg
            steps = start_steps
            denoise = start_denoise
            xy_dict_in['xy_input'] = {"width": width, "height": height, "start_cfg": start_cfg, "end_cfg": end_cfg,
                                   "step_cfg": step_cfg, "start_steps": start_steps, "end_steps": end_steps,
                                   "step_steps": step_steps, "start_denoise": start_denoise,
                                   "end_denoise": end_denoise, "step_denoise": step_denoise}
            xy_dict_in['xy_current'] = {"cfg": cfg, "steps": steps, "denoise": denoise}

            node_dir = os.path.join(os.getcwd(), "custom_nodes/ComfyUI-Ardenius")
            json_file = os.path.join(node_dir, "data/xy_data.json")

            if os.path.exists(json_file):
                xy_dict = self.read_data(json_file)
                if xy_dict['xy_input'] != xy_dict_in['xy_input']:
                    xy_dict['xy_input'] = xy_dict_in['xy_input']
                cfg = xy_dict['xy_current']['cfg']
                steps = xy_dict['xy_current']['steps']
                denoise = xy_dict['xy_current']['denoise']
                xy_dict = self.update_steps(xy_dict)
                xy_dict = self.write_data(xy_dict, json_file)
            else:
                xy_dict = self.write_data(xy_dict_in, json_file)
                cfg = xy_dict['xy_current']['cfg']
                steps = xy_dict['xy_current']['steps']
                denoise = xy_dict['xy_current']['denoise']

            remainder = width % 8
            width = width + remainder

            remainder = height % 8
            height = height + remainder

        else:
            cfg = 8
            steps = 20
            denoise = 8
            print('\n---\nCPlus XY Script is off and set to defaults:\nsteps: 20\ncfg: 8\ndenoise: 1\n---\n')

        return width, height, cfg, steps, denoise, trigger_seed

    def update_steps(s, xy_dict):
        if int(xy_dict['xy_current']['steps']) < int(xy_dict['xy_input']['end_steps']):
            xy_dict['xy_current'].update({"steps": xy_dict['xy_current']['steps'] + xy_dict['xy_input']['step_steps']})
            print(f"\n---\nCPlus XY Script : executing step {xy_dict['xy_current']['steps']}\n---\n")
        else:
            xy_dict['xy_current'].update({"steps": xy_dict['xy_input']['start_steps']})

        if float(xy_dict['xy_current']['cfg']) < float(xy_dict['xy_input']['end_cfg']):
            xy_dict['xy_current'].update({"cfg": xy_dict['xy_current']['cfg'] + xy_dict['xy_input']['step_cfg']})
            print(f"\n---\nCPlus XY Script : executing cfg {xy_dict['xy_current']['cfg']}\n---\n")
        else:
            xy_dict['xy_current'].update({"steps": xy_dict['xy_input']['start_cfg']})

        if float(xy_dict['xy_current']['denoise']) < float(xy_dict['xy_input']['end_denoise']):
            xy_dict['xy_current'].update({"denoise": xy_dict['xy_current']['denoise'] + xy_dict['xy_input']['step_denoise']})
            print(f"\n---\nCPlus XY Script : executing denoise {xy_dict['xy_current']['denoise']}\n---\n")
        else:
            xy_dict['xy_current'].update({"steps": xy_dict['xy_input']['start_denoise']})
        return xy_dict

    def write_data(s,data_dict, data_file):
        with open(data_file, 'w') as wdf:
            json_data = json.dumps(data_dict)
            wdf.write(json_data)
            data_dict = json.loads(json_data)
            return data_dict

    def read_data(s,data_file):
        if os.path.exists(data_file):
            with open(data_file, 'r') as rdf:
                json_data = json.load(rdf)
                output_dict = json.loads(json_data)
                return output_dict
        else:
            print(f'\n---\ndata file {data_file} not found\n---\n')
            return None
    # my_code_end
