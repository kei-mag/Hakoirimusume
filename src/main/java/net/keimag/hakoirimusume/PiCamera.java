package net.keimag.hakoirimusume;

import org.slf4j.Logger;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.BufferedOutputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.file.Files;
//import uk.co.caprica.picam.*;
//import uk.co.caprica.picam.enums.AutomaticWhiteBalanceMode;
//import uk.co.caprica.picam.enums.Encoding;

//public class PiCamera {
//    private static final Logger log = org.slf4j.LoggerFactory.getLogger(PiCamera.class);
//    private Camera camera;
//    private CameraConfiguration cameraConfig;
//    private final ByteArrayPictureCaptureHandler pictureCaptureHandler = new ByteArrayPictureCaptureHandler();
//
//    public PiCamera(int width, int height) {
//        cameraConfig = CameraConfiguration.cameraConfiguration()
//                .width(width)
//                .height(height)
//                .automaticWhiteBalance(AutomaticWhiteBalanceMode.AUTO)
//                .encoding(Encoding.JPEG);
//        try {
//            this.camera = new Camera(cameraConfig);
//        } catch (CameraException e) {
//            log.error("Failed to initialize camera, continued with no image.", e);
//        }
//    }
//
//    public byte[] getPicture() {
//        byte[] pictureData = null;
//        if (camera == null) {
//            return null;
//        } else {
//            for (int i = 0; i < 2; i++) { // Try to take picture twice if failed at first shot, then give up
//                if (pictureData != null) {
//                    break;
//                }
//                try {
//                    pictureData = camera.takePicture(this.pictureCaptureHandler);
//                } catch (CaptureFailedException cfe) {
//                    log.warn("Failed to capture image ({}/2}.", i+1, cfe);
//                    pictureData = null;
//                    camera.close();
//                    try {
//                        this.camera = new Camera(cameraConfig);
//                    } catch (CameraException ce) {
//                        log.error("Failed to initialize camera, continued with no image.", ce);
//                        this.camera = null;
//                        return null;
//                    }
//                }
//            }
//            return pictureData;
//        }
//    }
//}

class PiCamera {
    private final int width;
    private final int height;

    public PiCamera(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public String getPicture() throws IOException {
        try {
            Process process = Runtime.getRuntime().exec("rpicam-jpg --width " + width + " --height " + height + " --output /tmp/image.jpg");
            return "/tmp/image.jpg";
        } catch (IOException e) {
            return null;
        }
    }









}