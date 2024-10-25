# ComfyUI Ardenius ARD Nodes 
## Don't forget to smile :) you deserve it !
#### Donations help in improving and making new free custom nodes and other software at [Coffee Page](https://ko-fi.com/ardenius) 
#### Change the mood ! by Visiting my [AI Image Gallery](https://ko-fi.com/ardenius/gallery)
#### See Member Perks [Free Custom nodes, AI Models, Embedding, Workflows, Image prompts, and exclusive content](https://ko-fi.com/ardenius/tiers). 

## [Get 50% Off Cloud GPU Servers with code Ardenius](https://bit.ly/ardenius)

## [Download link CPlus control box for ComfyUI](https://ko-fi.com/ardenius/shop)
## what's included in the custom nodes ?
1. ARD Control Box takes a model, vae and prompts input and outputs:
model, positive, negative, latent image, seed, width, height, cfg, steps, denoise, scaler, vae
2. ARD Math nodes: ComfyUI math nodes include ARD math which allows for divide, multiply, add, subtract in ComfyUI workflows, ARD integer to float, ARD remainder and more
3. ARD Resize: allows for resizing images
4. ARD Position: controls positioning of images in latent space 
5. ARD 4 latent decode: decodes 4 latents at the same time
6. ARD crop latent: crops a latent image into 4
7. ARD Save Image : is a ComfyUI work organizer that allows you to save images wherever you want and add metadata to your images 
8. ARD Load Image : lets you load images and will read and output your image saved metadata through ARD Save Image or standard ComfyUI save image
9. ARD Dual Prompt: takes negative and positive string as input and outputs negative and positive conditioning to be used in ksamplers
10. ARD xy scripts: allows you to test ComfyUI image generations using a range of steps, cfg, denoise 
11. ARD empty latent image: lets you set the shape dimension of the latent image example 8 for SDXL 16 for Flux. 

![](https://storage.ko-fi.com/cdn/useruploads/display/6f0dddf9-0697-4ef0-a772-2f189e0de6e2_comfyui_cplus_control_box.jpg)

### quick install 
1. go to ComfyUI/custom_nodes folder right click to open a terminal window 
2. type ```git clone https://github.com/ArdeniusAI/ComfyUI-Ardenius.git```
3. restart ComfyUI terminal 
4. click ( refresh ) on the comfy ui panel
5. double click anywhere on your workflow and search for ARD and nodes above will show up

### Manual install
IMPORTANT: if you download the zip file make sure to rename the folder to ( ComfyUI-Ardenius ) without the -main at the end
1. click on the green button above ( Code )
2. download zip file
3. extract the zip file
4. copy the contents to ComfyUI/custom-nodes/ 
5. restart your comfyui server
6. click ( refresh ) on the comfy ui panel
7. double click anywhere on your workflow and search for ARD and nodes above will show up
