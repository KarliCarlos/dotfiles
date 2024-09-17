#   _____       _  _   
#  |     | ___ |_|| |_ 
#  |-   -||   || ||  _|
#  |_____||_|_||_||_|  

import sys
from os.path import expanduser, exists, normpath, getctime
from subprocess import run
from os import system, listdir, makedirs
from datetime import datetime
from libqtile import layout, qtile, hook, bar, core, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from qtile_extras.layout.decorations import ConditionalBorder, GradientBorder, GradientFrame, RoundedCorners
from json import dump, load

sys.path.append(expanduser('~/.config/qtile'))

from variables import *

screenshots_path = expanduser(screenshots_path)
layouts_saved_file = expanduser(layouts_saved_file)
autostart_file = expanduser(autostart_file)
wallpapers_path = expanduser(wallpapers_path)

if not exists(path := layouts_saved_file):
    with open(path, 'w') as file:
        file.write('{}')

if not exists(screenshots_path):
    makedirs(screenshots_path)

if not exists(wallpapers_path):
    makedirs(wallpapers_path)


#   _____  _____  _____  _____  _____  _____ 
#  |   __|| __  ||     ||  |  ||  _  ||   __|
#  |  |  ||    -||  |  ||  |  ||   __||__   |
#  |_____||__|__||_____||_____||__|   |_____|

groups = [Group(name) for name in groups_names]


#   __     _____  __ __  _____  _____  _____  _____                                             
#  |  |   |  _  ||  |  ||     ||  |  ||_   _||   __|                                            
#  |  |__ |     ||_   _||  |  ||  |  |  | |  |__   |                                            
#  |_____||__|__|  |_|  |_____||_____|  |_|  |_____|  

layout_theme = {
    "border_width": layouts_border_width,
    "margin": layouts_margin,
    "border_focus": layouts_border_focus_color,
    "border_normal": layouts_border_color,
    "border_on_single": layouts_border_on_single
}

layouts_tweaks = {
    "Columns": {
        "grow_amount": 5,
        "fair": False,
        "num_columns": 2,
    },
    "MonadTall": {
        "ratio": 0.57,
        "min_ratio": 0.5,
        "max_ratio": 0.7,
        "change_size": 20,
        "change_ratio": 0.01,
    },
    "MonadWide": {
        "ratio": 0.55,
        "min_ratio": 0.45,
        "max_ratio": 0.7,
        "change_size": 35,
        "change_ratio": 0.02,
    },
    "Bsp": {
        "fair": False,
    },
}

layouts = [getattr(layout, i)(**(layout_theme|layouts_tweaks.get(i, {}))) for i in layouts]


#   _____  _____  _____  _____  _____  _____  _____  _____  _____ 
#  |   __||  |  ||     || __  ||_   _||     ||  |  ||_   _||   __|
#  |__   ||     ||  |  ||    -|  | |  |   --||  |  |  | |  |__   |
#  |_____||__|__||_____||__|__|  |_|  |_____||_____|  |_|  |_____|

@lazy.function
def screenshot(_qtile, mode=0):
    file_path = datetime.now().strftime(f"{screenshots_path}%d-%m-%Y-%H-%M-%S.jpg")
    system(f"scrot {'-s' if mode == 1 else ''} {file_path}")
    system(f"xclip -selection clipboard -t image/png -i {file_path}")


keys = [

    # Window Management

    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "j", lazy.layout.grow(), desc="Grow window"),
    Key([mod], "h", lazy.layout.shrink(), desc="Shrink window"),
    Key([mod], "r", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.next_layout(), desc="Toggle fullscreen",),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle full-fullscreen",),
    
    Key([mod], "x", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),

    # Media
    
    Key([], "XF86AudioRaiseVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], "XF86AudioLowerVolume", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], "XF86AudioMute", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    Key([], "XF86AudioPlay", lazy.spawn('playerctl play-pause')),
    Key([], "XF86AudioPrev", lazy.spawn('playerctl previous')),
    Key([], "XF86AudioNext", lazy.spawn('playerctl next')),

    # Launch

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Space", lazy.spawn(launcher), desc="Launch launcher"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager"),
    Key([mod, "control"], "Space", lazy.spawn(powermenu), desc="Launch powermenu"),
    
    # Qtile
    
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Screenshot

    Key([mod, "shift"], "s", screenshot(mode=1), desc="Take a screenshot of a zone or a window"),
        
    # Groups
    *[Key([mod], num_keys[index], lazy.group[group.name].toscreen(), desc=f"Switch to the {group.name} group") for index, group in enumerate(groups)],
    *[Key([mod, "shift"], num_keys[index], lazy.window.togroup(group.name, switch_group=False), desc=f"Move focused window to the {group.name} group") for index, group in enumerate(groups)],
]


