import base64
import binascii
import io
from PIL import Image
import cv2
import numpy as np
from pathlib import Path

def get_base64_from_bytes(bytes_str):
    '''
        Given bytes, returns Base64 representation of those bytes
    '''
    return base64.b64encode(bytes_str).decode()

def get_jpeg_bytes_from_rgb_img(numpy_image):
    '''
        Given a numpy image, compresses to the image to JPEG and returns the bytes
    '''
    buf = io.BytesIO()
    pillow_image = Image.fromarray(numpy_image)
    pillow_image.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    return byte_im

def get_jpeg_bytes_from_pillow_img(pillow_image):
    '''
        Given a numpy image, compresses to the image to JPEG and returns the bytes
    '''
    buf = io.BytesIO()
    pillow_image.save(buf, format='JPEG')
    byte_im = buf.getvalue()
    return byte_im

def get_jpeg_bytes_from_bgr_img(numpy_image):
    '''
        Given a numpy image, compresses to the image to JPEG and returns the bytes
    '''
    rgb_image = cv2.cvtColor(numpy_image, cv2.COLOR_BGR2RGB)
    return get_jpeg_bytes_from_rgb_img(rgb_image)

def get_pillow_image_from_base64(base64_string):
    '''
        Given a Base64 string for an image, returns a numpy array in RGB order
    '''
    nparr = np.frombuffer(base64.b64decode(str(base64_string)), np.uint8)
    result = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if result is None:
        raise binascii.Error()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    pillow_image = Image.fromarray(result)
    return pillow_image

def normalize_image(image):
    '''
    Given a single image that could be numpy, pillow, path string or path,
    returns the Pillow image
    '''
    if isinstance(image, np.ndarray):
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pillow_image = Image.fromarray(image)
        except:
            raise ValueError("image is not in BGR format")
    elif isinstance(image, Image.Image):
        return image
    elif isinstance(image, Path):
        try:
            path = str(image)
            n_image = cv2.imread(path)
            n_image = cv2.cvtColor(n_image, cv2.COLOR_BGR2RGB)
            if n_image is None:
                raise ValueError("Could not read image from path: {}".format(path))
            pillow_image = Image.fromarray(n_image)
        except:
            raise ValueError("Could not read image from path: {}".format(path))
    elif isinstance(image, str):
        try:
            path = str(image)
            n_image = cv2.imread(path)
            n_image = cv2.cvtColor(n_image, cv2.COLOR_BGR2RGB)
            if n_image is None:
                raise ValueError("Could not read image from path: {}".format(path))
            pillow_image = Image.fromarray(n_image)
        except:
            raise ValueError("Could not read image from path: {}".format(path))
    else:
        raise TypeError("At least one image is of inappropriate type")
    return pillow_image


def normalize_images(images):
    '''
    Given an array of images that could be numpy, pillow, path string or path,
    returns an array of Pillow images
    '''
    result = []
    for image in images:
        pillow_image = normalize_image(image)
        result.append(pillow_image)

    return result