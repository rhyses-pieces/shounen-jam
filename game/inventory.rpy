## This file provides inventory system.
## This is a file that adds functions to buy, sell and manage items.
## It can be used universally to manage various elements such as skills and quests.

#################################################### 
## How to Use
#################################################### 

## First, create a list of the types of items you want to manage.
define item_types = ["supply", "food", "outfit"]

## Then define each item with Item(name, type, value, score, max_score, cost, order, prereqs, info).
## name is the displayed name, type is the category and value is the price.
## score is the default number of items when adding, if omitted it will be 1.
## max_score is the maximum number of items you can have, if omitted or set to zero it will be infinite.
## cost If you set the cost, the number of items will be reduced by the cost when using the item.
## order is used when you want to determine the default sort order.
## prereqs are the items consumed when purchasing the item.
## info is the information displayed when the mouse is focused.
## must be defined in the namespace of the namespace you give to inventory.

define item.apple = Item("Apple", type="food", value=10, info="apple")
define item.orange = Item("Orange", type="food", value=20, info="orange")
define item.knife = Item("Knife", type="supply", value=50, info="knife")
define item.dress = Item("Dress", type="outfit", value=100, info="dress")
define item.juice = Item("Juice", type="food", value=30, prereqs="orange:1, apple:2", info="It requires two oranges and one apple")

## Finally define the custodian of the item with Inventory(currency, item_types, namespace, tradein, infinite, recharge, removable, items).
## currency is money you have.
## item_types is the list of item types defined above, used for categorization on the item screen.
## Items of types that do not fit the category are also available, but will not be displayed on the screen.
## namespace If you set a namespace, you can separate the items handled by the administrator by namespace.
## tradein is the price ratio at which the owner trades in.
## infinite to True, you will have infinite money.
## recharge is True, inventory will always be replenished.
## removable is False, the item will not be removed from the item list when the inventory is zero.
## items setting this has the same effect as add_items described below.

default housewife = Inventory(currency=1000, item_types = item_types, namespace = "item")
default merchant = Inventory(item_types = item_types, namespace = "item", tradein=.25, infinite=True, recharge=True, removable=False)


## When the game starts, jump here with jump sample_inventory.

label sample_inventory:

    ## add_item(item, score).Use the argument score to specify the number.
    ## item is a string without item.
    $ housewife.add_item("apple", score=2)

    ## add_all_items(types, charge=True) will automatically add all items defined in the namespace with matching types.
    ## charge is True, add up to max_score.
    $ merchant.add_all_items()

    ## There are other methods below.
    ## has_item(item) - Returns True if you have it.
    ## count_item(item) - Returns the total number of items you have.
    ## charge_item(item, score) - Charge the item you have to the maximum number.If you give a score, it will charge for the score.
    ## charge_all_items(types, score) - Charges the items in the types you have up to the maximum number or score.
    ## add_items(items, score) - Give multiple item names like "a,b,c" to add all of them.
    ## remove_item(item) - Removes the item if you have it.
    ## remove_items(items) - Given multiple item names like "a,b,c", removes those items if you have them.
    ## score_item(item, score) - Change the number of items, get if 1 or more, delete if less than 0.
    ## score_items(item, score) - If you give multiple item names like "a,b,c", you can change/gain/delete multiple numbers.
    ## give_item(item, getter, score) - Give the item to the getter.
    ## can_buy_item(item, score) - Checks if an item is available for purchase.
    ## buy_item(item, score) - If you have enough money and the requested item, spend it to add the item.
    ## sell_item(item, buyer, score) - Sell the item to the buyer and receive your money.
    ## can_use_item(item, target, cost="cost") - Check if item is available.Cost="currency" consumes currency.
    ## use_item(item, target, cost="cost") - Use item as target.Define the effect for each item.

    ## The following methods are for internal use.
    ## get_item(name) - Get Item object by string name.
    ## get_items(types, score) - Returns a list of items in types with score or higher as a tuple of (name, score, obj).
    ## sort_items(order="order") - Sort the items.


    while True:

        ## The next instruction blocks the rollback and allows you to save all game changes.
        ## (Needed because by default it only saves the start of the current input wait.)
        $block()

        menu:

            ## Show list of items with "call screen inventory(inv, buyer, title)".

            "show inventory":
                ## Use inventory when you want to see and organize items.
                ## If you click on an item in this state, it will enter slot replacement mode.
                $block()
                call screen inventory (housewife)

            "buy items":
                ## When you want to buy an item, use inventory(seller's owner, buyer's owner).
                $block()
                call screen inventory(merchant, buyer=housewife, title="Buy")

            "sell items":
                ## When you want to sell items, you also use inventory (seller's owner, buyer's owner).
                ## The trading partner is just reversed, but the screen title is changed.
                $block()
                call screen inventory(housewife, buyer=merchant, title="Sell")

            "return":
                $ renpy.full_restart()


