from mxnet import nd, image
import gluoncv as gcv
# gcv.utils.check_version('0.6.0')
from gluoncv.data import ImageNet1kAttr
from gluoncv.data.transforms.presets.imagenet import transform_eval
from gluoncv.model_zoo import get_model
from PIL import Image
from PIL.ExifTags import TAGS
import sys
from geopy.geocoders import Nominatim


def detect_objects(filename, topK = 3):
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


def convert_tuple(exif_tuple):
    '''
    Converts 3-tuple representation of latitude and longitude into one number
    @param exif_tuple: 3-tuple of degrees, minutes, and seconds
    @return tuple converted into one value
    '''
    deg, min, sec = exif_tuple
    return deg + min / 60 + sec / 3600


def get_metadata(filename):
    '''
    Gets information from the metadata of the image.
    @param filename: name of the image
    @return location: location that the image was taken
    '''
    # Get latitude and longitude if it has that data
    img = Image.open(filename)
    metadata = dir(img)
    latitude = 0
    longitude = 0
    if 'gps_latitude' in metadata:
        latitude = convert_tuple(img.gps_latitude)
    if 'gps_longitude' in metadata:
        longitude = convert_tuple(img.gps_longitude)
    # Revert latitude and longitude to location
    geolocator = Nominatim(user_agent="my-application")
    location = geolocator.reverse(str(latitude) + ", " + str(longitude))
    return location.address


def get_detection(filename):
    '''
    Get final detection.
    @param filename
    @return class of object detected or location where image was taken
    '''
    img_class, prob = detect_objects(filename, 1)
    try:
        if prob[0] < 0.5:
            return get_metadata(filename)
    except:
        pass
    return img_class


if __name__ == '__main__':
    filename = sys.argv[1]
    detection = get_detection(filename)
    print(detection)
