## This file defines Actor and Arena class to add turn-based combat.
## Adds actor and arena classes for turn-based combat and competition.
## The Actor class inherits from Inventory and treats Items like skills.
## You will need Inventory.rpy.

##############################################################################
## How to Use
##############################################################################


## First, create a list of the types of items you want to manage.
define skill_types = ["active"]

## Then define each item with Item(name, type, value, score, max_score, cost, order, prereqs, info, target, effect, damage).
## Must be defined in the namespace of the namespace you give the actor.

define skill.attack = Item("Attack", type="active", target="foe", effect="attack", damage=5)
define skill.heal = Item("Heal", type="active", score=2, max_score=2, cost=1, target="friend", effect="heal", damage=20)

## Next define the skill's manager as Actor(name, currency, item_types, namespace, tradein, infinite, recharge, removable, items, ability value).
## hp is your stats. You can add it by rewriting the Actor class.

default knight = Actor("Knight", item_types = skill_types, namespace = "skill", removable=False, items="attack", hp=30)
default bishop = Actor("Bishop", item_types = skill_types, namespace = "skill", removable=False, items="attack, heal", hp=20)
default pawn = Actor("Pawn A", item_types = skill_types, namespace = "skill", removable=False, items="attack", hp=10)

## Copy an actor with the same ability with a different name with actor.copy(name).
default pawn2 = pawn.copy("Pawn B")
default pawn3 = pawn.copy("Pawn C")

## Finally we define the arena to store data about the battle.
default arena = Arena()

## That's it, you're ready to go.


## Jump here when the game starts with jump sample_combat.

label sample_combat:

    ## Adds combat companion and combat opponent actors to the arena as a list.

    $ arena.player_actors = [knight, bishop]
    $ arena.enemy_actors = [pawn, pawn2, pawn3]

    ## Combat begins here.
    call _combat(arena)

    ## When the battle is over, you can know the result with _return.
    if _return == "win":
        "You win"

    elif _return == "lose":
        "You lose"

    else:
        "Draw"

    return


##############################################################################
## Definition
##############################################################################

##############################################################################
## Combat label

label _combat(arena):

    # initialize
    python:
        arena.init()
        arena.reset_actors()
        _rollback = False

    show screen combat_ui(arena)

    while arena.state not in ["win", "lose", "draw"]:

        python:

            # set current actor to perform
            arena.actor = arena.get_turn()

            # player
            if arena.actor in arena.player_actors:
                arena.actor.skill = renpy.call_screen("choose_skill", arena)
                arena.actor.target = renpy.call_screen("choose_target", arena)

            # enemy
            else:
                arena.actor.skill = arena.get_random_item()
                arena.actor.target = arena.get_target()

            # perform skill
            arena.perform_skill()

            # update arena's state
            arena.end_turn()

    hide screen combat_ui

    python:
        _return = arena.state
        _rollback = True
        renpy.block_rollback()

    return _return


##############################################################################
## combat screens

screen combat_ui(arena):

    zorder -1

    # show player status
    vbox:
        for i in arena.player_actors:
            hbox:
                text "[i.name]: HP [i.hp]"

    # show enemy status
    vbox xalign 1.0:
        for i in arena.enemy_actors:
            hbox:
                text "[i.name]: HP [i.hp]"


screen choose_skill(arena):

    tag menu
    modal True

    $ actor = arena.actor

    # caption
    label "[actor.name]'s turn" align .5, .2

    # commands
    vbox align .5, .5:
        for name, score, obj in actor.get_items(types=["active"]):
            $ score_text = " ({}/{})".format(score, obj.max_score) if obj.cost else ""
            textbutton "[obj.name][score_text]":

                # sensitive if skill is available
                if actor.can_use_item(name):
                    action Return(name)


screen choose_target(arena):

    tag menu
    modal True

    $ actor = arena.actor

    # caption
    label "Choose target" align .5, .2

    # commands
    vbox align .5, .5:
        for i in arena.foes(actor) if actor.get_item(actor.skill).target == "foe" else arena.friends(actor):
            textbutton i.name:

                # sensitive if target is available
                if arena.check_target(actor, i):
                    action Return(i)


##############################################################################
## Arena class

