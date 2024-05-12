import time
from io import BytesIO

from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()
time.sleep(1)
image = picam2.capture_image("main")
with BytesIO() as bytes_io:
    image.save(open("test.png", "wb"), format="PNG")
    image.save(bytes_io, format="PNG")
    image_bytes = bytes_io.getvalue()
