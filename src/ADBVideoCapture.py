import socket
import subprocess
import threading
import cv2

class ADBVideoCapture(cv2.VideoCapture):
    def __init__(self, open=True):
        super().__init__()
        self.t = None
        self.port = None
        self.server_socket = None
        if open:
            self.open()

    def open(self, resolution=[1200, 900], buffersize=1600000):
        if not check_adb_connection():
            print("No ADB device connected")
            return False

        ev = threading.Event()

        def service():
            PORT = 0
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(("localhost", PORT))
            self.port = self.server_socket.getsockname()[1]
            self.server_socket.listen(1)
            ev.set()
            client_socket, addr = self.server_socket.accept()
            w, h = resolution
            command = f"adb exec-out screenrecord --bit-rate={buffersize} --output-format=h264 --size {w}x{h} -"
            while True:
                process = subprocess.Popen(command, stdout=client_socket.fileno(), stderr=subprocess.STDOUT, shell=True)
                process.wait()

        self.t = threading.Thread(target=service, daemon=True)
        self.t.start()
        ev.wait()
        return super().open(f"tcp://localhost:{self.port}")

    def close(self):
        # Stop the service thread and release resources
        if self.t and self.t.is_alive():
            self.t.join(timeout=1)  # Wait for the thread to exit
        if self.server_socket:
            self.server_socket.close()
        self.release()  # Release the cv2.VideoCapture


def check_adb_connection():
    # Run the "adb devices" command to check if ADB is connected to any device
    try:
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        cut_string = '\n'.join(result.stdout.split('\n')[1:])
        # Check if any device is listed
        if 'device' in cut_string:
            return True
        else:
            return False
    except subprocess.SubprocessError as e:
        print(f"Error checking ADB connection: {e}")
        return False

