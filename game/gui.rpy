﻿################################################################################
## Initialization
################################################################################

## The init offset statement causes the initialization statements in this file
## to run before init statements in any other file.
init offset = -2

## Calling gui.init resets the styles to sensible default values, and sets the
## width and height of the game.
init python:
    gui.init(1920, 1080)


################################################################################
## GUI Configuration Variables
################################################################################
## Some choice gui values have been left in, to make them
## easier to adjust for accessibility purposes e.g. to allow
## players to change the default text font or size by rebuilding the gui.
## You may add more back if you need to adjust them, or find-and-replace
## any instances where they are used directly with their value.

# The text font for dialogue and choice menus
define gui.text_font = gui.preference("font", "Abaddon Bold.ttf")
# The text font for buttons
define gui.interface_text_font = gui.preference("interface_font", "NFPixels-Regular.otf")
# The default size of in-game text
define gui.text_size = gui.preference("size", 36)
# The font for character names
define gui.name_text_font = gui.preference("name_font", "Sonic2HUD.ttf")
# The size for character names
define gui.name_text_size = gui.preference("name_size", 48)

## Localization ################################################################

## This controls where a line break is permitted. The default is suitable
## for most languages. A list of available values can be found at
## https://www.renpy.org/doc/html/style_properties.html#style-property-language

define gui.language = "unicode"


################################################################################
## Style Initialization
################################################################################

init offset = -1

################################################################################
## Styles
################################################################################

style default:
    font gui.text_font
    antialias False
    hinting "bytecode"
    size gui.text_size
    language gui.language

style input:
    adjust_spacing False

style hyperlink_text:
    hover_underline True

style gui_text:
    color '#130c17'
    size gui.text_size
    font gui.interface_text_font

style button:
    xysize (None, None)
    padding (0, 0)

style button_text:
    is gui_text
    yalign 0.5
    xalign 0.0
    ## The color used for a text button when it is neither selected nor hovered.
    idle_color '#888888'
    ## The color that is used for buttons and bars that are hovered.
    hover_color '#e0e066'
    ## The color used for a text button when it is selected but not focused. A
    ## button is selected if it is the current screen or preference value.
    selected_color '#ffffff'
    ## The color used for a text button when it cannot be selected.
    insensitive_color '#8888887f'

style label_text:
    font gui.name_text_font
    size 36
    kerning 1
    color '#432641'


style bar:
    ysize 38
    left_bar Frame("gui/bar/left.png", 6, 6, 6, 6, tile=False)
    right_bar Frame("gui/bar/right.png", 6, 6, 6, 6, tile=False)

style vbar:
    xsize 38
    top_bar Frame("gui/bar/top.png", 6, 6, 6, 6, tile=False)
    bottom_bar Frame("gui/bar/bottom.png", 6, 6, 6, 6, tile=False)

style scrollbar:
    ysize 24
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", 12, 0, tile=True)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", 0, 0, tile=False)
    unscrollable 'hide'

style vscrollbar:
    xsize 24
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", 6, 6, 6, 6, tile=False)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", 6, 6, 6, 6, tile=False)
    unscrollable 'hide'

style slider:
    ysize 52
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", 16, 12, tile=True)
    left_gutter 16
    right_gutter 16
    thumb "gui/slider/horizontal_[prefix_]thumb.png"
    thumb_offset 26

style vslider:
    xsize 52
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", 12, 16, tile=True)
    top_gutter 16
    bottom_gutter 16
    thumb "gui/slider/vertical_[prefix_]thumb.png"
    thumb_offset 26


style frame:
    padding (6, 6, 6, 6)
    background Frame("gui/frame.png", 8, 8, tile=False)
