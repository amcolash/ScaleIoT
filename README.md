# ScaleIoT
OpenCV python program with a simple webpage to track weight readings from a scale.

This project:
- Takes an image from a webcam when scale begins weighing
- Process the image to both reduce noise and crop to the specific section of the display
- Do OCR on the image
- Record data
- Graph data on a web page
- Push to PebbleHealth API (Future)

# Setup
- Install opencv (with python bindings and NumPy for python 2.x)
  `sudo apt-get install python-opencv python-numpy`
- Install ssocr (ocr of seven segment displays)
```
sudo apt-get install libx11-dev
sudo apt-get install libimlib2-dev
wget http://www.unix-ag.uni-kl.de/~auerswal/ssocr/ssocr-2.14.1.tar.bz2
bzip2 -d ssocr-2.14.1.tar.bz2
tar xvf ssocr-2.14.1.tar
cd ssocr-2.14.1/
make
sudo make install
```

I had some problems compiling ssocr, after the `make` command I then ran `cc   ssocr.o imgproc.o help.o  -L/usr/lib/arm-linux-gnueabihf -lImlib2 -o ssocr` followed by another `make` and finally `sudo make install`. Yikes, compiler linking problems (and I am pretty rusty with Makefiles).

## Installing as a service
To install this ScaleIoT as a service, edit the `scaleiot` script in the root of this repository with `vim scaleiot` or `nano scaleiot`. Then just run `./install.sh` from the root directory of the project. (If you do not have upstart, you may need to add to rc.local or something similar)

## Setting up the web server
In this project I am using nginx because it is lightweight and less overhead for the pi. The setup is also really simple!

First, install with `sudo apt-get install nginx`. Then, to change the deafult location for the server, do `sudo vim /etc/nginx/sites-available` (substitute for your favorite editor). On the line with ``, just edit the path from `/usr/share/nginx/www` to the root directory of the project.

Finally, you will need to install dependencies for the web page. I used bower in this case. You might need to install that and nodejs.
```
cd web/
sudo apt-get install node
npm install -g bower
bower install
```

Finally, start up nginx (will run by default on startup normally): `sudo /etc/init.d/nginx start`.

## Projects Used
- [OpenCV for Python](http://opencv.org/) - Open source computer vision library
- [NumPy](http://www.numpy.org/) - Python computation and array library
- [ssocr](https://www.unix-ag.uni-kl.de/~auerswal/ssocr/) - Seven segment display digit detection
- [HighStock](http://www.highcharts.com/products/highstock) - Javascript library for graphing data
- [highcharts-regression](https://github.com/streamlinesocial/highcharts-regression) - Regression lines for Highcharts / HighStock
- [Bootstrap](http://getbootstrap.com/) - CSS and Javascript library for layouts
- [Bower](http://bower.io/) - Front-End web dependency management
