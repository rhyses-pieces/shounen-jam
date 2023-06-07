## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

define config.history_length = 250

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    style_prefix "history"

    frame:

        label _("History") style "history_title"

        vpgrid:
            cols 1
            yinitial 1.0
            mousewheel True draggable True pagekeys True
            scrollbars "vertical"

            vbox:

                for h in _history_list:
            
                    window:
                        has fixed:
                            yfit True

                        if h.who:
                            label h.who style 'history_name':
                                substitute False
                                ## Take the color of the who text
                                ## from the Character, if set
                                if "color" in h.who_args:
                                    text_color h.who_args["color"]
                                xsize 200   # this number and the null width
                                            # number should be the same
                        else:
                            null width 200

                        $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                        text what:
                            substitute False

                if not _history_list:
                    label _("The dialogue history is empty.")

        textbutton _("Return") action Return()

## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_frame:
    margin (200, 100)
    padding (40, 100)
    background Frame("gui/frame.png", 8, 8)

style history_vbox:
    spacing 20

style history_window:
    is empty
    xfill True

style history_name:
    xalign 0.0
    ypadding 4
    background '#130c17'

style history_name_text:
    font gui.name_text_font
    text_align 0.5
    align (0.5, 0.5)
    color '#dbcfb1'

style history_text:
    text_align 0.0
    ypos 6
    xpos 220
    xsize 1175
    color '#130c17'

style history_title:
    xfill True
    top_margin -70

style history_title_text:
    font gui.name_text_font
    size 60
    xalign 0.5

style history_button:
    xalign 1.0
    yalign 1.0
    yoffset 60