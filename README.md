# Phone Facial Tracking
UNI project for my "Control Systems" course.

The project works like the following:
- The program gets the phone screen (meant to be in the camera app) and passes it to opencv using [ADBVideoCapture](https://github.com/alexroat/opencv-adbvideocapture)
- Faces are detected using a frontal face cascade
- Actual physical distance from the projection of the target to the camera sensor to the sensor's center is calculated
- Some lineal algebra sorcery is performed to get both the center vector (camera -> forwards) and the target vector (camera->target)
- Azimuth and elevation between those two vectors is calculated and then passed to an rpp as a json trhough serial port communication
- the rpp moves the servos

Some more stuff is done to have a Qt app run a graph of a "simulation" of the project in real time

https://github.com/user-attachments/assets/d1e4a87a-ce03-4d59-9df5-b308e62cda16

