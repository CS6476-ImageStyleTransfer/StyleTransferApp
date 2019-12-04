import re
import torch
from torchvision import transforms
import torch.onnx
from networks.cnn_transformer_net import TransformerNet
import cnn_utils as utils

def stylize(input_path, style, model_path='trained_models/CNN/'):
    device = torch.device("cpu")    
    
    content_image = utils.load_image(input_path, scale=None)
    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(content_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        style_model = TransformerNet()
        path = model_path + style + '.pth'
        
        state_dict = torch.load(path)
        # remove saved deprecated running_* keys in InstanceNorm from the checkpoint
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.to(device)
        output = style_model(content_image).cpu()
    
    utils.save_image('output/cnn_output.jpg', output[0])