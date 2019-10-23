#!/usr/bin/python

"""
geoqr-generator.py: Allows the user to generate a QR code in JPG format 
by either providing coordinates in the standard <lat>,<lon> notation or 
by submitting a Google Maps or OpenStreetMap URL from which coordinates 
can be extracting using pattern-matching.
   
The final QR-encoded data will be in the format of a geo: URL, which should 
trigger the default mapping application on any modern smartphone to the                
location determined by the coordinates.

The 'qrcode' package is required; see pypi for installation instructions:
https://pypi.org/project/qrcode/
"""

__author__      = "https://github.com/bushpigadv"
__version__     = 1.14

import optparse
import os
import qrcode
import re
import sys

parser = optparse.OptionParser()
parser.add_option('-c', '--coordinates',
                  default=None,
                  dest='coordinates',
                  help='Specify manual coordinates for the geo link.')
parser.add_option('-u', '--url',
                  default=None,
                  dest='url',
                  help='Submit a URL from Google Maps or OpenStreetMap for '
                  'analysis.')
parser.add_option('-o', '--output',
                  default=None,
                  dest='output',
                  help='Define the output file path (optional) and name. If '
                  'not supplied a name will be generated based on URL content '
                  'or coordinate information.)'
                  )
(options, args) = parser.parse_args()

if not options.coordinates and not options.url:
    sys.exit("Exiting: Please provide either a --url or --coordinates "
    "argument")
if options.coordinates and options.url:
    sys.exit("FATAL: Please provide either --coordinates or --url, but not "
    "both")

# Define the pattern for extracting coordinates and place names from 
# Google Maps or OpenStreetMap URLs
coord_pattern = \
    re.compile(r'[@\/](-{0,1}[0-9]{1,2}\.\d*)[,\/](-{0,1}[0-9]{1,3}\.\d*)')
name_pattern = re.compile(r'(place|query)[=\/]([A-Za-z0-9+%]*)[#\/]')
encoding_pattern = re.compile(r'(%[2-9]{1}[0-9A-F]{1})')

def get_coord_from_url():
    """
    Using regex patterns, we will attempt to extract meaningful GPS coordinate 
    data from the URL provided. 
    """
    try:
        coordinates = re.search(coord_pattern, options.url)
        return coordinates.group(1), coordinates.group(2)
    except AttributeError:
        sys.exit("Unable to extract coordinates from the URL provided: {0} . "
                 "This script expects a Google Maps or OpenStreetMap URL, "
                 "which in Google Maps looks like \'@<lat>,<lon>\' and "
                 "in OpenStreetMap looks like \'/<lat>/<lon>\'. If you "
                 "believe that your URL is correct and this script is failing "
                 "to match the pattern, please submit a bug report and be "
                 "sure to include the URL that is failing to parse.".format(
                     options.url)
                )

def get_place_from_url():
    """
    Using regex patterns, we will attempt to extract some sort of place name 
    from the URL provided. If that fails, the file's name will include the 
    location's coordinates instead.
    """
    try:
        place = re.search(name_pattern, options.url)
        return place.group(2)
    except AttributeError:
        sys.stdout.write("No output filename was provided, and no place name "
            "could be extracted from the URL provided: {0} . Filename will be "
            "created using coordinates instead\n.".format(options.url))
        return False

def determine_output_filename(gps_lat, gps_lon):
    """
    Manipulate either the place name or the GPS coordiantes to create a 
    logical filename for storing the output image.
    """
    if options.url:
        file_prefix = get_place_from_url()
    else:
        file_prefix = False
    
    # If we were able to extract a place name, return but drop encoding chars
    if file_prefix:
        return re.sub(encoding_pattern, '', file_prefix)
    # Else, make a name from the provided coordinates
    else:
        return '{0}_{1}'.format(gps_lat, gps_lon)

def generate_qr(output_fn, output_dir, gps_lat, gps_lon):
    """
    Generate the final QR image and save it to the output location.
    """
    sys.stdout.write("Generating QR Code...")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2
    )
    qr.add_data('geo:{0},{1}'.format(gps_lat, gps_lon))
    qr.make(fit=True)
    img = qr.make_image()

    if not output_fn.endswith('.jpg'):
        output_fn = output_fn + '.jpg'
    else:
        pass
    
    output_path = os.path.join(output_dir, output_fn)
    
    try:
        img.save(output_path)
        sys.stdout.write("QR successfully created at {0}\n".format(
            output_path
            ))
    except Exception, err:
        sys.stdout.write("Encountered an error while attempting to write "
            "the QR image file: {0}. This will normally be a permisions or "
            "file path problem. If you think that this is an issue with the "
            "script, please report a bug and be sure to include the error "
            "message.\n".format(str(err)))

def validate_coordinates(gps_lat, gps_lon):
    try:
        float(gps_lat)
        float(gps_lon)
        sys.stdout.write("Found coordinates: {0},{1}\n".format(
            gps_lat, gps_lon)
            )
    except ValueError:
        sys.exit("Unable to parse provided coordinates: {0} could not be "
        "read as floats. If using the --coorindates argument, ensure that "
        "your coordinates are correct and provided in <lat>,<lon> format with "
        "no special characters, symbols, or letters. If these were "
        "incorrectly parsed from a --url that you provided, please create a "
        "bug report and include the URL.".format(
            options.coordinates
            ))

def main():
    # Get coordinates either from the provided URL or user-supplied coordinates
    if options.url:
        gps_lat, gps_lon = get_coord_from_url()
    else:
        try:
            gps_lat, gps_lon = options.coordinates.split(',')
        except Exception, err:
            sys.exit("Unable to parse provided coordinates: {0}".format(
                str(err)
                ))
    
    # Ensure that our coordinates look like they should
    validate_coordinates(gps_lat, gps_lon)

    # Determine a filename or use the one set by the user with --output
    if not options.output:
        output_fn = determine_output_filename(gps_lat, gps_lon)
        output_dir = os.getcwd()
    else:
        output_fn = os.path.basename(options.output)
        output_dir = os.path.dirname(options.output)
    sys.stdout.write("Determined output location: {0}.jpg\n".format(
        os.path.join(output_dir, output_fn)
        ))
    
    # Attempt to generate the QR image
    generate_qr(output_fn, output_dir, gps_lat, gps_lon)

if __name__ == '__main__':
    main()
    exit()
