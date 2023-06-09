## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it in front of the text.
    add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

# Style for the dialogue window
style window:
    xalign 0.5
    xfill True
    yalign 0.9
    ysize 340
    background Image("gui/textbox.png", xalign=0.5, yalign=0.9)

# Style for the dialogue
style say_dialogue:
    color "#130c17"
    xpos 400
    xsize 1100
    ypos 135
    font gui.text_font
    adjust_spacing False

# The style for dialogue said by the narrator
style say_thought:
    is say_dialogue

# Style for the box containing the speaker's name
style namebox:
    xpos 360
    ysize 120
    xsize 580
    background Frame("gui/namebox.png", 153, 60, 120, 8, tile=True, xalign=0.0)
    padding (5, 5, 5, 5)

# Style for the text with the speaker's name
style say_label:
    font gui.name_text_font
    color '#dbcfb1'
    kerning 1
    xpos 160
    ypos 63
    size 48

## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            imagebutton:
                auto "gui/button/back_button_%s.png"
                action Rollback(greedy=False)
                tooltip _("Back")
            imagebutton:
                auto "gui/button/history_button_%s.png"
                action ShowMenu('history')
                tooltip _("History")
            imagebutton:
                auto "gui/button/skip_button_%s.png"
                action Skip()
                alternate Skip(fast=True, confirm=True)
                tooltip _("Skip")
            imagebutton:
                auto "gui/button/auto_button_%s.png"
                action Preference("auto-forward", "toggle")
                tooltip _("Auto forward")
            imagebutton:
                auto "gui/button/save_button_%s.png"
                action ShowMenu('save')
                tooltip _("Save")
            imagebutton:
                auto "gui/button/load_button_%s.png"
                action ShowMenu('load')
                tooltip _("Load")
            imagebutton:
                auto "gui/button/preferences_button_%s.png"
                action ShowMenu('preferences')
                tooltip _("Preferences")
        
        $ tooltip = GetTooltip()

        if tooltip:
            nearrect:
                focus "tooltip"
                prefer_top False
                yoffset 5

                frame:
                    background "#130c17"
                    xalign 0.5
                    xpadding 12
                    top_padding 2
                    bottom_padding 6
                    text tooltip font gui.interface_text_font textalign 0.5 size 24


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_hbox:
    xalign 0.5
    yalign 0.96
    spacing 16


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox
        spacing 15

        use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit True

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = 6

# The style for the NVL "textbox"
style nvl_window:
    is default
    xfill True yfill True
    background "gui/nvl.png"
    padding (0, 15, 0, 30)

# The style for the text of the speaker's name
style nvl_label:
    is say_label
    xpos 645 xanchor 1.0
    ypos 0 yanchor 0.0
    xsize 225
    min_width 225
    text_align 1.0

# The style for dialogue in NVL
style nvl_dialogue:
    is say_dialogue
    xpos 675
    ypos 12
    xsize 885
    min_width 885

# The style for dialogue said by the narrator in NVL
style nvl_thought:
    is nvl_dialogue

style nvl_button:
    xpos 675
    xanchor 0.0

## Click-to-continue screen ####################################################
##
## The ctc screen is displayed when dialogue has finished showing, to prompt 
## the player to click to display more text
##
## https://www.renpy.org/doc/html/screen_special.html#ctc-click-to-continue

screen ctc(arg=None):

    zorder 100
    style_prefix "ctc"

    add arg

    hbox:
        xalign 0.8
        yalign 0.9
        at ctc_appear
        
        imagebutton:
            idle "gui/button/continue_button_idle.png"
            hover "gui/button/continue_button_hover.png"


transform ctc_appear:
    alpha 0.0
    pause 1.0
    linear 0.5 alpha 1.0
