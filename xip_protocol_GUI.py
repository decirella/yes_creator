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

# Gooey options for form elements
item_default = {
        'error_color': '#ea7878',
        'label_color': '#ffffff',
        'help_color': '#ffffff',
        'full_width': False,
        'validator': {
            'type': 'local',
            'test': 'lambda x: True',
            'message': ''
        },
        'external_validator': {
            'cmd': '',
        }
    }


# Primary Gooey settings and About menu info
@Gooey(program_name='SIPCreator v6',tabbed_groups=True, advanced=True, menu=[{'name': 'Help', 'items': [{
    'type': 'AboutDialog',
    'menuTitle': 'About',
    'name': 'SIP Creator',
    'description': 'v6 SIP Creator',
    'version': '0.0.0',
    'copyright': '2021',
    'website': 'https://github.com/decirella',
    'developer': 'https://github.com/decirella',
    'license': 'MIT'
}
]}], body_bg_color='#262626', header_bg_color='#262626', footer_bg_color='#262626', sidebar_bg_color='#262626', terminal_panel_color='#262626', show_restart_button=False)
def main():
    global sips_out_path 
    
    # Gooey parser creation
    parser = GooeyParser(description='Create SIPs for Preservica v6')
    
    # parser groups, each group displays as tab in UI
    main_group = parser.add_argument_group(
    "Main options", 
    "Main options"
        )
    main_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}

    so_group = parser.add_argument_group(
    "SO Options", 
    "Options for Structural Objects"
        )
    so_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}

    io_group = parser.add_argument_group(
    "IO Options", 
    "Options for Information Objects"
        )
    io_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}
        
    sync_group = parser.add_argument_group(
    "Sync Options", 
    "Options for Sync"
        )
    sync_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}


    # args from GUI, map to cli args in library
    main_group.add_argument("-input", "-i", "--input", widget='DirChooser', help='Directory containing content files', gooey_options=item_default)
    main_group.add_argument("-output", "-o", "--output", widget='DirChooser', help='Directory to export the SIP to', gooey_options=item_default)
    so_group.add_argument("-sotitle", "-sot", "--sotitle", default=0, help='Title for structural object', gooey_options=item_default)
    main_group.add_argument("-parent", "-p", "--parent", default=None, help='Parent or destination reference', gooey_options=item_default)
    main_group.add_argument("-securitytag", "-s", "--securitytag", default=default_security_tag, help='Security tag for objects in sip', gooey_options=item_default)
    main_group.add_argument("-assetonly", "-a", "--assetonly", action='store_true', help='Ingest files as assets (no folder)', gooey_options=item_default)
    main_group.add_argument("-export", "-e", "--export", action='store_true', help='Export files to content subdirectory of sip', gooey_options=item_default)
    sync_group.add_argument("-aspace", "-ao", "--aspace", help='ArchivesSpace archival object reference: archival_object_5555555', gooey_options=item_default)
    so_group.add_argument("-sodescription", "-sod", "--sodescription", help='Description field for Structural Objects', gooey_options=item_default)
    io_group.add_argument("-iodescription", "-iod", "--iodescription", help='Description field for all Information Objects', gooey_options=item_default)
    
    so_group.add_argument("-sometadata", "-som", "--sometadata", help='Embed content of XML file as metadata linked to SO', gooey_options=item_default)
    io_group.add_argument("-iometadata", "-iom", "--iometadata", help='Embed content of XML file as metadata linked to IO', gooey_options=item_default)

    io_group.add_argument("-ioidtype", "-ioidt", "--ioidtype", help='Identifier type for all IOs', gooey_options=item_default)
    io_group.add_argument("-ioidvalue", "-ioidv", "--ioidvalue", help='Identifier value for all IOs', gooey_options=item_default)
    
    so_group.add_argument("-soidtype", "-soidt", "--soidtype", help='Identifier type for all SO', gooey_options=item_default)
    so_group.add_argument("-soidvalue", "-soidv", "--soidvalue", help='Identifier value for all SO', gooey_options=item_default)

    '''
    main_group.add_argument("-md5", "--md5", action='store_true', help='fixity values will  be generated using the MD5 algorithm', gooey_options=item_default)
    main_group.add_argument("-sha1", "--sha1", action='store_true', help='fixity values will be generated using the SHA1 algorithm', gooey_options=item_default)
    main_group.add_argument("-sha256", "--sha256", action='store_true', help='fixity values will be generated using the SHA256 algorithm', gooey_options=item_default)
    main_group.add_argument("-sha512", "--sha512", action='store_true', help='fixity values will be generated using the SHA512 algorithm', gooey_options=item_default)
    '''
    
    fixity_algo = main_group.add_mutually_exclusive_group(
        required=True,
        gooey_options={
            'initial_selection': 3, 'label_color': '#ffffff', 'description_color': '#ffffff'
        }
    )

    
    fixity_algo.add_argument("-md5", "--md5", action='store_true', help='fixity values will  be generated using the MD5 algorithm', gooey_options=item_default)
    fixity_algo.add_argument("-sha1", "--sha1", action='store_true', help='fixity values will be generated using the SHA1 algorithm', gooey_options=item_default)
    fixity_algo.add_argument("-sha256", "--sha256", action='store_true', help='fixity values will be generated using the SHA256 algorithm', gooey_options=item_default)
    fixity_algo.add_argument("-sha512", "--sha512", action='store_true', help='fixity values will be generated using the SHA512 algorithm', gooey_options=item_default)
    
    
    
    args = parser.parse_args()
    
    # calls module with args from GUI input
    xip_protocol.main(args)
    
    

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
