## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action
    

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5
    spacing 33

style choice_button:
    is default # This means it doesn't use the usual button styling
    xysize (950, 84)
    background Frame("gui/button/choice_[prefix_]background.png",
        28, 8, tile=True)

style choice_button_text:
    is default # This means it doesn't use the usual button text styling
    font gui.interface_text_font
    xalign 0.5
    yalign 0.5
    idle_color "#ccc"
    hover_color "#fff"
    insensitive_color "#444"
