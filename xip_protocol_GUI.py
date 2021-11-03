#!/usr/bin/env python3
"""
GUI
"""


__author__ = "David Cirella"
__version__ = "0.1.3"
__license__ = "MIT"

from gooey import Gooey, GooeyParser
import shutil
import argparse
import hashlib
import uuid
import datetime
import xml.etree.ElementTree as et
from xml.dom import minidom
from lxml import etree
from pathlib import Path

import xip_protocol


localAIPstr = ''
sips_out_path = ''


## user set defaults
default_security_tag = 'open'



@Gooey()
def main():
    global sips_out_path 
    
    #parser = argparse.ArgumentParser()
    parser = GooeyParser()

    # Optional argument flag 
    parser.add_argument("-input", "-i", "--input", widget='DirChooser', help='Directory containing content files')
    parser.add_argument("-output", "-o", "--output", widget='DirChooser', help='Directory to export the SIP to')
    parser.add_argument("-sotitle", "-sot", "--sotitle", default=0, help='Title for structural object')
    parser.add_argument("-parent", "-p", "--parent", default=None, help='Parent or destination reference')
    parser.add_argument("-securitytag", "-s", "--securitytag", default=default_security_tag, help='Security tag for objects in sip')
    parser.add_argument("-assetonly", "-a", "--assetonly", action='store_true', help='Ingest files as assets (no folder)')
    parser.add_argument("-export", "-e", "--export", action='store_true', help='Export files to content subdirectory of sip')
    parser.add_argument("-aspace", "-ao", "--aspace", help='ArchivesSpace archival object reference: archival_object_5555555')
    parser.add_argument("-sodescription", "-sod", "--sodescription", help='Description field for Structural Objects')
    parser.add_argument("-iodescription", "-iod", "--iodescription", help='Description field for all Information Objects')
    
    parser.add_argument("-sometadata", "-som", "--sometadata", help='Embed content of XML file as metadata linked to SO')
    parser.add_argument("-iometadata", "-iom", "--iometadata", help='Embed content of XML file as metadata linked to IO')

    parser.add_argument("-ioidtype", "-ioidt", "--ioidtype", help='Identifier type for all IOs')
    parser.add_argument("-ioidvalue", "-ioidv", "--ioidvalue", help='Identifier value for all IOs')
    
    parser.add_argument("-soidtype", "-soidt", "--soidtype", help='Identifier type for all SO')
    parser.add_argument("-soidvalue", "-soidv", "--soidvalue", help='Identifier value for all SO')


    parser.add_argument("-md5", "--md5", action='store_true', help='fixity values will  be generated using the MD5 algorithm')
    parser.add_argument("-sha1", "--sha1", action='store_true', help='fixity values will be generated using the SHA1 algorithm')
    parser.add_argument("-sha256", "--sha256", action='store_true', help='fixity values will be generated using the SHA256 algorithm')
    parser.add_argument("-sha512", "--sha512", action='store_true', help='fixity values will be generated using the SHA512 algorithm')
    
    args = parser.parse_args()
    
    xip_protocol_test.main(args)
    
    # call module

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
