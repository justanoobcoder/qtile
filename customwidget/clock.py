from libqtile import widget

class CustomMouseOverClock(widget.Clock):
    defaults = [
        (
            'long_format',
            '%H:%M:%S %a,%d/%m/%Y',
            'Show datetime in long format when hovered.'
        )
    ]

    def __init__(self, **config):
        widget.Clock.__init__(self, **config)
        self.add_defaults(CustomMouseOverClock.defaults)
        self.short_format = self.format

    def mouse_enter(self, *args, **kwargs):
        self.format = self.long_format
        self.bar.draw()

    def mouse_leave(self, *args, **kwargs):
        self.format = self.short_format
        self.bar.draw()
