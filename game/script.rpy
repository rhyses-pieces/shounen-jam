# define variables

label start:
    $ renpy.change_language(_preferences.language, force=True)

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

    e "I want to start writing a long dialogue, one that will span at least three lines in order to test your resolve. We will need some kind of result. How many characters can fit inside here? We should be going to {b}hello{/b} there we are trying our best to see the length of the end"

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
            jump test_mettle

    # This ends the game.

    return

label next_time:
    
    e "It doesn't matter what you choose, in the end."

    e "Farewell!"

    return

label test_mettle:
    $ timeout_label = "mettle_failed"
    $ player = Actor(protag.name, 100)
    $ enemy = Actor(rival.name, 100)

    show screen battle_ui(player, enemy)

    menu mettle_menu (screen="battle_choice"):
        "What say you?!"

        "Attack with grace" (power="critical"):
            "You dodge to the side, easily bypassing the attack!"
            jump mettle_succeed
        "Meet head on!" (power="moderate"):
            "You struggle to meet the attack!"
            jump mettle_moderate
        "Fumble" (power="minor"):
            "Oh no!"
            jump mettle_minor
        "Freeze":
            hide screen battle_ui
            "You freeze up, too spooked to move!"
            jump mettle_failed

label mettle_succeed:
    hide screen battle_ui

    narrator "You succeed! well done, friend. Will there be a lot of text?"
    jump next_time

    return

label mettle_moderate:
    narrator "Both opponents attempt to throw the other, to no success!"
    call battle_loop(player, enemy)

    jump mettle_menu

label mettle_minor:
    narrator "You stumble, and the opponent gets the best of you!"
    call battle_loop(player, enemy)

    jump mettle_menu

label mettle_failed:

    narrator "Oh no! You failed...."
    jump end

    return

label end:
    $ timeout_label = None
    "Game over...."

    return