from mxnet import nd, image
import gluoncv as gcv
# gcv.utils.check_version('0.6.0')
from gluoncv.data import ImageNet1kAttr
from gluoncv.data.transforms.presets.imagenet import transform_eval
from gluoncv.model_zoo import get_model
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS
import sys
import geopy.geocoders
from geopy.geocoders import Here, Nominatim
import urllib
import certifi

def get_detection(filename):
    '''
    Runs model trained on ImageNet to detect objects in image.
    @return img_class: top class
    @return img_prob: probability of object being in the predicted class
    '''
    # Load pretrained model
    net = get_model('ResNet50_v2', pretrained = True)
    classes = net.classes
    # Load and transform images
    img = image.imread(filename)
    img = transform_eval(img)
    pred = net(img)
    # Determine object class and confidence value
    ind = nd.topk(pred, k=1)[0].astype('int')
    img_class = classes[ind[0].asscalar()]
    img_prob = nd.softmax(pred)[0][ind[0]].asscalar()
    return img_class, img_prob


def get_metadata(filename):
    '''
    Gets information from the metadata of the image.
    @param filename: name of the image
    @return location: location that the image was taken
    '''
    # Get exif data from image
    img = Image.open(filename)
    img.verify()
    exif = img._getexif()
    # Create dictionary with keys and values from exif data
    labeled_data = {}
    for (key, value) in exif.items():
        labeled_data[TAGS.get(key)] = value
    # Isolate geographic information
    gps_info = labeled_data['GPSInfo']
    geo_info = {}
    for (key, value) in GPSTAGS.items():
        if value in ['GPSLatitudeRef', 'GPSLatitude', 'GPSLongitudeRef', 'GPSLongitude']:
            geo_info[value] = labeled_data['GPSInfo'][key]
    return geo_info


def convert_to_decimal(val_tuple, ref_dir):
    '''
    Converts tuple of latitude or longitude information to decimal values
    @param val_tuple: tuple representing latitude or longitude
    @param ref_dir: reference direction like N, S, E, W
    @return: latitude or longitude in decimal representation
    '''
    # Calculate decimal values
    hours = val_tuple[0][0] / val_tuple[0][1]
    min = val_tuple[1][0] / val_tuple[1][1] / 60
    sec = val_tuple[2][0] / val_tuple[2][1] / 3600
    decimal_val = hours + min + sec
    # Adjust based on reference direction
    if ref_dir == 'S' or ref_dir == 'W':
        decimal_val *= -1
    return decimal_val


def get_city(address):
    '''
    Isolates the city from the full address
    @param address: string with the full address
    @return: just the city name
    '''
    # Get index of first comma
    comma_idx = address.find(',')
    # Get index of blank preceding comma
    blank_idx = 0
    for i in range(comma_idx + 2, len(address)):
        if address[i] == ' ':
            blank_idx = i
            break
    # Return substring that is the city name
    return address[comma_idx + 2 : blank_idx - 1]


def get_location(filename):
    '''
    Gets location from gps dictionary entries
    @param filename: image we are performing object detection on
    @return latitude and longitude as single values
    '''
    gps_dict = get_metadata(filename)
    # Calculate latitude and longitude
    lat = convert_to_decimal(gps_dict['GPSLatitude'], gps_dict['GPSLatitudeRef'])
    long = convert_to_decimal(gps_dict['GPSLongitude'], gps_dict['GPSLongitudeRef'])
    # Get full address
    geolocator = Nominatim(timeout=10)
    def uo(args, **kwargs):
       return urllib.request.urlopen(args, cafile=certifi.where(), **kwargs)
    geolocator.urlopen = uo
    # print(geolocator.reverse((lat, long)))

    address = geolocator.reverse((lat, long))

    return address.raw['address']['city']


def get_final_detection(filename):
    '''
    Get final detection.
    @param filename
    @return class of object detected or location where image was taken
    '''
    img_class, prob = get_detection(filename)
    location = None
    try:
        location = get_location(filename)
    except:
        pass
    return img_class, prob, location


if __name__ == '__main__':
    filename = sys.argv[1]
    detection, prob, location = get_final_detection(filename)
    print(detection, prob, location)
