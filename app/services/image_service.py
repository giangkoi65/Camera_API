import cv2
import numpy as np

def process_image(image_path: str):
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Cannot read image")

    height, width, _ = image.shape

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    brightness = float(np.mean(gray).item())

    edges = cv2.Canny(gray, 50, 150)
    edge_pixels = int(np.sum(edges > 0))

    return {
        "width": width,
        "height": height,
        "brightness": round(brightness, 2),
        "edge_pixels": edge_pixels
    }
