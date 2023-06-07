## Hit Points screen ###########################################################
##
## A screen that shows HP bars

define current_hp = 100
default max_hp = 100
define enemy_current_hp = 100
default enemy_max_hp = 100
define boss_current_hp = 150
default boss_max_hp = 150

screen hit_points(name, xalign, to_flip=False, is_boss=False):

    zorder 100

    style_prefix "battle"

    frame:
        xalign xalign
        
        vbox:
            spacing 5

            hbox:
                if to_flip is True:
                    text "[name!t]" style "battle_name"
                    xalign 1.0
                else:
                    text "[name!t]" style "battle_name"
            
            hbox:
                if to_flip is True:
                    if is_boss is True:
                        bar value AnimatedValue(boss_current_hp, boss_max_hp, delay=1.0) at flip
                    else:
                        bar value AnimatedValue(enemy_current_hp, enemy_max_hp, delay=1.0) at flip
                else:
                    bar value AnimatedValue(current_hp, max_hp, delay=1.0)
                

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
    if enemy is antag:
        use hit_points(enemy, 1.0, True, True)
    else:
        use hit_points(enemy, 1.0, True)
