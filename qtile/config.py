import os
import subprocess
from libqtile import bar, layout, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration

# --- 1. Autostart ---
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    if os.path.exists(home):
        subprocess.Popen([home])

# --- 2. Warna & Dekorasi ---
BG_BAR = "#111111"
BG_ISI = "#333333"
BG_IKON = "#222222"
FG_WHITE = "#ffffff"
FG_GRAY = "#555555"
BORDER_ACTIVE = "#aaaaaa" # Abu-abu terang
BORDER_NORMAL = "#222222" # Abu-abu gelap

def box_decor(color, is_group=True):
    return [
        RectDecoration(
            colour=color,
            radius=0,
            filled=True,
            padding_y=5, 
            group=is_group,
        )
    ]

# --- 3. Layout (Gap set ke 5) ---
layouts = [
    layout.Columns(
        border_focus=BORDER_ACTIVE,
        border_normal=BORDER_NORMAL,
        border_width=2,
        margin=5, # Gap sudah jadi 5 sesuai request
        border_on_single=True,
    ),
    layout.Max(),
]

# --- 4. Keybindings ---
mod = "mod4"
groups = [Group(i) for i in "12345"]

keys = [
    # Navigasi & Workspace
    *[Key([mod], i.name, lazy.group[i.name].toscreen()) for i in groups],
    *[Key([mod, "shift"], i.name, lazy.window.togroup(i.name)) for i in groups],
    
    # Fokus Jendela (Vim-like)
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),

    # Resize Jendela (Mod + Shift + h/l)
    Key([mod, "shift"], "h", lazy.layout.grow_left(), lazy.layout.shrink_main()),
    Key([mod, "shift"], "l", lazy.layout.grow_right(), lazy.layout.grow_main()),

    # Apps & System
    Key([mod], "Return", lazy.spawn("kitty")),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.reload_config()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod], "d", lazy.spawn("dmenu_run -l 10 -fn 'JetBrainsMono Nerd Font:size=10' -nb '#111111' -nf '#aaaaaa' -sb '#333333' -sf '#ffffff' -p 'Run:'")),
    Key([], "Print", lazy.spawn("flameshot gui")),

    # Hardware Control
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 5%+")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("sh -c 'brightnessctl s +5% && ~/cli/bright_notify'")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("sh -c 'brightnessctl s 5%- &&~/cli/bright_notify'")),
]

# --- 5. Smart Battery Logic ---
def get_smart_bat():
    try:
        is_chg = False
        for p in ["AC", "ACAD", "ADP1"]:
            path = f"/sys/class/power_supply/{p}/online"
            if os.path.exists(path) and open(path).read().strip() == "1":
                is_chg = True; break
        with open("/sys/class/power_supply/BAT0/capacity", "r") as f: b0 = int(f.read().strip())
        with open("/sys/class/power_supply/BAT1/capacity", "r") as f: b1 = int(f.read().strip())
        avg = int((b0 + b1) / 2)
        if is_chg: icon = "󱐋"
        elif avg >= 80: icon = "󰁹"
        elif avg >= 50: icon = "󰁿"
        else: icon = "󰁻"
        return f"{icon}"
    except: return "󰂎"

# --- 6. Screen & Bar ---
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=12,
                    highlight_method="line",
                    highlight_color=[BG_BAR, BG_BAR], # No shadow
                    this_current_screen_border=FG_WHITE,
                    active=FG_WHITE,
                    inactive=FG_GRAY,
                    borderwidth=3,
                    rounded=False,
                    padding_x=10,
                    disable_drag=True,
                ),
                widget.Spacer(),
                # Module urutan Data < Ikon
                widget.CPU(format='{load_percent}%', decorations=box_decor(BG_ISI), padding=10),
                widget.TextBox(text="", decorations=box_decor(BG_IKON), padding=10),
                widget.Spacer(length=8),
                widget.Volume(decorations=box_decor(BG_ISI), padding=10),
                widget.TextBox(text="󰕾", decorations=box_decor(BG_IKON), padding=10),
                widget.Spacer(length=8),
                widget.Battery(format='{percent:2.0%}', decorations=box_decor(BG_ISI), padding=10),
                widget.GenPollText(func=get_smart_bat, update_interval=2, decorations=box_decor(BG_IKON), padding=10),
                widget.Spacer(length=8),
                widget.Clock(format='%d %b %Y', decorations=box_decor(BG_ISI), padding=10),
                widget.TextBox(text="󰃭", decorations=box_decor(BG_IKON), padding=10),
                widget.Spacer(length=8),
                widget.Clock(format='%H:%M', decorations=box_decor(BG_ISI), padding=10),
                widget.TextBox(text="󱑂", decorations=box_decor(BG_IKON), padding=10),
                widget.Spacer(length=12),
                widget.Systray(padding=10), # Tray alami tanpa kerangkeng
                widget.Spacer(length=4),
            ],
            26,
            background=BG_BAR,
        ),
    ),
]

# --- 7. WM Name Fix ---
wmname = "Qtile"