#################################################### 
## Definitions
#################################################### 

init python:

    def block():
        # blocks rollback then allows saving data in the current interaction

        config.skipping = None
        renpy.checkpoint()
        renpy.block_rollback()
        renpy.retain_after_load()


####################################################
## Inventory Screen

## screen that shows inventory
## inv is an inventory object that has items on the screen
## if buyer is given, it's trade mode.
## otherwise, it's stock mode that can reorder item slots

screen inventory(inv, buyer=None, title="Inventory"):

    # screen variables
    default tab = "all"

    if title=="Buy":
        default confirm_message = "Are you sure to buy it?"
    else:
        default confirm_message = "Are you sure to sell it?"

    default notify_message = "You don't have money or required items"

    # frame size
    python:
        width = config.screen_width*3//4
        height = config.screen_height//2

    # unselect items on show
    on "show" action SetField(inv, "selected", None)

    vbox:
        # screen title
        label title text_size gui.title_text_size

        # currency.when seller (inv) is an infinite inventory, show buyer's currency
        $ currency = inv.currency if not inv.infinite else buyer.currency
        text "Currency:[currency:>5]" xalign.5

        null height 60

        # sort buttons
        text "Sort by"
        for i in ["name", "type", "value", "amount", "order"]:
            textbutton i.capitalize():
                action Function(inv.sort_items, order=i)

    vbox align .5,.6:

        # category tabs
        hbox style_prefix "radio":

            for i in ["all"] + inv.item_types:
                textbutton i.capitalize():
                    action SetScreenVariable("tab", i)

        # item slots
        frame xysize width, height:

            vpgrid style_prefix "item":
                cols 2 mousewheel True draggable True scrollbars "vertical"

                for name, score, obj in inv.get_items(types=[tab] if tab != "all" else inv.item_types):

                    $ price = int(obj.value*(buyer.tradein if buyer else inv.tradein))

                    textbutton "[obj.name] x[score] ([price])":
                        selected inv.selected == name
                        tooltip obj.info

                        # Sell/buy mode
                        if buyer:
                            if buyer.can_buy_item(name):
                                action Confirm(confirm_message, Function(inv.sell_item, name=name, buyer=buyer))
                            else:
                                action Notify(notify_message)

                        #Arrange mode
                        else:

                            # reorder after selected
                            if inv.selected:
                                action [Function(inv.replace_items, first=name, second=inv.selected),
                                        SetField(inv, "selected", None)]

                            # reorder before selecting
                            else:
                                action SetField(inv, "selected", name)

                            # This action uses items.
                            # action Function(inv.use_item, name=name, target=?)

        null height 10

        # information window
        frame xysize width, height//3:
            $tooltip = GetTooltip() or ""
            text [tooltip]

    textbutton "Return" action Return() yalign 1.0

    key "game_menu" action [SetField(inv, "selected", None) if inv.selected else Return()]


style item_button:
    xsize 250


#################################################### 
## Inventory class.

