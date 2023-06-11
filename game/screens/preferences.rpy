## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    add "#a8845dad" # The background; can be whatever

    use game_menu(_("Preferences"))

    style_prefix "pref"

    frame:
        has vbox
        xalign 0.5

        hbox:

            if renpy.variant("pc") or renpy.variant("web"):
                # Only need fullscreen/windowed on desktop and web builds

                vbox:
                    style_prefix "radio"
                    label _("Display")
                    textbutton _("Window"):
                        # Ensures this button is selected when
                        # not in fullscreen.
                        selected not preferences.fullscreen
                        action Preference("display", "window")
                    textbutton _("Fullscreen"):
                        action Preference("display", "fullscreen")

            vbox:
                style_prefix "check"
                label _("Skip")
                textbutton _("Unseen Text"):
                    action Preference("skip", "toggle")
                textbutton _("After Choices"):
                    action Preference("after choices", "toggle")
                textbutton _("Transitions"):
                    action InvertSelected(Preference("transitions", "toggle"))

            ## Additional vboxes of type "radio_pref" or "check_pref" can be
            ## added here, to add additional creator-defined preferences.
            vbox:
                style_prefix "check"
                label _("Accessibility")
                textbutton _("Sound Captions"):
                    action ToggleVariable("persistent.sound_captions")
                textbutton _("Image Captions"):
                    action ToggleVariable("persistent.image_captions")
                textbutton _("Timed Choices"):
                    action ToggleVariable("persistent.timed_choices")
                # Self-voicing does not work on smartphone devices, so this option only shows if the user is playing on a PC.
                if renpy.variant("pc"):
                    textbutton _("Self-Voicing"):
                        action Preference("self voicing", "toggle")
                # This shows Ren'Py's built-in accessibility menu, added to Ren'Py in Ren'Py 7.2.2. This can also be displayed by pressing "A" on the keyboard when playing on a PC. As this option can break the way the game is displayed and also does not support translation as of Ren'Py build 7.3.2, you may want to hide the option. The button should also be removed if your version of Ren'Py is under 7.2.2, as the menu does not exist in previous versions.
                textbutton _("More Options..."):
                    style_prefix "button"
                    action Show("_accessibility")

        null height 40

        hbox:
            style_prefix "slider"

            vbox:

                label _("Text Speed")
                bar value Preference("text speed")

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

            vbox:

                if config.has_music:
                    label _("Music Volume")
                    hbox:
                        bar value Preference("music volume")

                if config.has_sound:
                    label _("Sound Volume")
                    hbox:
                        bar value Preference("sound volume")
                        if config.sample_sound:
                            textbutton _("Test") action Play("sound", config.sample_sound)

                if config.has_voice:
                    label _("Voice Volume")
                    hbox:
                        bar value Preference("voice volume")
                        if config.sample_voice:
                            textbutton _("Test") action Play("voice", config.sample_voice)

                if config.has_music or config.has_sound or config.has_voice:
                    null height 20
                    textbutton _("Mute All"):
                        style_prefix "check"
                        xpos 20
                        action Preference("all mute", "toggle")

### PREF
style pref_frame:
    xpos 520
    yalign 0.5
    padding (40, 20, 0, 40)

style pref_label:
    top_margin 15
    bottom_margin 5

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 400

## RADIO
style radio_label:
    is pref_label

style radio_label_text:
    is pref_label_text

style radio_vbox:
    is pref_vbox
    spacing 12

style radio_button:
    foreground "gui/button/radio_[prefix_]foreground.png"
    padding (35, -12, 0, 0)

## CHECK
style check_label:
    is pref_label
style check_label_text:
    is pref_label_text

style check_vbox:
    is pref_vbox
    spacing 12

style check_button:
    foreground "gui/button/check_[prefix_]foreground.png"
    padding (35, -12, 0, 0)

## SLIDER
style slider_label:
    is pref_label
style slider_label_text:
    is pref_label_text

style slider_slider:
    xsize 525
    xoffset 20

style slider_button:
    yalign 0.5
    left_padding 20

style slider_vbox:
    xsize 600