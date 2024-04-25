import numpy as np
from PIL import Image
import yaml
import json
from influxdb_client import InfluxDBClient


SCALE_SIZE = 256

class Image_Ope():
    def __init__(self, path_file):
        self.image = Image.open(path_file)
        
    def load_image(self):
        self.image.load()
        return self.image

    def __prepare_image(self):
        self.image = self.image.convert('L')  #Convert to 1 channel picture from RGB
        self.image = self.image.resize((SCALE_SIZE, SCALE_SIZE))
        return np.array(self.image)

    def blur_center(self):
        image = self.__prepare_image()
        #image = np.array(image / 255, dtype='float32')  #Normalise data
        all_pix = SCALE_SIZE
        
        get_idx = lambda t:np.where(t==max(t))
        x = get_idx(np.sum(image, axis=0)/all_pix)
        y = get_idx(np.sum(image, axis=1)/all_pix)
        return (x[0],y[0])


class Test():
    def __init__(self, path_file):
        self.history = {"metrics":{}, "test":{}}
        self.val_data = self.load_val_data(path_file)
        self.x_0 = self.val_data['position'][0]+int(SCALE_SIZE/2) #Center of the picture
        self.y_0 = self.val_data['position'][1]+int(SCALE_SIZE/2)

    def test_func1(self, x_b, y_b):
        self.history["metrics"]['position'] = [x_b-int(SCALE_SIZE/2), y_b-int(SCALE_SIZE/2)]

        if x_b==self.x_0 and y_b==self.y_0:
            self.history["test"]['test_func1'] = "Success"
        else:
            self.history["test"]['test_func1'] = "Fail"
        assert x_b==self.x_0 and y_b==self.y_0,"center of the blur not in the position"
      
    def test_func2(self, x_b, y_b):
        std = np.sqrt(((x_b-self.x_0)**2) + ((y_b-self.y_0)**2))
        self.history["metrics"]['std'] = std

        if std < self.val_data['std']:
            self.history["test"]['test_func2'] = "Success"
        else:
            self.history["test"]['test_func2'] = "Fail"       
        assert std < self.val_data['std'], f"std more than reference {std[0]} > {val_data['std']}"

    def test_func3(self, x_b, y_b):
        dis = ((x_b-self.x_0)**2) + ((y_b-self.y_0)**2)
        self.history["metrics"]['dispersion'] = dis

        if dis < self.val_data['dispersion']:
            self.history["test"]['test_func3'] = "Success"
        else:
            self.history["test"]['test_func3'] = "Fail"
        assert dis < self.val_data['dispersion'], f"dispersion more than reference {dis[0]} > {val_data['dispersion']}"

    def load_val_data(self, path_file):
        with open(path_file, 'r') as file:
            val_data = yaml.safe_load(file)
        return val_data
   
    def result_to_db(self):
        with InfluxDBClient(url="http://localhost:1111", token="my-token", org="my-org") as client:
            with client.write_api() as write_api:
                write_api.write(bucket="my-bucket", record=self.history)

    def result_to_json(self):
        with open('result.json', 'w') as file:
            json.dump(self.history, file)
        
        
    
if __name__ == "__main__":
    image_obj = Image_Ope("file.jpg")  #Taking a picture from a file for example
    image_obj.load_image()
    x,y = image_obj.blur_center()

    testing = Test('val.yml')
    testing.test_func1(x, y)
    testing.test_func2(x, y)
    testing.test_func3(x, y)

    testing.result_to_db()  #Send test result to DB
    testing.result_to_json()    #Send test result to JSON
