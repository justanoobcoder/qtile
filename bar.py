import subprocess
from libqtile import bar, qtile, widget

from unicodes import right_half_circle, left_half_circle
from customwidget import battery, clock, volume, timer

fg_dark =       '#191724'
fg_light =      '#e0def4'
gb_active =     '#ffffff'
gb_inactive =   '#665c54'
gb_hl_text =    '#eb6f92'
gb_bg =         '#2e3410'
bg0 =           '#232136'
bg1 =           '#ddffd9'
bg2 =           '#ecc8ae'
bg3 =           '#d7907b'
bg4 =           '#BBDEF0'
bg5 =           '#24A777'
bg6 =           '#F4D35E'
bg7 =           '#50C9CE'

bar = bar.Bar([
    widget.GroupBox(
        disable_drag = True,
        active = gb_active,
        inactive = gb_inactive,
        highlight_method = 'line',
        block_highlight_text_color = gb_hl_text,
        borderwidth = 0,
        highlight_color = gb_bg,
        background = gb_bg
    ),
    right_half_circle(gb_bg, bg0),
    widget.Spacer(background = bg0),

    left_half_circle(bg7, bg0),
    timer.CustomTimer(
        duration_cmd = 'printf | rofi -dmenu -p "Duration:" 2> /dev/null',
        timeout_cmd = 'notify-send "Timeout!"',
        background = bg7,
        foreground = fg_dark
    ),

    left_half_circle(bg1, bg7),
    widget.CPU(
        format = ' {freq_current}GHz {load_percent}%',
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('st -e htop')},
        update_interval = 2,
        background = bg1,
        foreground = fg_dark
    ),

    left_half_circle(bg2, bg1),
    widget.GenPollText(
        func = lambda: subprocess.getoutput('printf \" $(free -m | awk \'/Mem/ { printf \"%.2fGiB\", ($3 + $5)/1024}\')\"'),
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('st -e htop')},
        update_interval = 2,
        background = bg2,
        foreground = fg_dark,
    ),

    left_half_circle(bg3, bg2),
    volume.CustomVolume(
        update_interval = 0.5,
        icon = True,
        background = bg3,
        foreground = fg_dark
    ),

    left_half_circle(bg4, bg3),
    battery.BatteryIcon(
        scale = 1,
        update_interval = 5,
        background = bg4,
        foreground = fg_light
    ),
    battery.Battery(
        format = '{percent:2.0%}',
        notify_below = 20,
        show_short_text = False,
        update_interval = 5,
        background = bg4,
        foreground = fg_dark
    ),

    left_half_circle(bg5, bg4),
    clock.CustomMouseOverClock(
        format = ' %H:%M',
        long_format = ' %H:%M:%S %a,%d/%m/%Y',
        background = bg5,
        foreground = fg_dark,
    ),

    left_half_circle(bg6, bg5),
    widget.Systray(
        background = bg6
    ),

    widget.Spacer(length = 10, background = bg6)
], background = bg0, size = 26, margin = 9)
