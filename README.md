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
- Install ffmpeg [here](https://www.reddit.com/r/raspberry_pi/comments/1yja3h/latest_ffmpeg_crosscompiled_for_pi/)
- Install opencv 2 [here](https://github.com/Nolaan/libopencv_24/releases)
- Install ssocr
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

## Projects Used
- [OpenCV for Python](http://opencv.org/) - Open source computer vision library
- [ssocr](https://www.unix-ag.uni-kl.de/~auerswal/ssocr/) - Seven segment display digit detection
- [HighStock](http://www.highcharts.com/products/highstock) - Javascript library for graphing data
- [Bootstrap](http://getbootstrap.com/) - CSS and Javascript library for layouts
- [Bower](http://bower.io/) - Front-End web dependency management
