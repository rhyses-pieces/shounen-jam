## This file modifies transforms and transitions.
## This file adds / changes various transforms (image transformations) and transitions (image transitions).

## This file must be run before any of those files so that it can be used for guis and image definitions.
init offset = -3

##############################################################################
## Animations
## The following transforms animate the image.
## If you want to specify the position at the same time as the animation, specify it in the order of show image at animation, position.
## Example: show girl at inR, move_center
 
## Defines the magnitude of animation movement as an integer.
## A guideline is about 1/20 of the size of the standing picture of the whole body.
define move_time = 0.5
define move_size = 32

transform move_center:
    ease move_time xalign 0.5

transform move_left:
    ease move_time xalign 0.0

transform move_right:
    ease move_time xalign 1.0

## Animation that appears from the left.
transform inL(t=move_time/2, d=move_size):
    alpha .0 xoffset -d yoffset 21
    easein t alpha 1.0 xoffset 0

## Animation that appears from the right.
transform inR(t=move_time/2, d=move_size):
    alpha .0 xoffset d yoffset 21
    easein t alpha 1.0 xoffset 0

## Animation that disappears to the left.
## hide uses the show image at transform because the at clause cannot be used.
transform outL(t=move_time/2, d=move_size):
    easeout t alpha .0 xoffset -d
    xoffset 0

## Animation that disappears to the right.
transform outR(t=move_time/2, d=move_size):
    easeout t alpha .0 xoffset d
    xoffset 0

## Lightly hop animation.
transform hop(t=move_time/2, d=move_size):
    alpha 1.0
    ease t/2 yoffset -d
    ease t/2 yoffset 0

## Animation that hops twice in a row.
transform doublehop(t=move_time, d=move_size):
    alpha 1.0
    ease t/4 yoffset -d
    ease t/4 yoffset 0
    ease t/4 yoffset -d
    ease t/4 yoffset 0

## Animation that bends lightly.
transform bow(t=move_time, d=move_size):
    alpha 1.0
    ease t/2 yoffset d
    ease t/2 yoffset 21

## Animation that sways from side to side twice.
transform wag(t=move_time, d=move_size):
    alpha 1.0
    easein t/6 xoffset d/2
    ease t/3 xoffset -d/2
    easein t/3 xoffset d/4
    easein t/6 xoffset 0

## Animation to avoid quickly to the left.
transform swayL(t=move_time/2, d=move_size):
    alpha 1.0
    ease t/3 xoffset -d*4
    ease t*2/3 xoffset 0

## Animation to avoid quickly to the right.
transform swayR(t=move_time/2, d=move_size):
    alpha 1.0
    ease t/3 xoffset d*4
    ease t*2/3 xoffset 0


## An animation that vibrates like a shock.
## First, define a function to calculate the shaking in python.
init python:

    def _shake_function(trans, st, at, dt=.5, dist=64):
        #dt is duration timebase, dist is maximum shake distance in pixel
        if st <= dt:
            trans.xoffset = int((dt-st)*dist*(.5-renpy.random.random())*2)
            trans.yoffset = int((dt-st)*dist*(.5-renpy.random.random())*2)
            return 1.0/60
        else:
            return None

###Actual vibration animation.
transform shake(t=move_time, d=move_size):
    alpha 1.0
    function renpy.curry(_shake_function)(dt=t, dist=d*2)
    xoffset 0 yoffset 0


##############################################################################
# Transitions
##############################################################################

## https://www.renpy.org/doc/html/transitions.html

## transition is a function that displays the transition between two screens.
## The basic usage is in the form of show image with transform, but instead of with
## $ renpy.transition (transition, layer = "master") is used before the show image,
## There is no waiting time until the end of the effect, and you can specify the layer.
 
 
## Basic transition.
## The ones defined by default are commented out, so
## Please uncomment only if you want to change it.

define flash = Fade(.15, 0, .3, color="#fff")
define fade = Fade(.5, 0, .5)
define dissolve = Dissolve(0.5)
#define pixellate = Pixellate(1.0, 5)

#define vpunch = Move((0, 10), (0, -10), .10, bounce=True, repeat=True, delay=.275)
#define hpunch = Move((15, 0), (-15, 0), .10, bounce=True, repeat=True, delay=.275)

#define blinds = ImageDissolve(im.Tile("blindstile.png"), 1.0, 8)
#define squares = ImageDissolve(im.Tile("squarestile.png"), 1.0, 256)


## The following redefines CropMove, which is defined by default, with ImageDissolve.
## The two images to be wiped will be mixed in the dissolve.
## To use ImageDissolve, you need an image that transitions from white to black.

#define wipedown = ImageDissolve("transitions/wipedown.png", .5, ramplen=32)
#define wipeup = ImageDissolve("transitions/wipedown.png", .5,  ramplen=32, reverse=True)
#define wiperight = ImageDissolve("transitions/wiperight.png", .5, ramplen=32)
#define wipeleft = ImageDissolve("transitions/wiperight.png", .5,  ramplen=32, reverse=True)

#define irisout = ImageDissolve("transitions/irisout.png", .5,  ramplen=32)
#define irisin = ImageDissolve("transitions/irisout.png", .5,  ramplen=32,reverse=True)