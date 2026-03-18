#!/bin/sh
dunst &
feh --bg-fill ~/Pictures/wallpapers/wall1.png &
export XDG_CURRENT_DESKTOP=Qtile
export XDG_SESSION_TYPE=Qtile
nm-applet --indicator &
