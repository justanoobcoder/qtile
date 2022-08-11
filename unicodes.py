from libqtile import widget

def left_half_circle(fg_color, bg_color):
    return widget.TextBox(
            text='',
            font = 'JetBrainsMono Nerd Font',
            fontsize = 20,
            foreground = fg_color,
            background = bg_color,
            padding = 0
        )


def right_half_circle(fg_color, bg_color):
    return widget.TextBox(
            text = '',
            font = 'JetBrainsMono Nerd Font',
            fontsize = 20,
            foreground = fg_color,
            background = bg_color,
            padding = 0
        )
