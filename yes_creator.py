#!/usr/bin/env python3
"""
GUI
"""


__author__ = "David Cirella"
__version__ = "0.1.3"
__license__ = "MIT"

# import wx
from gooey import Gooey, GooeyParser
import yesc.yesc as yesc


localAIPstr = ''
sips_out_path = ''

## user set defaults
default_security_tag = 'open'

# Gooey options for form elements
item_dark = {
        'error_color': '#ea7878',
        'label_color': '#1c2833',
        'label_bg_color': '#eaeded', 
        'help_color': '#1c2833',
        'help_bg_color': '#eaeded', 
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

item_light = {'show_label' : True}

group_dark = {'label_color': '#ffffff', 'description_color': '#ffffff'}

#if gooey_opts = 'dark':
#else:
    
gooey_dark = {'body_bg_color' : '#262626', 'header_bg_color' : '#262626'}

#[body_bg_color='#262626', header_bg_color='#262626', footer_bg_color='#262626', sidebar_bg_color='#262626', terminal_panel_color='#262626']

item_default = item_light
gooey_default = ''

# Primary Gooey settings and About menu info
@Gooey(program_name='YES Creator',tabbed_groups=True, advanced=True, default_size=(750, 1050),  menu=[{'name': 'Help', 'items': [{
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
]}], show_restart_button=False)
def main():
    
    # system color handling
    #print(wx.SystemSettings.GetAppearance().IsUsingDarkBackground())
    #print(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

    
    global sips_out_path 
    
    # Gooey parser creation
    parser = GooeyParser(description='Create SIPs for Preservica v6')
    
    # parser groups, each group displays as tab in UI
    main_group = parser.add_argument_group(
    "Package options"
        )
    #main_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}

    '''
    ob_group = parser.add_argument_group(
    "Object Options", 
    "Options for folders and assets"
        )
     '''   
        
    
    io_group = parser.add_argument_group("Information Object Options",
    )
    
    so_group = parser.add_argument_group("Structural Object Options",
    )
    
    #so_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}

    #io_group = parser.add_argument_group(
    #"Information Objects Options", 
    #"Options for Information Objects"
    #    )
    #io_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}
        
    sync_group = parser.add_argument_group(
    "Sync Options", 
    "Options for Sync"
        )
    #sync_group.gooey_options = {'label_color': '#ffffff', 'description_color': '#ffffff'}

    


    # args from GUI, map to cli args in library
    main_group.add_argument("-input", "-i", "--input", widget='DirChooser', help='Directory containing files to package', gooey_options=item_default, metavar='Input')
    main_group.add_argument("-output", "-o", "--output", widget='DirChooser', help='Directory to export the SIP to', gooey_options=item_default, metavar='Output')
    
    main_group.add_argument("-parent", "-p", "--parent", default='None', help='Parent or destination reference', gooey_options=item_default, metavar='Destination Collection')
    main_group.add_argument("-securitytag", "-s", "--securitytag", default=default_security_tag, help='Security tag for objects in sip', gooey_options=item_default, metavar='Security Tag')
    
   
    ob_type_group = main_group.add_argument_group(
    "Package Type Options", gooey_options={
            'show_border': True, 'full_width': False
        }
        )
    
    fixity_algo = main_group.add_mutually_exclusive_group(
        required=True,
        gooey_options={
            'initial_selection': 3, 'show_border': True
        }
    )
    
    
    ob_type_group.add_argument("-assetonly", "-a", "--assetonly", action='store_true', help='Ingest files as assets (no folder)', gooey_options={'full_width': False,'show_label' : True}, metavar='Assets Only')
    ob_type_group.add_argument("-singleasset", "-sa", "--singleasset", action='store_true', help='Ingest multiple files as single asset, -parent uuid required', gooey_options={'full_width': False,'show_label' : True}, metavar='Single Asset (mult files)')
    
    
    
    sync_group.add_argument("-aspace", "-ao", "--aspace", help='ArchivesSpace archival object reference: archival_object_5555555', gooey_options=item_default, metavar='Archival Object Ref')
    
    
    
    
    
    
    so_group.add_argument("-sotitle", "-sot", "--sotitle", help='Title for folder', gooey_options=item_default, metavar='SO Title')
    so_group.add_argument("-sodescription", "-sod", "--sodescription", help='Description field for the folder', gooey_options=item_default, metavar='SO Description')
    so_group.add_argument("-sometadata", "-som", "--sometadata", help='Embed content of XML file as metadata linked to SO', widget='FileChooser',gooey_options={'full_width': True}, metavar='SO Metadata to embed')
    so_group.add_argument("-soidtype", "-soidt", "--soidtype", help='Identifier type for all SO', gooey_options=item_default, metavar='SO id Type')
    so_group.add_argument("-soidvalue", "-soidv", "--soidvalue", help='Identifier value for all SO', gooey_options=item_default, metavar='SO id Value')

    io_group.add_argument("-iotitle", "-iot", "--iotitle", default=0, help='Title for IO, Asset', gooey_options=item_default, metavar='IO Title')
    io_group.add_argument("-iodescription", "-iod", "--iodescription", help='Description field for all Information Objects', gooey_options=item_default, metavar='IO Description')
    
    io_group.add_argument("-iometadata", "-iom", "--iometadata", help='Embed content of XML file as metadata linked to IO', widget='FileChooser',gooey_options={'full_width': True}, metavar='IO Metadata to embed')

    io_group.add_argument("-ioidtype", "-ioidt", "--ioidtype", help='Identifier type for all IOs', gooey_options=item_default, metavar='IO id Type')
    io_group.add_argument("-ioidvalue", "-ioidv", "--ioidvalue", help='Identifier value for all IOs', gooey_options=item_default, metavar='IO id Value')
   
   
   

    ob_type_group.add_argument("-representations", "-manifestations", "-r", "--representations", action='store_true', help='Structure should follow the multiple manifestation package definition with manifestation folders of the form *preservica_(presentation| preservation', gooey_options={'full_width': False,'show_label' : True}, metavar='Multi-represenations')
    ob_type_group.add_argument("-sipconfig", "-sc", "--sipconfig", help='Location of sip config', widget='FileChooser', gooey_options={'full_width': False,'show_label' : True}, metavar='SIPConfig')
    
    
    
  
   

    
    fixity_algo.add_argument("-md5", "--md5", action='store_true', help='fixity values will  be generated using the MD5 algorithm', gooey_options=item_default, metavar='MD5')
    fixity_algo.add_argument("-sha1", "--sha1", action='store_true', help='fixity values will be generated using the SHA1 algorithm', gooey_options=item_default, metavar='SHA1')
    fixity_algo.add_argument("-sha256", "--sha256", action='store_true', help='fixity values will be generated using the SHA256 algorithm', gooey_options=item_default, metavar='SHA256')
    fixity_algo.add_argument("-sha512", "--sha512", action='store_true', help='fixity values will be generated using the SHA512 algorithm', gooey_options=item_default, metavar='SHA512')
    
    
    main_group.add_argument("-export", "-e", "--export", action='store_true', default=True, help='Export files to content subdirectory of sip', gooey_options=item_default, metavar='Export')
    
    main_group.add_argument("-excludedFileNames", "-ef", "--excludedFileNames", default='', help='Comma separated list of file names to  exclude during SIP creation')
    
    args = parser.parse_args()
        
    # calls module with args from GUI input
    yesc.main(args)
    
    

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
