# -*- coding: UTF-8 -*-
#
#    Assistant for RoboFont4
#    Using TYPETR-Assistant library classes.
#
#    MyAssistant-001.py
#
#    In general, Asistant modules should only print to the console of something is change or wrong.
#    Regarding report prints, Assistant code has the following meanings:
#    "..." is an processing report, a value or measure in the data, "all is going well, this is in an intended function."
#    "###" is an error in the Assistant module code. "this should not happen, check the code"
#    "@@@" is for generic messages during initialization, such as adding the AssistantLib path to RoboFont.
#    All other message are only of the purpose of debugging and should be remove overtime.
#
import sys, os
import importlib
 
# In the same local folder as this source, the masterData.py should exist. It contains all info about the
# masters that cannot be defined in font.info.
# In case there are already UFO files and not a masterData.py, just create it with an empty dictionary:
# MASTER_DATA = {} or catch the import error.
# The MasterDataManager will recognize that the MasterData of some UFO's does not exist, and it will create
# them accordingly. Don't add comments, since the will be written again for every UFO that is added later
# (which will then remove your comments).

import myMasterData
importlib.reload(myMasterData)
from myMasterData import MASTERS_DATA

# Add paths to libs in sibling repositories. The assistantLib module contains generic code for Asistanta.s
PATHS = ['../TYPETR-TypeLab-Club-Assistants/'] # Relative path to this respository that holds AssistantLib
for path in PATHS:
    if not os.path.exists(path):
        print(f'@@@ Locate this file on the top of the project repository and make sure that {path} exists.')
    if not path in sys.path:
        print(f'@@@ Append {path} to sys.path')
        sys.path.append(path)

# First import the modules that we need for this Assistant
# For more modules, other imports will be added.
import assistantLib.toolbox
import assistantLib.baseAssistant
import assistantLib.assistantModules.data # This contains the MasterData class that keeps information for each master.
import assistantLib.assistantModules.builder
import assistantLib.assistantModules.overlay
import assistantLib.assistantModules.glyphsets.Latin_S_set

# Reload the imports, in case they were already imported and their sources changed while RoboFont is open.
importlib.reload(assistantLib.toolbox)
importlib.reload(assistantLib.baseAssistant)
importlib.reload(assistantLib.assistantModules.data)
importlib.reload(assistantLib.assistantModules.overlay)

# Reload some more stuff, just in case.
importlib.reload(assistantLib.assistantModules.glyphsets.anchorData)
importlib.reload(assistantLib.assistantModules.glyphsets.groupBaseGlyphs)
importlib.reload(assistantLib.assistantModules.glyphsets.glyphSet)
importlib.reload(assistantLib.assistantModules.glyphsets.Latin_S_set)
importlib.reload(assistantLib.assistantModules.glyphsets.glyphData)

# Import the two base classes
# Assistant is inheriting from the RoboFont Subscriber class. It will take care of events happening in RoboFont, such as selecting a new glyph.
# Each opened font will have its own Assistant instance, handling the events from RoboFont separately.
# AssistantController inherits from WindowController. It create the Assistant window and will mainly respond to user-manipulation of the UI controls
from assistantLib.baseAssistant import (Assistant, AssistantController)
import assistantLib.assistantModules.overlay
from assistantLib.assistantModules.overlay import AssistantModuleOverlay

# The MasterDataManager answers a dictionary of MasterData instances. It is imported from the locel myMasterData.py
# but if the MasterDataManager detects that the file does not exist, it will be created first, filling the values
# as accurate a possible based on guessing from the existing UFO masters in the ufo/ folder.
# MasterData instances will hold specific additional data for each master, that cannot be retrieved
# from the standard font.info
import assistantLib.assistantModules.data
importlib.reload(assistantLib.assistantModules.data)
from assistantLib.assistantModules.data import MasterDataManager

# For this demo we use a small Latin set. For real project, there's a choice from multiple standardized glyphsets.
# Also the choice between Roman and Italic needs another glyphset as import.
from assistantLib.assistantModules.glyphsets.glyphSet import GlyphSet
from assistantLib.assistantModules.glyphsets.Latin_S_set import LATIN_S_SET_NAME

from assistantLib.toolbox import path2Dir

THIS_PROJECT_PATH =  path2Dir(__file__) # Get the path to this project directory

