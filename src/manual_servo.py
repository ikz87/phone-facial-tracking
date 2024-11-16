import kzserial
import serial
import json
import threading
import colorsys
import keyboard
import numpy as np
import time

def main():
    half_max_angle = 45
    angle_dict = {
        "servo_x": 0,
        "servo_y": 0,
    }
    available_ports = kzserial.get_serial_ports()
    rpp = None
    if available_ports:
        rpp = serial.Serial(available_ports[-1], timeout=1)

    step = 5
    angle_json = json.dumps(angle_dict)
    while True:
        try:
            # Check if arrow keys are pressed
            if keyboard.is_pressed("up"):
                angle_dict["servo_y"] += step
            if keyboard.is_pressed("down"):
                angle_dict["servo_y"] -= step
            if keyboard.is_pressed("left"):
                angle_dict["servo_x"] += step
            if keyboard.is_pressed("right"):
                angle_dict["servo_x"] -= step

            # Make sure to send nice values
            angle_dict["servo_x"] = min(half_max_angle,max(-half_max_angle,angle_dict["servo_x"]))
            angle_dict["servo_y"] = min(half_max_angle,max(-half_max_angle,angle_dict["servo_y"]))

            # Send the data
            last_json = angle_json
            angle_json = json.dumps(angle_dict)
            if last_json!= angle_json:
                print(f"Sending: {angle_json}")
                rpp.write((angle_json + "\n").encode())

            # Exit the loop if 'Esc' is pressed
            if keyboard.is_pressed("esc"):
                print("Exiting...")
                break

            # Adding a small sleep to reduce CPU usage
            time.sleep(0.03)
        except Exception as e:
            print(f"Error: {e}")
            break



if __name__ == "__main__":
    main()

