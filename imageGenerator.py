
# from diffusers import StableDiffusionPipeline,LMSDiscreteScheduler , DPMSolverMultistepScheduler
#
# model_id = "runwayml/stable-diffusion-v1-5"
# pipe = StableDiffusionPipeline.from_pretrained(model_id)
# pipe.scheduler = LMSDiscreteScheduler.from_config(pipe.scheduler.config)
# prompt = "a photo of an astronaut riding a horse on mars"
# image = pipe(prompt,height=256,width=256,num_inference_steps=10).images[0]
# image.save("astronaut_rides_horse.png")


import torch
from diffusers import LCMScheduler, AutoPipelineForText2Image

model_id = "Lykon/dreamshaper-7"
adapter_id = "latent-consistency/lcm-lora-sdv1-5"

pipe = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)

# load and fuse lcm lora
pipe.load_lora_weights(adapter_id)
pipe.fuse_lora()


prompt = "Self-portrait oil painting, a beautiful cyborg with golden hair, 8k"

# disable guidance_scale by passing 0
image = pipe(prompt=prompt, num_inference_steps=4, guidance_scale=0).images[0]
