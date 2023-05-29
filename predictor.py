import cv2
import numpy as np

from keras.models import load_model

class Predictor:


    def __init__(self,model_path) -> None:

        self.model = load_model(model_path)
        self.probability_threshold = 0.8
    

    def get_predicton(self,splited_boxes):

        prediction_result= []

        for image in splited_boxes:

            image = self.preprocess_before_prediction(image)
            predictions = self.model.predict(image)
            result = self.model.predict(image , verbose =0)

            predicted_class = np.argmax(result[0])
            probability = np.amax(predictions)


            if probability > self.probability_threshold:

                prediction_result.append(predicted_class)

            else :
                
                prediction_result.append(0)

        return prediction_result

    def preprocess_before_prediction(self,image):

        image = np.asarray(image) 
        image = image[4:image.shape[0] -4 , 4:image.shape[1] -4]
        image = cv2.resize(image , (28,28))
        image = image / 255
        image = image.reshape(1,28,28,1)
    
        return image





