from io import BytesIO
from picamera2 import Picamera2


class PiCamera:
    def __init__(self, rotation=None):
        """Initialize PiCamera

        Parameters
        ----------
        rotate_angle : float, optional
            angle of the image, by default None
        """
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(main={"size": (3280, 2464), "format": "RGB888"})
        self.picam2.start(config=config)

    def capture_bytes(self, zoom=None):
        """Capture photo by Raspberry Pi Camera Module

        Parameters
        ----------
        zoom : tuple[int, int, float], optional
            tuple of (zoom_point_x, zoom_point_y, zoom_ratio), by default None

        Returns
        -------
        bytes
            Bytes of PNG Image
        """
        image = self.picam2.capture_image()
        if zoom:
            w, h = image.size
            x, y, ratio = zoom
            double_ratio = ratio * 2
            image = image.crop((x - w / double_ratio, y - h / double_ratio, x + w / double_ratio, y + h / double_ratio))
        # Convert PIL Image to bytes
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes = image_bytes.getvalue()
        return image_bytes
