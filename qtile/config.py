#  ██████╗ ████████╗██╗██╗      ███████╗
# ██╔═══██╗╚══██╔══╝██║██║      ██╔════╝
# ██║   ██║   ██║   ██║██║      █████╗
# ██║▄▄ ██║   ██║   ██║██║      ██╔══╝
# ╚██████╔╝   ██║   ██║███████╗███████╗
#  ╚══▀▀═╝    ╚═╝   ╚═╝╚══════╝╚══════╝
#-----------------------------------------

import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy

# --- 1. Autostart ---
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    if os.path.exists(home):
        subprocess.Popen([home])

# --- 2. Logika Baterai Pintar v2 ---
def get_battery_total():
    try:
        is_charging = False
        for path in ["AC", "ACAD", "ADP1"]:
            ac_path = f"/sys/class/power_supply/{path}/online"
            if os.path.exists(ac_path):
                with open(ac_path, "r") as f:
                    if f.read().strip() == "1":
                        is_charging = True
                        break
        
        with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
            b0 = int(f.read().strip())
        with open("/sys/class/power_supply/BAT1/capacity", "r") as f:
            b1 = int(f.read().strip())
        avg = int((b0 + b1) / 2)
        
        if is_charging:
            icon = "󱐋"
        else:
            if avg >= 95: icon = "󰁹"
            elif avg >= 75: icon = "󰂂"
            elif avg >= 50: icon = "󰁿"
            elif avg >= 25: icon = "󰁽"
            else: icon = "󰂎"
            
        return f"{icon} {avg}%"
    except:
        return "󰂎 N/A"

# --- 3. Warna Stealth ---
c_abu_1 = "#4f4f4f"
c_abu_2 = "#3a3a3a"
c_abu_3 = "#303030"
c_abu_4 = "#2a2a2a"
c_abu_5 = "#242424"
c_abu_6 = "#1d1d1d"
c_abu_7 = "#1a1a1a"

# --- 4. Layout ---
layouts = [
    layout.Columns(border_focus=c_abu_1, border_normal=c_abu_7, border_width=2, margin=4, gap=4),
    layout.Max(),
]
floating_layout = layout.Floating(border_focus=c_abu_1, border_normal=c_abu_7, border_width=2)

# --- 5. Keybindings ---
mod = "mod4"
groups = [Group(i) for i in "12345"]
keys = [
    *[Key([mod], i.name, lazy.group[i.name].toscreen()) for i in groups],
    *[Key([mod, "shift"], i.name, lazy.window.togroup(i.name)) for i in groups],
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 5%+")),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q sset Master toggle")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 5%+")),
    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "d", lazy.spawn("dmenu_run -l 10 -nb '#1a1a1a' -nf '#ffffff' -sb '#3a3a3a' -sf '#ffffff'")),
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod], "space", lazy.window.toggle_floating()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.reload_config()),
    Key([mod, "shift"], "q", lazy.shutdown()),
]

# --- 6. Bar & Screen ---
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(text='', foreground="#ffffff", background=c_abu_4, padding=10),
                widget.TextBox(text='', padding=0, fontsize=25, foreground=c_abu_4, background=c_abu_5),
                widget.GroupBox(
                    background=c_abu_5,
                    active="#ffffff",
                    inactive="#666666",
                    highlight_method="line",
                    this_current_screen_border="#ffffff",
                    highlight_color=[c_abu_5, c_abu_5],
                    padding=10
                ),
                widget.TextBox(text='', padding=0, fontsize=25, foreground=c_abu_5, background=c_abu_7),
                widget.WindowName(foreground="#aaaaaa", background=c_abu_7, padding=10),
                widget.Spacer(background=c_abu_7),
                widget.TextBox(text='', padding=0, fontsize=25, foreground=c_abu_5, background=c_abu_7),
                widget.CPU(format='  {load_percent}% ', background=c_abu_5, padding=10),
                widget.TextBox(text='', padding=0, fontsize=25, foreground=c_abu_4, background=c_abu_5),
                widget.Wlan(interface='wlp3s0', format='  {essid} ', background=c_abu_4, padding=10),
                widget.TextBox(text='', padding=0, fontsize=25, foreground=c_abu_3, background=c_abu_4),
                widget.GenPollText(func=get_battery_total, update_interval=5, background=c_abu_3, padding=10),
                widget.TextBox(text='', padding=0, fontsize=25, foreground=c_abu_2, background=c_abu_3),
                widget.Clock(format="󰃭  %Y-%m-%d ", background=c_abu_2, padding=5),
                widget.TextBox(text='', padding=0, fontsize=25, foreground=c_abu_1, background=c_abu_2),
                widget.Clock(format="󰅐  %H:%M ", background=c_abu_1, padding=5),
                widget.Systray(background=c_abu_1),
            ],
            22, background=c_abu_7,
        ),
    ),
]
