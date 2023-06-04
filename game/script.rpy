# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")
define protag = Character("Yuusha", who_color="#ff637f")
define rival = Character("Ruri", who_color="#b070eb")
define buddy = Character("Satoru", who_color="#fcc539")
define antag = Character("Mokusei", who_color="#4cbd56")
define announcer = Character("Hanako", who_color="#fff")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    e "I want to start writing a long dialogue, one that will span at least three lines in order to test your resolve. We will need some kind of result. How many characters can fit inside here?"

    protag "Hi! I'm Yuusha!"
    rival "And I'm Ruri!"
    buddy "I'm Satoru!"
    antag "... My name is Mokusei."
    announcer "I'm your announcer, Hanako!!"

    e "You have a choice to make."

    menu test_choice:
        "Say your prayers"
        "Path one":
            jump next_time
        "Choice 2":
            jump next_time        

    # This ends the game.

    return

label next_time:
    
    e "It doesn't matter what you choose, in the end."

    e "Farewell!"

    return
