# ocr_preprocessing.py
"""
This module provides functions to preprocess images for OCR.
It includes functions to convert images to grayscale, upscale them,
apply Gaussian blur, and adaptive thresholding.
It uses OpenCV for image processing.
"""

# imports
import cv2


def convert_to_grayscale(image):
    """
    Convert a BGR image to grayscale.
    Args:
        image (numpy.ndarray): The input BGR image.
    Returns:
        numpy.ndarray: The grayscale image.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def upscale_image(image, scale_x=2, scale_y=2):
    """
    Resize the image by scaling it up using bicubic interpolation.

    Args:
        image (numpy.ndarray): The input image.
        scale_x (float): Scale factor along the horizontal axis.
        scale_y (float): Scale factor along the vertical axis.

    Returns:
        numpy.ndarray: The upscaled image.
    """
    return cv2.resize(image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_CUBIC)

def apply_gaussian_blur(image, kernel_size=(5, 5)):
    """
    Apply Gaussian blur to the image.
    Args:
        image (numpy.ndarray): The input image.
        kernel_size (tuple): Size of the Gaussian kernel.
    Returns:
        numpy.ndarray: The blurred image.
    """
    return cv2.GaussianBlur(image, kernel_size, 0)

def apply_adaptive_threshold(image):
    """
    Apply adaptive thresholding to the image.
    Args:
        image (numpy.ndarray): The input image.
    Returns:
        numpy.ndarray: The thresholded image.
    """
    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

def preprocess_image(
    image_path,
    use_grayscale=True,
    use_upscale=True,
    use_blur=True,
    use_threshold=True
):
    """
    Preprocess the image for OCR.
    Args:
        image_path (str): Path to the image file.
        use_grayscale (bool): Whether to convert to grayscale.
        use_upscale (bool): Whether to upscale the image.
        use_blur (bool): Whether to apply Gaussian blur.
        use_threshold (bool): Whether to apply adaptive thresholding.
    Returns:
        numpy.ndarray: The preprocessed image.
    """
    image = cv2.imread(image_path)

    if use_grayscale:
        image = convert_to_grayscale(image)

    if use_upscale:
        image = upscale_image(image)

    if use_blur:
        image = apply_gaussian_blur(image)

    if use_threshold:
        image = apply_adaptive_threshold(image)

    return image
