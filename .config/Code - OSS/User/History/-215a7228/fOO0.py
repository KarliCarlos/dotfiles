# Color Theme
#                  vvvvvvvvvvvvvvvv  change this to change theme
from themes import cornershop as theme

# General

mod = "mod4"
terminal = "alacritty" # guess if None
browser = "firefox" # guess if None
file_manager = None # guess if None
launcher = "rofi -show drun"
powermenu = "rofi -show menu -modi 'menu:~/.config/rofi/rofi-power-menu --choices=shutdown/reboot' -config ~/.config/rofi/power.rasi"
screenshots_path = "~/screenshots/" # creates if doesn't exists
layouts_saved_file = "~/.config/qtile/layouts_saved.json" # creates if doesn't exists
autostart_file = "~/.config/qtile/autostart.sh"
wallpapers_path = "~/wallpapers/" # creates if doesn't exists

floating_apps = [
    'nitrogen',
]

# Uncomment the first line for qwerty, the second for azerty
num_keys = "123456789"
#num_keys = "ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "minus", "egrave", "underscore", "ccedilla", "agrave"


# Groups

groups_count = 4
groups_names = list(map(str, range(1, groups_count + 1))) # Groups names **IN THE PROGRAM**, you probably don't need to change it
groups_labels = ['●' for _ in range(groups_count)] # How the groups are named in the top bar
# Alternatives :
# groups_labels = [str(i) for i in range(1, groups_count + 1)]
# groups_labels = ['what', 'ever', 'you', 'want']


# Layouts

# Uncomment to enable layout
layouts = [
    # "Columns",
    # "Bsp",
    # "RatioTile",
    "MonadTall",
    # "MonadWide",
    "Max",
    # "Floating",
    # "VerticalTile",
    # "Stack",
    # "Matrix",
    # "Tile",
    # "TreeTab",
    # "Zoomy",
]

layouts_margin = 7
layouts_border_width = 5
layouts_border_color = theme['dark2']
layouts_border_focus_color = theme['highlightd']
layouts_border_on_single = True
layouts_restore = True



# Top bar

bar_top_margin = 7
bar_bottom_margin = 7
bar_left_margin = 7
bar_right_margin = 7
bar_size = 37
bar_background_color = theme['dark']
bar_foreground_color = theme['text']
bar_background_opacity = 1.0
bar_global_opacity = 1.0
bar_font = "Mononoki Nerd Font"
bar_nerd_font = "Mononoki Nerd Font"
bar_fontsize = 14


# Widgets

widget_gap = 17
widget_left_offset = 5
widget_right_offset = 1
widget_padding = 10


