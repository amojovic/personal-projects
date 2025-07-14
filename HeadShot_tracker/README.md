Fun project inspired by sentry gun from Team Fortress 2.

Code is pretty simple for both parts:

mainCode.py is where python is used for face detection (via pre-existing model) and sends how much servo motors need to be moved based on the face offset from the center of the screen.

arduinoCode is just used to actually move the motors and also for regulating the laser i attached (originally it was always on and overheated)

If you are interested in building it, i left the picture of how it looks and the 'schematic' in the images folder.
