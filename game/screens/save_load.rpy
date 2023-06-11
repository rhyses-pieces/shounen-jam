## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save
## https://www.renpy.org/doc/html/screen_special.html#load

## The width and height of thumbnails used by the save slots.
define config.thumbnail_width = 380
define config.thumbnail_height = 212


screen save():

    tag menu

    add "#91e8fe72" # The background; can be whatever

    use file_slots(_("Save"))

    text "Choose a slot to save in":
        xalign 0.5


screen load():

    tag menu

    add "#91fefc72" # The background; can be whatever

    use file_slots(_("Load"))

    frame:
        xalign 0.65
        ypos 150
        background "#000"
        
        text "Choose a file to load"

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(
        pattern=_("Page {}"), auto=_("Automatic saves"),
        quick=_("Quick saves"))

    use game_menu(title)

    fixed:
        xsize 1500 xalign 1.0
        ## This ensures the input will get the enter event before any of the
        ## buttons do.
        order_reverse True

        ## The page name, which can be edited by clicking on it.
        ## This can be pretty easily removed if you want.
        ## Don't forget to also remove the `default` at the top if so.
        button:
            style "page_label"
            key_events True
            action page_name_value.Toggle()

            input:
                style "page_label_text"
                value page_name_value

        frame:
            xsize 1300
            ysize 670
            xpos 77
            yalign 0.5
            padding (20, 20)

            ## The grid of file slots.
            grid 3 2:
                style_prefix "slot"

                for i in range(3*2):
                    $ slot = i + 1

                    button:
                        action FileAction(slot)
                        has vbox
                        $ file_time = FileTime(slot, format=u'%b %d %Y, %I:%M %p', empty=_("empty slot"))

                        add FileScreenshot(slot) xalign 0.5 xoffset 1
                        use file_info(slot, file_time)

                        # This means the player can hover this save
                        # slot and hit delete to delete it
                        key "save_delete" action FileDelete(slot, confirm=True)

        ## Buttons to access other pages.
        hbox:
            style_prefix "page"

            textbutton _("<") action FilePagePrevious()

            if config.has_autosave:
                textbutton _("{#auto_page}A") action FilePage("auto")

            if config.has_quicksave:
                textbutton _("{#quick_page}Q") action FilePage("quick")

            ## range(1, 10) gives the numbers from 1 to 9.
            for page in range(1, 10):
                textbutton "[page]" action FilePage(page)

            textbutton _(">") action FilePageNext()


screen file_info(slot, file_time):

    style_prefix "file"

    frame:
        xsize config.thumbnail_width
        ysize 80
        xpos 1
        
        has hbox
        xfill True

        vbox:
            align (0.5, 0.5)
            xpos 170
            
            text "File [slot]" style "slot_time_text"
            null height 5
            text "[file_time]" style "slot_time_text"
        vbox:
            xalign 1.0

            imagebutton:
                idle "gui/button/button_trash.png"
                hover "gui/button/button_trash.png"
                action FileDelete(slot, confirm=True, page=None)


style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color '#e0e066'

style slot_grid:
    xalign 0.5
    yalign 0.5
    spacing 15

style slot_time_text:
    size 25
    xalign 0.5

style slot_button:
    xysize (414, 309)
    padding (15, 15, 15, 15)
    background "gui/button/slot_[prefix_]background.png"

style slot_button_text:
    size 21
    xalign 0.5
    idle_color '#aaaaaa'
    hover_color '#e0e066'
    selected_idle_color '#ffffff'

style page_hbox:
    xalign 0.5
    yalign 1.0
    spacing 5

style page_button:
    padding (15, 6, 15, 6)

style file_frame:
    background None

style file_text:
    is button_text
    size 24
    color '#fff'