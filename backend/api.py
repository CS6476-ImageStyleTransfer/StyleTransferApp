from flask import Flask
from flask_restful import Resource, Api, request, abort
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64
import requests
import cloudinary
import cloudinary.uploader

import cartoonGAN


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
api = Api(app)

cloudinary.config(
  cloud_name = 'bxie41',  
  api_key = '319594211464436',  
  api_secret = 'f6CXshANZsH_yUun9Xfl9lc71cs'  
)

#put your style name here, which should be sent through http
styles = ['Hayao', 'Shinkai', 'Paprika']

class TransformImage(Resource):
    def get(self):
        return 'Hello world'

    def post(self):
        data = request.json
        
        #validate the style type
        style = data['style']
        if style not in styles:
            abort(404, message="Style {} is not supported".format(style))
        
        #download the image from image server
        img_url = data['img_url']
        img_data = requests.get(img_url).content
        img = Image.open(BytesIO(img_data))

        #use different models according to style
        if style in ['Hayao', 'Shinkai', 'Paprika']:
            output_image = cartoonGAN.transfer(img, style, load_size=500)
    
        # save image to local and upload it to cloudinary
        img_id = img_url[img_url.rfind('/')+1:-4]
        output_image.save('output/' + img_id + '.png')
        reponse = cloudinary.uploader.upload('output/test.png')
        
        return {'img_url': reponse['secure_url']}
        
api.add_resource(TransformImage, '/tf')

if __name__ == '__main__':
    app.run(debug=True)