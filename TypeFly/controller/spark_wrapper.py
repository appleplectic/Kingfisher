from io import BytesIO
from typing import Tuple
import cv2
import numpy as np
import requests
from requests.adapters import HTTPAdapter

from controller.abs.robot_wrapper import RobotWrapper


class BindableHTTPAdapter(HTTPAdapter):
    def __init__(self, source_ip: str, *args, **kwargs):
        self.source_ip = source_ip
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['source_address'] = (self.source_ip, 0)
        return super().init_poolmanager(*args, **kwargs)


class SparkBackgroundFrameReader():
    def __init__(self, uri: str, interface: str):
        self.uri = uri
        self.session = requests.Session()
        adapter = BindableHTTPAdapter(interface)
        self.session.mount('http://', adapter)
        self.last_good_img = None

    @property
    def frame(self) -> np.ndarray:
        with self.session.get(self.uri + "videoStream", stream=True) as response:
            if response.status_code == 200:
                bytes_image = BytesIO()
                start_marker_found = False

                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        if not start_marker_found:
                            # Search for the JPEG start marker (b'\xff\xd8')
                            start_index = chunk.find(b'\xff\xd8')
                            if start_index != -1:
                                bytes_image.write(chunk[start_index:])
                                start_marker_found = True
                        else:
                            # Stop when JPEG end marker (b'\xff\xd9') is found
                            end_index = chunk.find(b'\xff\xd9')
                            if end_index != -1:
                                bytes_image.write(chunk[:end_index+2])
                                break
                            bytes_image.write(chunk)


                bytes_image.seek(0)
                img_array = np.asarray(bytearray(bytes_image.read()), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

                if img is None:
                    print("Failed to get image, using last image.")
                    return self.last_good_img

                img = self.adjust_exposure(img, alpha=1.3, beta=-30)
                img = self.sharpen_image(img)

                self.last_good_img = img
                return img

            raise RuntimeError("Failed to get frame from drone.")

    def adjust_exposure(self, img: np.ndarray, alpha: float = 1.0, beta: int = 0) -> np.ndarray:
        """
        Adjust the exposure of an image.

        :param img: Input image
        :param alpha: Contrast control (1.0-3.0). Higher values increase exposure.
        :param beta: Brightness control (0-100). Higher values add brightness.
        :return: Exposure adjusted image
        """
        # Apply exposure adjustment using the formula: new_img = img * alpha + beta
        new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        return new_img

    def sharpen_image(self, img: np.ndarray) -> np.ndarray:
        """
        Apply a sharpening filter to an image.

        :param img: Input image
        :return: Sharpened image
        """
        # Define a sharpening kernel
        kernel = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])

        # Apply the sharpening filter
        sharpened = cv2.filter2D(img, -1, kernel)
        return sharpened


class SparkWrapper(RobotWrapper):
    def __init__(self, uri: str, interface: str):
        self.uri = uri
        if not self.uri.endswith('/'):
            self.uri += '/'
        self.interface = interface

        self.session = requests.Session()
        adapter = BindableHTTPAdapter(interface)
        self.session.mount('http://', adapter)

        self.fr = SparkBackgroundFrameReader(self.uri, self.interface)

    def connect(self):
        if "Connected" not in self.session.get(self.uri).text:
            raise RuntimeError("Could not establish connection to DJI Control Server.")

    def keep_active(self):
        pass

    def takeoff(self) -> bool:
        return self.session.get(self.uri + "takeoff").status_code == 200

    def land(self):
        self.session.get(self.uri + "disableLandingProtection")
        self.session.get(self.uri + "land")

    def start_stream(self):
        pass

    def stop_stream(self):
        pass

    def get_frame_reader(self) -> SparkBackgroundFrameReader:
        return self.fr

    def move_forward(self, distance: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "moveForward/" + str(distance / 1000)) == 200, True

    def move_backward(self, distance: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "moveBackward/" + str(distance / 1000)) == 200, True

    def move_left(self, distance: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "moveLeft/" + str(distance / 1000)) == 200, True

    def move_right(self, distance: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "moveRight/" + str(distance / 1000)) == 200, True

    def move_up(self, distance: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "moveUp/" + str(distance / 1000)) == 200, True

    def move_down(self, distance: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "moveDown/" + str(distance / 1000)) == 200, True

    def turn_ccw(self, degree: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "rotateCounterClockwise/" + str(degree)) == 200, True

    def turn_cw(self, degree: int) -> Tuple[bool, bool]:
        return self.session.get(self.uri + "rotateClockwise/" + str(degree)) == 200, True
