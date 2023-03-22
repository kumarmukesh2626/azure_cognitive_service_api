import pytest
from cameraLoader.getlatestframes import CameraLoader
import unittest
import configparser
import time
import os

# Get the absolute path of the current file
file_path = os.path.abspath(__file__)
# Construct the relative path to the logs directory
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(file_path))), 'logs')
# Construct the relative path to the config directory
config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(file_path))), 'config')


def test_empty():
    assert True


# # Test the CameraLoader class
# # @pytest.mark.usefixtures("driver_init")
class TestCameraLoader():
    # Test case for successful initialization of CameraLoader

    def test_init_success(self):
        # Initialize the CameraLoader with a valid configuration file path
        loader = CameraLoader(os.path.join(config_dir, "cam_config.ini"))
        # Check that the loader object is not None
        assert loader is not None
    

# # #     # Test case for starting the frame capture thread
#     def test_start(self):
#         # Initialize the CameraLoader with a valid configuration file path
#         loader = CameraLoader("src/config/cam_config.ini")
#         # Start the frame capture thread
#         loader.start()
#         # Check that the thread has started
#         assert loader.stopped == False

#     # Test case for stopping the frame capture thread
    def test_stop(self):
        # Initialize the CameraLoader with a valid configuration file path
        loader = CameraLoader(os.path.join(config_dir, "cam_config.ini"))
        # Start the frame capture thread
        loader.start()
        # Stop the frame capture thread
        loader.stop()
        # Check that the thread has stopped
        time.sleep(1)
        assert loader.stopped == True