init -10 python:

    from collections import OrderedDict

    class Inventory(object):

        """
        Class that stores items.

        currency - score of money this object has.

        item_types - list of item types that are grouped up as tabs in the inventory screen.
        
        namespace - if given, items defined in this name space are used
        
        tradein - when someone buyoff items to this inventory, value is reduced by this value
        
        infinite - if True, currency is infinite.
        
        recharge - if True, an item score is charged at max_score (or 1) when its score is changed
        
        removable - if False, an item is not removed when score reached at 0.
        
        items - ordered dictionary of {"item name": score}.
            if items property given at the init time, they are added by add_items method,
        
        selected - selected slot in a current screen.
        """


        def __init__(self, currency = 0, item_types= None, namespace=None, tradein = 1.0, infinite = False, recharge=False, removable = True, items=None):

            self.currency = int(currency)
            self.item_types = item_types or []
            self.namespace = getattr(store, namespace) if namespace else store
            self.tradein = float(tradein)
            self.infinite = infinite
            self.recharge = recharge
            self.removable = removable
            self.items = OrderedDict()
            if items:
                self.add_items(items)
            self.selected = None


        def get_item(self, name):
            # returns item object from name

            if isinstance(name, Item):
                return name

            elif isinstance(name, basestring):
                obj = getattr(self.namespace, name, None)
                if obj:
                    return obj

            raise Exception("Item '{}' is not defined".format(name))


        def get_items(self, types = None, score=None, rv=None):
            # returns list of (name, score, object) tuple in conditions
            # if rv is "name" or "obj", it returns them.

            items = [k for k, v in self.items.items() if score==None or v >= score]

            types = types or self.item_types
            items = [i for i in items if self.get_item(i).type in types]

            if rv == "name":
                return items

            elif rv == "obj":
                return [self.get_item(i) for i in items]

            return [(i, self.items[i], self.get_item(i)) for i in items]


        def has_item(self, name, score=None):
            # returns True if inventory has this item whose score is higher than given.

            # check valid name or not
            self.get_item(name)

            return name in [k for k, v in self.items.items() if score==None or v >= score]


        def has_items(self, name, score=None):
            # returns True if inventory has these items whose score is higher than give.
            # "a, b, c" means a and b and c, "a | b | c" means a or b or c.

            separator = "|" if name.count("|") else ","
            names = name.split(separator)
            for i in names:
                i = i.strip()
                if separator == "|" and self.has_item(i, score):
                    return True
                elif separator == "," and not self.has_item(i, score):
                    return False

            return True if separator == "," else False


        def count_item(self, name):
            # returns score of this item

            if self.has_item(name):
                return self.items[name]


        def charge_item(self, name, score=None):
            # changes score of name to its maximum value

            if self.has_item(name):
                if score:
                    self.items[name] += score
                else:
                    self.items[name] = max(self.get_item(name).max_score, 1)


        def charge_all_items(self, types=None):
            # charges all items in self.items.

            types = types or self.item_types

            for i in self.items.keys():
                if self.get_item(i).type in types:
                    self.charge_item(i)


        def add_item(self, name, score = None):
            # add an item
            # if score is given, this score is used instead of item's default value.

            score = score or self.get_item(name).score
            max_score = self.get_item(name).max_score

            if self.has_item(name):
                self.items[name] += score
            else:
                self.items[name] = score

            if max_score > 0:
                self.items[name] = min(self.items[name], max_score)

            if self.recharge:
                self.charge_item(name)


        def add_items(self, items, score=None):
            # add items

            for i in items.split(","):
                i = i.strip()
                score = score or self.get_item(i).score
                self.add_item(i, score=score)


        def add_all_items(self, types=None, charge=True, sort="order"):
            # get all Item objects defined under namespace

            types = types or self.item_types

            for i in dir(self.namespace):
                if isinstance(getattr(self.namespace, i), Item):
                    if self.get_item(i).type in types:
                        self.add_item(i)
                        if charge:
                            self.charge_item(i)

            self.sort_items(order=sort)


        def remove_item(self, name):
            # remove an item

            if self.has_item(name):
                del self.items[name]


        def remove_items(self, items):
            # remove items

            for i in items.split(","):
                i = i.strip()
                self.remove_item(i)


        def score_item(self, name, score):
            # changes score of name

            self.add_item(name, score)
            if self.removable and self.items[name] <= 0:
                self.remove_item(name)


        def score_items(self, name, score):
            # changes score of name

            for i in items.split(","):
                self.add_item(name, score)
                if self.removable and self.items[name] <= 0:
                    self.remove_item(name)


        def give_item(self, name, getter, score=None):
            # remove an item slot then add this name to getter

            score = score or self.get_item(name).score

            if self.has_item(name, score):

                getter.score_item(name, score)
                self.score_item(name, -score)


        def can_buy_item(self, name, score = None, prereqs=True):
            # returns True if this item can be bought

            score = score or self.get_item(name).score
            value = self.get_item(name).value*score
            prereqs = self.get_item(name).prereqs

            if self.infinite:
                return True

            if self.currency < value:
                return False

            if prereqs:
                for k,v in prereqs.items():
                    if not self.has_item(k, score=v*score):
                        return False

            return True


        def buy_item(self, name, score = None, prereqs=True):
            # buy an item
            # if prereqs is True, it requires items listed in prereqs

            if not self.can_buy_item(name, score, prereqs):
                return False

            score = score or self.get_item(name).score
            value = self.get_item(name).value*score
            prereqs = self.get_item(name).prereqs

            self.add_item(name, score)
            if not self.infinite:
                self.currency -= value

            if prereqs:
                for k,v in prereqs.items():
                    self.score_item(k, score=-v*score)


        def sell_item(self, name, buyer, score = None, prereqs=True):
            # remove an item then add this item to buyer for money

            if self.has_item(name):

                score = score or self.get_item(name).score
                value = self.get_item(name).value*score

                buyer.buy_item(name, score, prereqs)

                if buyer.infinite or buyer.currency >= value:
                    self.score_item(name, score=-score)
                    if not self.infinite:
                        self.currency += int(value*buyer.tradein)


        def replace_items(self, first, second):
            # swap order of two slots

            keys = list(self.items.keys())
            values = list(self.items.values())
            i1 = keys.index(first)
            i2 = keys.index(second)
            keys[i1], keys[i2] = keys[i2], keys[i1]
            values[i1], values[i2] = values[i2], values[i1]

            self.items = OrderedDict(zip(keys, values))


        def sort_items(self, order="order"):
            # sort slots

            items = self.items.items()

            if order == "name":
                items.sort(key = lambda i: self.get_item(i[0]).name)
            elif order == "type":
                items.sort(key = lambda i: self.item_types.index(self.get_item(i[0]).type))
            elif order == "value":
                items.sort(key = lambda i: self.get_item(i[0]).value, reverse=True)
            elif order == "amount":
                items.sort(key = lambda i: i[1], reverse=True)
            elif order == "order":
                items.sort(key = lambda i: self.get_item(i[0]).order)

            self.items = OrderedDict(items)


        def can_use_item(self, name, target=None, cost="cost"):
            # returns True if inv can use this item

            obj = self.get_item(name)

            if cost=="cost" and self.count_item(name) >= obj.cost:
                return True
            elif cost=="value" and (self.currency >= obj.value or self.infinite):
                return True
            return False


        def use_item(self, name, target=None, cost="cost"):
            # uses item on target

            if not self.can_use_item(name, target, cost):
                return False

            obj = self.get_item(name)

            if cost=="cost" and obj.cost:
                self.score_item(name, -obj.cost)

            elif cost=="value" and obj.value and not self.infinite:
                self.currency -= value


            ## write script here



#################################################### 
## Item class.

    class Item(object):

        """
        Class that represents item that is stored by inventory object.

        name - item name that is shown on the screen

        type - item category

        value - price that is used for trading

        score - default amount of item when it's added into inventory

        max_score - maximum score.Score higher than this is ignored.

        cost - if not zero, using this item reduces score.

        order - if integer is given, item can be sorted by this number.

        prereqs - required items to buy.This should be given in strings like "itemA:1, itemB:2"

        info - description that is shown when an item is focused
        """


        def __init__(self, name="", type="", value=0, score=1, max_score = 0, cost=0, order=0, prereqs=None, info="", **kwargs):

            self.name = name
            self.type = type
            self.value = int(value)
            self.score = int(score)
            self.max_score = int(max_score)
            self.cost = int(cost)
            self.order = int(order)

            self.prereqs = {}
            if prereqs:
                for i in [x.split(":") for x in prereqs.split(",")]:
                    self.prereqs.setdefault(i[0].strip(), int(i[1]))
            self.info = info

            for i in kwargs.keys():
                setattr(self, i, kwargs[i])