# TypeLabClub Demo Assistant, inherits from the module classes that need to implemented
class TLCDemoAssistant( # Eacht masters has its own, responding to a varaiety of RoboFont/EditWindow/Events
        Assistant, # Inheriting from Subscriber
        AssistantModuleOverlay, # Inheriting from WindowController. Adds library module functions as inherited class.
	):
    # These get called on opening the Installer window, defining the elements that draw in the EditorWindow
    INIT_MERZ_METHODS = [ 
        'initMerzOverlay',
    ]
    # Allow the subscribed assistant parts to update the Merz elements.
    UPDATE_MERZ_METHODS = [ 
        'updateMerzOverlay',
    ] 
    SET_GLYPH_METHODS = [
        
    ]
class TLCDemoAssistantController( # Single Assistant window that creates/communicates with the Assistant subscribers.
        AssistantController, 
        AssistantModuleOverlay, # Add library function part source as inherited class.
	):
    W = 450 # Width and height of the Assistant window
    H = 250

    # Overlay colors
    OVERLAY_FILL_SRC_COLOR = 0, 0.3, 0.8, 0.3
    OVERLAY_FILL_COLOR = 0, 0, 0, 0.3
    
    NAME = 'TypLab-Club Demo Assistant' # Name of the Assistant window

    PROJECT_PATH = THIS_PROJECT_PATH # Let the AssistantContoller know where this proj4ct file is.
    ADD_GLOBAL_BUTTONS = False # For now, keep it simple, supressing the BaseAssistant show the buttons at the bottom

    UFO_PATH = 'ufo/' # This is the relative path of the directory that contains all UFO masters
    PROJECT_PATH = THIS_PROJECT_PATH # Set the absolute path of this project (different for every user)
    
	# Always define the UFO file names as variables. This way accidental tupos are deteted by the Python compiler
	# and UFO file names can be change during the deisgn process, e.g. pointing to other versions
	# This way there is no need to find/replace names in the entire source.
    UPGRADE_TRY_LIGHT      = 'Upgrade_Try-Light.ufo'    UPGRADE_TRY_REGULAR    = 'Upgrade_Try-Regular.ufo'
    UPGRADE_TRY_BOLD       = 'Upgrade_Try-Bold.ufo'
    # Used by familyOverview, defining the order of masters in the top family line that shows in the EditorWindow
    UFO_NAMES = [ # Define the order of display in FamilyOverview
        UPGRADE_TRY_LIGHT,
        UPGRADE_TRY_REGULAR,
        UPGRADE_TRY_BOLD,
    ]
    # Define the glyphSet for this selection of masters.
    # See https://github.com/koeberlin/Latin-Character-Sets
    # There is also LatinM_GlyphSet and LatinL_GlyphSet
    # Custom glyphsets can be added localled and then imported/created as GLYPH_SET    GLYPH_SET = GlyphSet(LATIN_S_SET_NAME) # Make a Small Latin1 glyphset object.  

    # Generate the MasterDataManager instance. This will test if the local masterData.py exists.
    # Otherwise it will be generated as default source.
    MDM = MASTER_DATA_MANAGER = MasterDataManager(MASTERS_DATA, PROJECT_PATH, ufoNames=UFO_NAMES, glyphSet=GLYPH_SET)
    MDM.save()
    
    # The default MASTER_DATA_MANAGER behaves as a dictionary of MasterData instances, derived from the
    # local masterData.py file, as anwered (or generated) by the MasterDataManager look similar to the following: 
    #MASTER_DATA = { # This will contain all meta information about the masters as MasterData instances.
    #    UPGRADE_TRY_LIGHT: MD(
    #        name=UPGRADE_TRY_LIGHT, 
    #        glyphSet=GS,
    #        m0=UFO_PATH + UPGRADE_TRY_REGULAR,
    #    ),
    #    UPGRADE_TRY_REGULAR: MD(
    #        name=UPGRADE_TRY_LIGHT, 
    #        glyphSet=GS,
    #        m0=UFO_PATH + UPGRADE_TRY_REGULAR,
    #    ),      
    #    UPGRADE_TRY_BOLD: MD(
    #        name=UPGRADE_TRY_LIGHT, 
    #        glyphSet=GS,
    #        m0=UFO_PATH + UPGRADE_TRY_BOLD,
    #    ),
    #} 

    BUILD_UI_METHODS = [
        'buildOverlay',
    ]
    assistantGlyphEditorSubscriberClass = TLCDemoAssistant


if __name__ == '__main__':
    OpenWindow(TLCDemoAssistantController)

