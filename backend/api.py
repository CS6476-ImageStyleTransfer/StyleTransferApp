from flask import Flask
from flask_restful import Resource, Api, request, abort
from flask_cors import CORS
from PIL import Image
from io import BytesIO
import base64
import requests
import cloudinary
import cloudinary.uploader

import transformer
from settings import CLOUD_NAME, API_KEY, API_SECRET


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
api = Api(app)

cloudinary.config(
  cloud_name = CLOUD_NAME,  
  api_key = API_KEY,  
  api_secret = API_SECRET
)

#put your style name here, which should be sent through http
styles = ['Candy', 'Mosaic', 'RainPrincess', 'Udnie', 'Hayao', 'Shinkai', 'Paprika', 'Hosoda', 'Monet', 'Vangogh', 'Ukiyoe', 'Cezanne', 'Shoe', 'Handbag', 'Facade', 'Map']

class TransformImage(Resource):
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
        if style in ['Candy', 'Mosaic', 'RainPrincess', 'Udnie']:
            output_image = transformer.cnn_transformer(img, style)
        elif style in ['Hayao', 'Shinkai', 'Paprika', 'Hosoda']:
            output_image = transformer.cartoon_gan_transformer(img, style, load_size=500)
        elif style in ['Monet', 'Vangogh', 'Ukiyoe', 'Cezanne']:
            output_image = transformer.cycle_gan_transformer(img, style)
        elif style in ['Shoe', 'Handbag', 'Facade', 'Map']:
            output_image = transformer.pix2pix_transformer(img, style)
        else:
            print('Error style')
        
        # save image to local and upload it to cloudinary
        img_id = img_url[img_url.rfind('/')+1:-4]
        output_image.save('output/' + img_id + '.png')
        reponse = cloudinary.uploader.upload('output/' + img_id + '.png')
        
        return {'img_url': reponse['secure_url']}
        
api.add_resource(TransformImage, '/tf')

if __name__ == '__main__':
    app.run(debug=True)