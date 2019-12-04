import os
from options.test_options import TestOptions
from data import create_dataset
from models import create_model
import numpy as np
from util import util 
from util.visualizer import save_images
from util import html

def pix2pix(input_image_path="imgs", model_name='facades_label2photo_pretrained'):
    opt = TestOptions().parse()  # get test options
    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    opt.dataroot= input_image_path
    opt.direction = "BtoA" 
    opt.model = "pix2pix" 
    opt.name = model_name
    opt.num_test = 1
    opt.dataset_mode='aligned'
    opt.norm='batch'
    opt.netG='unet_256'
	
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers

    if opt.eval:
        model.eval()

    for i, data in enumerate(dataset):
        if i >= opt.num_test:  # only apply our model to opt.num_test images.
            break
        model.set_input(data)  # unpack data from data loader
        model.test()           # run inference
        visuals = model.get_current_visuals()  # get image results

        image_dir = "results/result.png"
        count = 0
        for label, im_data in visuals.items():
            im = util.tensor2im(im_data)
            if(count == 1):
                util.save_image(im, image_dir, aspect_ratio=1)
            count += 1

# run code: pix2pix("imgs", "facades_label2photo_pretrained")