#   _____  _____  _____  _____  _____  _____  _____                                             
#  |   __||     || __  ||   __||   __||   | ||   __|                                            
#  |__   ||   --||    -||   __||   __|| | | ||__   |                                            
#  |_____||_____||__|__||_____||_____||_|___||_____|

powerlineL = {     
		"decorations": [  PowerLineDecoration(path="forward_slash")     ] 
		}
powerlineR = {     
		"decorations": [  PowerLineDecoration(path="back_slash")     ] 
		}

class WidgetTweaker:
    def __init__(self, func):
        self.format = func

@WidgetTweaker
def groupBox(output):
    index = groups_names.index(output)
    label = groups_labels[index]

    return label

widget_defaults = dict(
    font="Mononoki Nerd Font",
    foreground=bar_foreground_color,
    fontsize=bar_fontsize,
    padding=widget_padding
)

extension_defaults = widget_defaults.copy()

left = [
    widget.GroupBox(
        font=f"{bar_font} Bold",
        disable_drag=True,
        borderwidth=0,
        fontsize=15,
        inactive=theme['dark'],
        active=bar_foreground_color,
        block_highlight_text_color=theme['bright'],
        padding=7,
        fmt=groupBox,
        **powerlineR,
        background = theme['dark2']
    ),
]

right = [
    widget.CPU(
        format="{load_percent}%",
        fmt="  {}",
    ),
        
    widget.Memory(
        measure_mem="G",
        format=" {MemUsed: .2f}{mm} /{MemTotal: .2f}{mm}",
        padding=25
    ),

    widget.DF(
        visible_on_warn = False,
        format = '󰋊 {f} {m}B'
    ),

    widget.Clock(
        format="%A %d %B %Y %H:%M",
    ),

    widget.TextBox(
        '⏻',
        mouse_callbacks={
            'Button1': lazy.spawn(powermenu)
        },
    ),
]

screens = [
    Screen(
        top=bar.Bar(
            widgets=[widget.Spacer(length=widget_left_offset, decorations=[])] + left + [widget.WindowName(foreground="#00000000", fmt="", decorations=[])] + right + [widget.Spacer(length=widget_right_offset, decorations=[])],
            size=bar_size,
            background = bar_background_color + format(int(bar_background_opacity * 255), "02x"),
            margin = [bar_top_margin, bar_right_margin, bar_bottom_margin-layouts_margin, bar_left_margin],
            opacity = bar_global_opacity
        )
    ),
    Screen(
        top=bar.Bar(
            widgets=[widget.Spacer(length=widget_left_offset, decorations=[])] + left + [widget.WindowName(foreground="#00000000", fmt="", decorations=[])] + right + [widget.Spacer(length=widget_right_offset, decorations=[])],
            size=bar_size,
            background = bar_background_color + format(int(bar_background_opacity * 255), "02x"),
            margin = [bar_top_margin, bar_right_margin, bar_bottom_margin-layouts_margin, bar_left_margin],
            opacity = bar_global_opacity
        )
    ),
]



#   _____  _____  _____  _____  _____                                                           
#  |     ||     ||  |  ||   __||   __|                                                          
#  | | | ||  |  ||  |  ||__   ||   __|                                                          
#  |_|_|_||_____||_____||_____||_____|

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


#   _____  _____  _____  _____  _____    _____  _____  _____  _____  _____  _____  _____  _____ 
#  |     ||_   _||  |  ||   __|| __  |  |   __||   __||_   _||_   _||     ||   | ||   __||   __|
#  |  |  |  | |  |     ||   __||    -|  |__   ||   __|  | |    | |  |-   -|| | | ||  |  ||__   |
#  |_____|  |_|  |__|__||_____||__|__|  |_____||_____|  |_|    |_|  |_____||_|___||_____||_____|

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry,
        *[Match(wm_class=app) for app in floating_apps]
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False
wmname = "Qtile"


#   _____  _____  _____  _____  _____                                                           
#  |  |  ||     ||     ||  |  ||   __|                                                          
#  |     ||  |  ||  |  ||    -||__   |                                                          
#  |__|__||_____||_____||__|__||_____| 

ready = False

@hook.subscribe.startup_once
def _():
    run(autostart_file)

@hook.subscribe.layout_change
def _(layout, group):
    global ready

    if ready:
        with open(layouts_saved_file, 'r') as file:
            layouts_saved = load(file)

        layouts_saved[group.name] = layout.name

        with open(layouts_saved_file, 'w') as file:
            dump(layouts_saved, file)

@hook.subscribe.startup
def _():
    global ready

    if layouts_restore:
        with open(layouts_saved_file, 'r') as file:
            layouts_saved = load(file)

        for group in groups:
            if layouts_saved.get(group.name):
                qtile.groups_map.get(group.name).layout = layouts_saved[group.name]
    
    ready = True
