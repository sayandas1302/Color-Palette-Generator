from flask import Flask, render_template, request
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

class Pallete:
    def __init__(self, path, ncol=6):
        self.img_oject = Image.open(path)
        self.height = self.img_oject.size[1]
        self.width = self.img_oject.size[0]
        self.n_pix = self.height*self.width
        self.col_array = np.array(self.img_oject).reshape(self.n_pix, 3)
        self.ncol = ncol
        self.colors = self.get_dominating_cols()
        self.pallete = self.create_pallete()
        self.hex_vals = self.get_hex()

    def get_dominating_cols(self):
        '''method for extracting colors'''
        model = KMeans(n_clusters=self.ncol)
        model.fit(self.col_array)
        colors = [tuple(x) for x in model.cluster_centers_.astype(int)]
        return colors
    
    def create_pallete(self):
        '''method for creating pallette'''
        pallatte_size = 100
        pallatte = Image.new('RGB', (self.ncol*pallatte_size, pallatte_size))

        position = 0
        for col in self.colors:
            current_col = Image.new('RGB', (pallatte_size, pallatte_size), col)
            pallatte.paste(current_col, (position,  0))
            position += pallatte_size
        
        return pallatte

    def get_hex(self):
        '''method for getting the hex code'''
        col_hex = lambda x: hex(x).split("x")[1]
        hex_vals = [f'#{col_hex(col[0])}{col_hex(col[1])}{col_hex(col[2])}' for col in self.colors]
        return hex_vals
    

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    uploadImage_url = './static/images/uploadIcon.png'
    input_url=None
    output_url = None
    hex_values = None
    img_height = None
    img_width = None
    if request.method == 'POST':
        img = request.files.get('input_img')
        input_url = './static/input_output/inputImg.jpg'
        img.save(input_url)
        pallete_object = Pallete(input_url)
        output_url = './static/input_output/outputImg.jpg'
        pallete_object.pallete.save(output_url)
        hex_values = pallete_object.hex_vals
        img_height = pallete_object.height
        img_width = pallete_object.width
    return render_template('index.html',
                           uploadImage_url=uploadImage_url,
                           input_url=input_url,
                           output_url=output_url,
                           hex_values=hex_values,
                           img_height=img_height, 
                           img_width=img_width)

if __name__ == '__main__':
    app.run(debug=True)