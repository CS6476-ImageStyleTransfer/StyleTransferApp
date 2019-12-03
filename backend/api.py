from flask import Flask
from flask_restful import Resource, Api, request, abort
import base64
from PIL import Image
from io import BytesIO
import cartoonGAN


app = Flask(__name__)
api = Api(app)

#put your style name here, which should be sent through http
styles = ['Hayao', 'Shinkai', 'Paprika']

class TransformImage(Resource):
    def get(self):
        data = request.json

        #validate the style type
        style = data['style']
        if style not in styles:
            abort(404, message="Style {} is not supported".format(style))
        
        #convert base64 string to image
        img_data = base64.b64decode(data['image'])
        image = Image.open(BytesIO(img_data))
        image.show()

        #use different models according to style
        if style in ['Hayao', 'Shinkai', 'Paprika']:
            output_image = cartoonGAN.transfer(image, style, load_size=500)
        output_image.show()
       
        #convert tranferred image to base64
        buffered = BytesIO()
        output_image.save(buffered, format="PNG")
        output_image_data = base64.b64encode(buffered.getvalue())

        return {'image': output_image_data.decode('ascii')}, 201
        

api.add_resource(TransformImage, '/tf')

if __name__ == '__main__':
    app.run(debug=True)