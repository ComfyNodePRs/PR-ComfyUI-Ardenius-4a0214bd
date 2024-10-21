# ARD ComfyUI Ardenius nodes

#### Donations help in imporoving and making new free custom nodes and other software at [Coffee Page](https://ko-fi.com/ardenius) 
#### Change the mood ! by Visiting my [AI Image Gallery](https://ko-fi.com/ardenius/gallery)
#### See Member Perks [Free Custom nodes, AI Models, Embedding, Workflows, Image prompts, and exclusive content](https://ko-fi.com/ardenius/tiers). 

## [Download link ARD control box for ComfyUI](https://ko-fi.com/s/2e67e2ae70)
## what nodes are in this ComfyUI custom nodes download ?
1. ARD Control Box :
my favorite node :) read below for details.
2. ARD Dual Prompt:
combines negative and positive in 1 node
3. ARD Text Box:
text box that outputs a text string
4. ARD math node : takes 2 float inputs and does math operations on them and outputs either integer or float 
5. ARD integer: allows adding an integer variable 
6. ARD float: allows adding a float variable 
7. ARD integer to float : converts an integer to float
   
(Will be adding new free nodes to this package so make sure to follow me on this ko-fi page in the top right for future releases )

the ARD control box gets a model and prompts input and outputs:
model, positive, negative, latent image, seed, width, height, cfg, steps, denoise, scaler, clip, vae

![](https://storage.ko-fi.com/cdn/useruploads/display/6f0dddf9-0697-4ef0-a772-2f189e0de6e2_comfyui_cplus_control_box.jpg)

this is one of my favorite custom nodes especially when dealing with large workflows with multiple Ksamplers with the same values for inputs.
ARD Control Box custom node does the following:

1. takes model and prompt inputs so it can allow for adding LoRas as you like.

2. you'll have the following to controls as outputs in one node instead of many:

model, positive, negative, latent image, seed, width, height, cfg, steps, denoise, scaler, clip, vae

### Manual install
IMPORTANT: if you download the zip file make sure to rename the folder to ( ComfyUI-Ardenius ) instead of ( ComfyUI-Ardenius-main ) without the -main at the end
1. click on the green button above ( Code )
2. download zip file
3. extract the zip file
4. copy the contents to ComfyUI/custom-nodes/ 
5. restart your comfyui server
6. click ( refersh ) on the comfy ui panel
7. double click anywhere on your workflow and search for CPlus control box 
