# ScaleIoT
OpenCV python program with a simple webpage to track weight readings from a scale.

This project:
- Takes an image from a webcam when scale begins weighing
- Process the image to both reduce noise and crop to the specific section of the display
- Do OCR on the image
- Record data
- Graph data on a web page
- Push to PebbleHealth API (Future)


## Projects Used
- [OpenCV for Python](http://opencv.org/) - Open source computer vision library
- [ssocr](https://www.unix-ag.uni-kl.de/~auerswal/ssocr/) - Seven segment display digit detection
- [HighStock](http://www.highcharts.com/products/highstock) - Javascript library for graphing data
- [Bootstrap](http://getbootstrap.com/) - CSS and Javascript library for layouts
- [Bower](http://bower.io/) - Front-End web dependency management
