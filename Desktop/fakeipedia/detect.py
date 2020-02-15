import argparse

from mxnet import nd, image

import gluoncv as gcv
gcv.utils.check_version('0.6.0')
from gluoncv.data import ImageNet1kAttr
from gluoncv.data.transforms.presets.imagenet import transform_eval
from gluoncv.model_zoo import get_model
from PIL import Image
from PIL.ExifTags import TAGS
import sys

# from geopy.geocoders import Nominatim

def get_detections(filename, topK = 3):
    '''
    Runs model trained on ImageNet to detect objects in image.
    @param topK: how many top detections to return, default is 3
    @return img_classes: top k classes
    @return probs: probabilities of object being in each of the top k classes
    '''

    # Load pretrained model
    net = get_model('ResNet50_v2', pretrained = True)
    classes = net.classes
    # Load and transform images
    img = image.imread(filename)
    img = transform_eval(img)
    pred = net(img)

    # Keep track of top classes and probabilities
    ind = nd.topk(pred, k=topK)[0].astype('int')
    img_classes = []
    probs = []
    for i in range(topK):
        img_classes.append(classes[ind[i].asscalar()])
        probs.append(nd.softmax(pred)[0][ind[i]].asscalar())
    return img_classes, probs


def get_metadata(filename):
    '''
    Gets information from the metadata of the image.
    @param filename: name of the image
    @return location: location that the image was taken
    '''
    img = Image.open(filename)
    img.verify()
    exif = img._getexif()

    # Get location that image was taken
    # coords = exif.items()[GPSInfo]
    print(exif.items())
    # location = geolocator.reverse("52.509669, 13.376294")

if __name__ == '__main__':
    filename = sys.argv[1]
    classes, probs = get_detections(filename, 1)
    print("Classes:", classes)
    print("Probs:", probs)
    get_metadata(filename)
# # If does not have any strong predictions, use image metadata
# if (img_prob < 0.3):
#     image = Image.open(opt.input_pic)
#     image.verify()
#     img_class = image._getexif()