init -5 python:

    class Arena(object):

        """
        This class represents acting field for actors. It has the following fields:

        player_actors - list of playable actors

        enemy_actors - list of unplayable actors

        actor - current actor to perform

        order - performing order of actors

        state - current state of arena. "win", "lose", "draw" ends combat, otherwise keep performing.
        """

        def __init__(self, player_actors=None, enemy_actors=None):

            self.player_actors = player_actors or []
            self.enemy_actors = enemy_actors or []

            self.order = []
            self.actor = None
            self.state = None


        def friends(self, actor=None):
            # returns friendly actors

            actor = actor or self.actor
            return self.player_actors if actor in self.player_actors else self.enemy_actors


        def foes(self, actor=None):
            # returns hostile actors

            actor = actor or self.actor
            return self.player_actors if actor in self.enemy_actors else self.enemy_actors


        def init(self):
            # call this to set order

            self.state = None
            self.order = self.player_actors + self.enemy_actors
            renpy.random.shuffle(self.order)


        def reset_actors(self):
            # reset actor's attributes

            for i in self.player_actors + self.enemy_actors:
                i.reset_attributes()


        def get_turn(self):
            # returns a next actor to perform

            while True:
                actor = self.order.pop(0)
                self.order.append(actor)
                if actor.hp > 0:
                    return actor


        def get_random_item(self, actor=None):
            # returns a random skill name

            actor = actor or self.actor
            names = [x for x in actor.get_items(score=1, types=["active"], rv="name") if actor.can_use_item(x)]
            return  renpy.random.choice(names)


        def check_target(self, actor=None, target=None):
            # returns True if target is available

            actor = actor or self.actor
            target = target or actor.target
            if target.hp>0:
                return True


        def get_target(self, actor=None):
            # returns a random target

            actor = actor or self.actor
            targets = self.foes(actor) if actor.get_item(actor.skill).target == "foe" else self.friends(actor)
            targets = [x for x in targets if self.check_target(actor, x)]
            return renpy.random.choice(targets)


        def perform_skill(self, actor=None, target=None, name=None):
            # perform skill on the target

            actor = actor or self.actor
            target = target or actor.target
            name = name or actor.skill
            obj = actor.get_item(name)

            actor.use_item(name)

            if obj.effect == "attack":
                target.change_attributes(hp = -obj.damage)
                narrator ("{}'s attack. {} loses {} HP".format(actor.name, target.name, obj.damage))

            elif obj.effect == "heal":
                target.change_attributes(hp = +obj.damage)
                narrator ("{}'s heal. {} gains {} HP".format(actor.name, target.name, obj.damage))



        def end_turn(self):
            # call this each turn to update arena's state

            for i in self.player_actors:
                if i.hp > 0:
                    break
            else:
                self.state = "lose"

            for i in self.enemy_actors:
                if i.hp > 0:
                    break
            else:
                self.state = "win"


##############################################################################
## Actor class.

    from collections import OrderedDict

    class Actor(Inventory):

        """
        Class that performs skills. It has following fields:

        name - name of this actor

        attributes - float or int variables that are added into an actor when an object is created.
        
        default_attributes - default values of attributes. if it's positive number, it means maximum point.

        and properties inherited from Inventory class
        """

        # Default attributes that are added when attributes are not defined.
        # This will create self.hp and self.default_hp.
        _attributes = ["hp"]


        def __init__(self, name="", currency = 0, item_types=None, namespace=None, tradein = 1.0, infinite = False, recharge=False, removable = True, items=None, **kwargs):


            super(Actor, self).__init__(currency, item_types, namespace, tradein, infinite, recharge, removable, items)

            self.name = name
            self.skill = None
            self.target = None

            # creates attributes as field value
            for i in self._attributes:
                if i in kwargs.keys():
                    setattr(self, "default_"+i, kwargs[i])
                    setattr(self, i, kwargs[i])
                else:
                    setattr(self, "default_"+i, None)
                    setattr(self, i, None)

            self.reset_attributes()


        def copy(self, name=None):
            # Returns copy of actor, changing its name.

            from copy import deepcopy

            actor = deepcopy(self)
            if name:
                actor.name = name

            return actor


        def reset_attributes(self):
            # reset attributes

            for i in self._attributes:
                setattr(self, i, getattr(self, "default_"+i))

            self.skill = None
            self.target = None
            self.charge_all_items()


        def change_attributes(self, **kwargs):
            # Change attributes.
            # instead of changing attributes directly, use this method.

            for k, v in kwargs.items():
                if k in self._attributes:
                    nv = getattr(self, k) + v
                    mv = getattr(self, "default_"+k)
                    setattr(self, k, max(0, min(nv, mv)))
                else:
                    raise Exception("{} is not defined attributes".format(k))

