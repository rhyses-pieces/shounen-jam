## Hit Points screen ###########################################################
##
## A screen that shows HP bars

init python:

    class Actor(object):
        """Class that implements HP for players and enemies"""
        def __init__(self, name, max_hp):
            super(Actor, self).__init__()
            self.name = name
            self.hp = max_hp
            self.max_hp = max_hp
        
        def attack(self, power, target):
            amount = determine_damage(power)
            target.hp -= amount
            if target.hp < 0:
                target.hp = 0
            return target.hp

    def shuffle_combat(l):
        renpy.random.shuffle(l)
        return l

    def determine_damage(power):
        if power == "critical":
            return renpy.random.randint(35, 50)
        elif power == "moderate":
            return renpy.random.randint(15, 20)
        elif power == "minor":
            return renpy.random.randint(5, 10)
        else:
            pass
    
    # rudimentary ai
    def enemy_ai(player_power):
        if player_power == "critical":
            return "minor"
        elif player_power == "moderate":
            return "moderate"
        elif player_power == "minor":
            return "critical"
        else:
            pass

default timeout = 5.0
default timeout_label = None
default player_power = "none"
default enemy_power = "none"

screen hit_points(actor, xalign, to_flip=False):

    zorder 100

    style_prefix "battle"

    frame:
        xalign xalign
        
        vbox:
            spacing 5

            hbox:
                if to_flip is True:
                    text "[actor.name]" style "battle_name"
                    xalign 1.0
                else:
                    text "[actor.name]" style "battle_name"
            
            hbox:
                if to_flip is True:
                    bar value AnimatedValue(actor.hp, actor.max_hp, delay=1.0) at flip
                else:
                    bar value AnimatedValue(actor.hp, actor.max_hp, delay=1.0)

transform flip:
    xzoom -1.0

style battle_frame:
    background None

style battle_name:
    font gui.name_text_font
    textalign 0.5
    size 60
    min_width 220

style battle_bar:
    xmaximum 532
    ymaximum 48
    bar_invert True
    left_bar Frame('gui/bar/left.png', 20, 4)
    right_bar Frame('gui/bar/right2.png', 20, 4)


## Battle UI screen ###########################################################
##
## A screen that shows both player and enemy bars

screen battle_ui(player, enemy):
    use hit_points(player, 0.0)
    use hit_points(enemy, 1.0, True)

screen battle_choice(items):
    style_prefix "choice"
    default shuffle_items = shuffle_combat(items)

    vbox:
        if renpy.in_fixed_rollback():
            textbutton "Continue..." action Return(renpy.roll_forward_info())
        else:
            for i in shuffle_items:
                textbutton i.caption action [SetVariable("player_power", i.kwargs.get("power", "minor")), i.action]

    if (timeout_label is not None) and persistent.timed_choices and not renpy.in_fixed_rollback():
        bar value AnimatedValue(old_value = 1.0, value = 0.0, range = 1.0, delay = timeout)
        
        timer timeout action Jump(timeout_label)

style choice_bar:
    xalign 0.5
    ypos 640
    xysize (680, 48)
    left_bar Frame("gui/bar/right.png", 20, 4, tile=4)
    right_bar Frame("gui/bar/left.png", 20, 4)


label battle_loop(player, enemy):
    
    $ player.attack(player_power, enemy)
    $ enemy_power = enemy_ai(player_power)
    $ enemy.attack(enemy_power, player)
    
    $ renpy.block_rollback()

    if player.hp == 0:
        "You died..."
        $ renpy.full_restart()
        return
    elif enemy.hp == 0:
        "You won!"
        return