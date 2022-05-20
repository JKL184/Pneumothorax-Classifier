
from build_img import read_image,class_dec
from build_mod import build_class_mod,build_seg_mod
import tensorflow as tf
import keras.backend as K

class prediction():
    
    def __init__(self,class_weights, seg_weights,input_shape=(3,256,256)):
        self.class_mod = build_class_mod()
        K.set_image_data_format('channels_first')
        self.seg_mod = build_seg_mod(input_shape)
        self.class_mod.load_weights(class_weights)
        print('Class_mod Load')
        self.seg_mod.load_weights(seg_weights)
        print('Segment_mod Load') 

    def Predict(self,image_path):
        original_img = class_dec(image_path)
        class_output = self.class_mod.predict(tf.expand_dims(original_img, axis=0))
        confidence = class_output
        if confidence > 0.5:
            print('Pneumothorax Positive')
            print('Classifier Prediction Confidence : {}%'.format(class_output*100))
            image_seg = read_image(image_path)
            image = tf.transpose(image_seg, [2,0,1])
            predicted_mask = self.seg_mod.predict(tf.expand_dims(image, axis=0))
            predicted_mask = tf.transpose(predicted_mask, [0,2,3,1])
            return confidence, predicted_mask
        else:
            image_seg = read_image(image_path)
            return confidence, image_seg
       
