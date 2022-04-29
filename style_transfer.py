import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
# import cv2
from PIL import Image, ImageFilter, ImageEnhance


class StyleTransfer:
    """Transfer style from one image into another.

    Args:
      model - trained model for image style transfer.
    """

    def __init__(self):
        self.model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    def transfer_style(self, content_image, style_image, scaler=540):
        """Transfer style from style image into content image.

        Args:
          content_image (PIL.Image) - source image.
          style_image (PIL.Image) - image with specific style.
          scaler (int) - intensity of processing.

        Returns:
          stylized_image (PIL.Image) - stylized source image.
        """
        max_dim = scaler
        content_image = self.__img_to_tensor(content_image, max_dim)
        style_image = self.__img_to_tensor(style_image, max_dim)
        stylized_image = self.model(content_image, style_image)[0]
        return self.__tensor_to_image(stylized_image)

    def __img_to_tensor(self, img, max_dim):
        """Converting image to tensor.

        Args:
            img (PIL.Image) - image.

        Returns:
            img (tensorflow.Tensor) - tensor from image.
        """
        img = np.array(img, dtype=np.float32)
        img = tf.convert_to_tensor(img, dtype=tf.float32)
        img = (img - np.min(img)) / np.ptp(img)
        shape = tf.cast(tf.shape(img)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        img = tf.image.resize(img, new_shape)
        img = img[tf.newaxis, :]
        return img

    def __tensor_to_image(self, tensor):
        """Converts tensor to image.

        Args:
          tensor (tensorflow.Tensor) - tensor with values of pixels.

        Returns:
          image (PIL.Image) - image getted from tensor.
        """
        tensor = tensor * 255
        tensor = np.array(tensor, dtype=np.uint8)
        if np.ndim(tensor) > 3:
            assert tensor.shape[0] == 1
            tensor = tensor[0]
        return Image.fromarray(tensor)

    @staticmethod
    def increase_saturation(image, coefficient=1.25):
        """Increase saturation of input image.

        Args:
          image (PIL.Image) - input image.
          coefficient (float) - coefficient for saturation increase

        Returns:
          image (PIL.Image)
        """
        return ImageEnhance.Color(image).enhance(coefficient)
