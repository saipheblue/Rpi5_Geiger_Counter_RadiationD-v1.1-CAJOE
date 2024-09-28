# Rpi5_Geiger_Counter_RadiationD-v1.1-CAJOE
Rpi5 with RadiationD-v1.1-CAJOE module + html site frontend with real time measurments and chart

![preview](https://github.com/user-attachments/assets/e0ad5fa0-65c0-49f1-919c-1d113893f186)

# Start measuring

run the script and keep it running
```
python3 geiger.py
```
Then open https://127.0.0.1:80/index in your browser

Others on your network can access it using *rpi5ip*:80/index

# Rpi5 GPIO diagram

Connect 5V to any 5V, Ground to any ground and VIN to GPIO4 ( pin 7 )
![GPIO_rpi5](https://github.com/user-attachments/assets/cc65b6c3-409a-4858-9668-00cd6c34757a)

# Issues

If you got permisisons error then use **sudo**

If you get 404 error make sure index page is in "templates" folder, it is case sensitive
It should have following structure:
- Project
- - geiger.py
- - templates
- - - index.html

Documentation from manufacturer is listing M4011 which has teh same specs as J305

ssl_context=('cert.pem', 'key.pem') can be replaced by ssl_context='adhoc' if oyu dotn have keys - https://zhangtemplar.github.io/flask/

rpi5 has problems with gpio remove it using:
```
sudo apt remove python3-rpi.gpio
```
and install lgpio
```
python3 -m pip install rpi-lgpio flask
```
if you have problems with install use:
```
python3 -m pip install rpi-lgpio flask --break-system-packages
```
more info - https://pimylifeup.com/python-externally-managed-environment/

# μSv/h ratio

Almsot everyone is using wrong coefficient / ratio of 0.00812037037037 here is the formula I used together with source elaborating why 0.0081 is wrong !
J305 has 25 CPM
1 / (25 * 60 / 8.77)  https://medium.com/@iotdevices/geiger-tube-j305-how-to-calculate-the-conversion-factor-of-cpm-to-%CE%BCsv-h-technical-note-b0cc14850576

# Credits

Heavily inspired by https://github.com/HeckerBirb/rpi-radiationd-v1.1
