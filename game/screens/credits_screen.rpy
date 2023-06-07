################################################################################
## Credits Screen
################################################################################

init -5 python:
    class Credit:
        """Class used for outputting names and roles in Credit screen"""
        def __init__(self, name, role, url):
            self.name = name
            self.role = role
            self.url = url
    
    class CategoryCredits:
        """Categories in Credit screen (ex, Art, programming, etc)"""
        def __init__(self, category, credit_list):
            self.category = category
            self.credit_list = credit_list

define credit_list = [
    Credit(name = "Andy", role = "Art, Game Design, UI", url = ""),
    Credit(name = "Lore", role = "Narrative Design, Writing", url = ""),
    Credit(name = "Rhys", role = "Programmer", url = ""),
]

define assets_credit_list = [
    Credit(name = "arimia", role = "Battle CGs", url = "https://arimia.itch.io/"),
    Credit(name = "Diablo Luna", role = "BGM", url = "https://pudretediablo.itch.io/"),
]

screen credits():
    style_prefix "credits"

    frame at credits_scroll(3):
        background "#00000088"
        xalign 0.5

        vbox:
            text "Credits" style "credits_header"
            
            spacing 20

            for credit in credit_list:
                hbox:
                    vbox:
                        text credit.name style "credits_name"
                        text credit.role style "credits_role"
                        textbutton credit.url action OpenURL(credit.url) style "credits_url_button" text_style "credits_url_text"

            text "Assets" style "credits_header"

            for credit in assets_credit_list:
                hbox:
                    vbox:
                        text credit.name style "credits_name"
                        text credit.role style "credits_role"
                        textbutton credit.url action OpenURL(credit.url) style "credits_url_button" text_style "credits_url_text"

    timer 0.5 action Return()

transform credits_scroll(speed):
    ypos 720
    linear speed ypos -720

style credits_header:
    font gui.name_text_font
    size 60

style category_header:
    font gui.name_text_font
    size 48

style credits_url_button is text_button

style credits_name:
    size 36
    bold True

style credits_role:
    size 24

# inherit style from hyperlink_text
style credits_url_text is hyperlink_text
style credits_url_text:
    size 24