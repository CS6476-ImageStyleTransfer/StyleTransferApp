import torch
import os
import re
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.utils as vutils
import torch.onnx

from networks.CartoonGAN import CartoonGAN
from networks.CNN import CNN


def cnn_transformer(input_image, style, model_path='./trained_models/CNN'):
    device = torch.device("cpu")

    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(input_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        style_model = CNN()
        path = os.path.join(model_path, style + '.pth')

        state_dict = torch.load(path)
        # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.to(device)
        output = style_model(content_image).cpu()

        output_image = output[0].clone().clamp(0, 255).numpy().transpose(1, 2, 0).astype('uint8')
        output_image = Image.fromarray(output_image)

        return output_image


def cartoon_gan_transformer(input_image, style, load_size=450, model_path='./trained_models/CartoonGAN'):
    model = CartoonGAN()
    model.load_state_dict(torch.load(os.path.join(
        model_path, style + '_net_G_float.pth')))
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


def cycle_gan_transformer(input_image, style, model_path='./trained_models/CycleGAN'):
    return 0


def pix2pix_transformer(input_image, style, model_path='./trained_models/pixel2pixel'):
    return 0