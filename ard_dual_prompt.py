"""
@author: initials AMAA
@title: Ardenius AI
@nickname: Ardenius
@description: ARD Dual Prompt can be used for positive and negative prompts converts string text input to conditioning prompt.
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

MAX_RESOLUTION = 8192

class ARD_DUAL_PROMPT:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pos_text": ("STRING", {"multiline": True, "dynamicPrompts": True, "tooltip": "The text to be encoded."}),
                "clip": ("CLIP", {"tooltip": "The CLIP model used for encoding the text."})
            },
            "optional": {
                "neg_text": ("STRING", {"dynamicPrompts": True, "tooltip": "The text to be encoded."}),
            }
        }

    RETURN_NAMES = ("pos_prompt", "neg_prompt")
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    OUTPUT_TOOLTIPS = ("A conditioning containing the embedded text used to guide the diffusion model.",)
    FUNCTION = "ard_dual_prompt"

    CATEGORY = "Ardenius"
    DESCRIPTION = "ARD Dual Prompt can be used for positive and negative prompts converts string text input to conditioning prompt"

    def ard_dual_prompt(self, clip, pos_text, neg_text):
        pos_cond = None
        neg_cond = None
        try:
            try:
                if not isinstance(pos_text, str):
                    pos_text = str(pos_text)
                    print(f"\nARD Dual Prompt: no positive prompt found in this image disconnect ARD Dual Prompt and add positive and negative prompts\npos_text: {pos_text}\n")
                pos_tokens = clip.tokenize(pos_text)
                pos_output = clip.encode_from_tokens(pos_tokens, return_pooled=True, return_dict=True)
                pos_cond = pos_output.pop("cond")
            except Exception as e:
                print(f"ARD Dual Prompt: positive prompt \n{e}")
            try:
                if not isinstance(pos_text, str):
                    neg_text = str(neg_text)
                    print(f"neg_text: {neg_text}\n")
                neg_tokens = clip.tokenize(neg_text)
                neg_output = clip.encode_from_tokens(neg_tokens, return_pooled=True, return_dict=True)
                neg_cond = neg_output.pop("cond")
            except Exception as e:
                print(f"ARD Dual Prompt: negative prompt \n{e}")

            if pos_cond is not None:
                return ([[pos_cond, pos_output]], [[neg_cond, neg_output]], )
            else:
                print("**************************************************************")
                print("ARD Dual Prompt: the clip for this model is not set correctly. or memory overload click Manager then on bottom left click Unload Models then try again.")
                print("**************************************************************")
        except Exception as e:
            print("************************************************************************************")
            print(f"ARD Dual Prompt: check clip settings. or memory overload click Manager then on bottom left click Unload Models then try again.")
            print("************************************************************************************")



