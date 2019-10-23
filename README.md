# geoqr
Quickly generate a QR code based on supplied GPS coordinates or map service URLs

# Requirements
Until (unless) I package this correctly, the user must install the qrcode python 
module using their package manager of choice. https://pypi.org/project/qrcode/

# Compatibility
This has only been tested against modern Linux and OS X operating systems running 
Python2.7. As far as I am aware this should be OS and Python version -agnostic as 
only standard libraries are used (outside of the qrcode module which does work on 
Windows.)

# Usage
Run the script using whatever python interpreter is at hand, and supply either a 
URL from a map service (Google Maps and OpenStreetMap currently supported) or GPS 
coordinates in standard &lt;lat&gt;,&lt;lon&gt; format.

# Output format
The image will be output as a JPG QR image. I may allow other image formats in the 
future, if I can get the necessary packages correct in the requirements.

The actual encoded data is a string with a geo: URL prefix. This should trigger the 
default map application on any modern smartphone to open to the encoded location.

# Output locations
If no --output argument is provided by the user, a filename will be generated from 
coordinates in the current directory. Users can specify either filename, output 
directory (ends in / or \, depending on your OS), or both. See the examples below.

# Warnings
There is no user-confirmation necessary to overwrite existing files. You should not 
be able to wipe out entire directories, but if you were to point the output to 
a necessary system file you might be able to break something.

# Examples
## With URL:
    /usr/bin/python geoqr-generator.py --url https://www.google.com/maps/place/Mount+Fuji/@35.3606247,138.7186086,15z/data=!3m1!4b1!4m5!3m4!1s0x6019629a42fdc899:0xa6a1fcc916f3a4df!8m2!3d35.3606255!4d138.7273634
## With Coordinates:
    /usr/bin/python geoqr-generator.py --coordinates 35.3606247,138.7186086
    Creates: <current_directory>/35.3606247_138.7186086.jpg
## With manual output name to the current directory:
    /usr/bin/python geoqr-generator.py --coordinates 35.3606247,138.7186086 --output mtfuji.jpg
    Creates: <current_directory>/mtfuji.jpg
## With no filename to an output directory:
    /usr/bin/python geoqr-generator.py --coordinates 35.3606247,138.7186086 --output /Users/myuser/images/
    Creates: /Users/myuser/images/35.3606247_138.7186086.jpg
## With manual output name to another directory:
    /usr/bin/python geoqr-generator.py --coordinates 35.3606247,138.7186086 --output /Users/myuser/images/mtfuji.jpg
    Creates: /Users/myuser/images/mtfuji.jpg
## Example Image Output:
![Example JPG](Mount+Fuji.jpg)
