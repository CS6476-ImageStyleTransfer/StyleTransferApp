import torch
import os
import numpy as np
import argparse
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.utils as vutils
from networks.CartoonGAN import CartoonGAN

def cartoon_gan_transform(input_image, style, load_size=450, model_path='./trained_models/CartoonGAN'):
	model = CartoonGAN()
	model.load_state_dict(torch.load(os.path.join(model_path, style + '_net_G_float.pth')))
	model.eval()
	model.float()

	h = input_image.size[0]
	w = input_image.size[1]
	ratio = h * 1.0 / w
	if ratio > 1:
		h = int(load_size)
		w = int(h * 1.0 / ratio)
	else:
		w = int(load_size)
		h = int(w * ratio)

	input_image = input_image.resize((h, w), Image.BICUBIC)
	input_image = np.asarray(input_image)
	# RGB -> BGR
	input_image = input_image[:, :, [2, 1, 0]]
	input_image = transforms.ToTensor()(input_image).unsqueeze(0)
	# preprocess, (-1, 1)
	input_image = -1 + 2 * input_image 
	input_image = Variable(input_image, volatile=True).float()
	# forward
	output_image = model(input_image)
	output_image = output_image[0]
	# BGR -> RGB
	output_image = output_image[[2, 1, 0], :, :]
	# deprocess, (0, 1)
	output_image = output_image.data.cpu().float() * 0.5 + 0.5
	
	return transforms.ToPILImage()(output_image).convert("RGB")