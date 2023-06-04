## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

default timeout = 5.0
default timeout_label = None
default persistent.timed_choices = True

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action
    
    if (timeout_label is not None) and persistent.timed_choices:
        bar:
            xalign 0.5
            ypos 400
            xsize 740
            value AnimatedValue(old_value = 1.0, value = 0.0, range = 1.0, delay = timeout)
        
        timer timeout action Jump(timeout_label)


style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5
    spacing 33

style choice_button:
    is default # This means it doesn't use the usual button styling
    xysize (1185, 84)
    background Frame("gui/button/choice_[prefix_]background.png",
        150, 8, 150, 8, tile=False)

style choice_button_text:
    is default # This means it doesn't use the usual button text styling
    xalign 0.5
    yalign 0.5
    idle_color "#ccc"
    hover_color "#fff"
    insensitive_color "#444"