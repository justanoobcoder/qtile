import subprocess

from libqtile import bar, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.layout.tile import Tile
from libqtile.layout.max import Max
from libqtile.layout.floating import Floating

from bar import bar

mod = 'mod1'
windowskey = 'mod4'
APP_LAUNCHER = subprocess.getoutput('echo $XDG_CONFIG_HOME') + '/rofi/launcher/launcher.sh'
TERMINAL = subprocess.getoutput('echo $TERMINAL')
BROWSER = subprocess.getoutput('echo $BROWSER')

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    Key([mod], 'h',                     lazy.layout.left(), desc='Move focus to left'),
    Key([mod], 'l',                     lazy.layout.right(), desc='Move focus to right'),
    Key([mod], 'j',                     lazy.layout.down(), desc='Move focus down'),
    Key([mod], 'k',                     lazy.layout.up(), desc='Move focus up'),
    Key([mod], 'space',                 lazy.layout.next(), desc='Move window focus to other window'),
    Key([mod, 'shift'], 'h',            lazy.layout.shuffle_left(), desc='Move window to the left'),
    Key([mod, 'shift'], 'l',            lazy.layout.shuffle_right(), desc='Move window to the right'),
    Key([mod, 'shift'], 'j',            lazy.layout.shuffle_down(), desc='Move window down'),
    Key([mod, 'shift'], 'k',            lazy.layout.shuffle_up(), desc='Move window up'),
    Key([mod, 'control'], 'h',          lazy.layout.grow_left(), desc='Grow window to the left'),
    Key([mod, 'control'], 'l',          lazy.layout.grow_right(), desc='Grow window to the right'),
    Key([mod, 'control'], 'j',          lazy.layout.grow_down(), desc='Grow window down'),
    Key([mod, 'control'], 'k',          lazy.layout.grow_up(), desc='Grow window up'),
    Key([mod], 'n',                     lazy.layout.normalize(), desc='Reset all window sizes'),
    Key([mod, 'shift'], 'Return',       lazy.layout.toggle_split(), desc='Toggle between split and unsplit sides of stack'),
    Key([mod, 'shift'], 'q',            lazy.spawn('dsysact'), desc='Spawn dsysact'),
    Key([mod], 'Return',                lazy.spawn(TERMINAL), desc='Launch terminal'),
    Key([mod], 'Tab',                   lazy.screen.toggle_group(), desc='Toggle between groups'),
    Key([mod], 'q',                     lazy.window.kill(), desc='Kill focused window'),
    Key([mod, 'shift'], 'r',            lazy.reload_config(), desc='Reload the config'),
    Key([mod, 'control'], 'q',          lazy.shutdown(), desc='Shutdown Qtile'),
    Key([mod], 'r',                     lazy.spawncmd(), desc='Spawn a command using a prompt widget'),
    Key([mod], 'w',                     lazy.spawn(BROWSER), desc='Launch browser'),
    Key([mod], 'd',                     lazy.spawn(APP_LAUNCHER), desc='Spawn application launcher'),
    Key([], 'XF86AudioMute',            lazy.spawn('changeVolume toggle'), desc='Toggle volume'),
    Key([], 'XF86AudioRaiseVolume',     lazy.spawn('changeVolume 2%+'), desc='Raise up volume'),
    Key([], 'XF86AudioLowerVolume',     lazy.spawn('changeVolume 2%-'), desc='Low down volume'),
    Key([], 'XF86MonBrightnessUp',      lazy.spawn('light -A 10'), desc='Increase screen brightness'),
    Key([], 'XF86MonBrightnessDown',    lazy.spawn('light -U 10'), desc='Decrease screen brightness'),
    Key([], 'Print',                    lazy.spawn('dscrot --full'), desc='Screenshot fullscreen and save it'),
    Key(['shift'], 'Print',             lazy.spawn('dscrot'), desc='Run screenshot script'),
]

groups = [
    Group('1', label="一"),
    Group('2', label="二"),
    Group('3', label="三"),
    Group('4', label="四"),
    Group('5', label="五"),
    Group('6', label="六"),
    Group('7', label="七"),
    Group('8', label="八"),
    Group('9', label="九"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc='Switch to group {}'.format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, 'shift'],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc='Switch to & move focused window to group {}'.format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, 'shift'], i.name, lazy.window.togroup(i.name),
            #     desc='move focused window to group {}'.format(i.name)),
        ]
    )

@hook.subscribe.client_new
def grouper(window):
    try:
        print('NEW WINDOW! Class: ' + str(window.window.get_wm_class()))
        if(window.window.get_wm_class()[1] == 'Microsoft-edge'):
            window.togroup(groups[1].name)
    except:
        pass # TODO: handle errors. LibreOffice makes qtile crash here

layouts = [
    Tile(
        border_normal = '#293132',
        border_focus =  '#50D8D7',
        border_width = 2,
        border_on_single = False,
        add_after_last = True,
        margin = 2,
        margin_on_single = 0,
        master_match = [Match(wm_class=["Microsoft-edge"])],
        ratio = 0.5,
        shift_windows = False,
    ),
    Max(),
]

widget_defaults = dict(
    font='JetBrainsMono Nerd Font',
    fontsize=15,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(top = bar),
]

# Drag floating layouts.
mouse = [
    Drag([mod], 'Button1', lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        Match(wm_class='nm-connection-editor'),  # ssh-askpass
    ]
)
auto_fullscreen = True
focus_on_window_activation = 'smart'
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'qtile'
