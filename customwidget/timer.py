import subprocess

from libqtile.widget import base
import subprocess
import re

class CustomTimer(base._TextBox):
    defaults = [
        ('duration', '-1s', 'Timer duration'),
        (
            'duration_cmd', 
            "printf '' | rofi -dmenu -p 'Duration' 2> /dev/null", 
            'Command that runs when timeout.'
        ),
        ('timeout_cmd', 'notify-send "Timeout!"', 'Command that runs when timeout.'),
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, 'Timer', **config)
        self.add_defaults(CustomTimer.defaults)
        self.remain_time = self._convert_to_seconds(self.duration)
        self.update_interval = 1
        self.add_callbacks(
            {
                'Button1': self._get_duration,
                'Button3': self._stop_timer,
            }
        )

    def _configure(self, qtile, parent_bar):
        base._TextBox._configure(self, qtile, parent_bar)

    def timer_setup(self):
        self.timeout_add(self.update_interval, self.update)

    def _stop_timer(self):
        self.remain_time = -1
        self.text = 'Timer'
        self.bar.draw()

    def _convert_to_seconds(self, duration):
        seconds = 0
        time_arr = re.split('(?<=\\d)(?=[hms])|(?=\\d)(?<=[hms])', duration)
        for i in range(len(time_arr)-1, -1, -1):
            if time_arr[i] == 's':
                seconds += int(time_arr[i-1])
            elif time_arr[i] == 'm':
                seconds += int(time_arr[i-1]) * 60
            elif time_arr[i] == 'h':
                seconds += int(time_arr[i-1]) * 3600
        return seconds

    def _get_duration(self):
        duration = subprocess.check_output(self.duration_cmd, shell=True).decode('utf-8').rstrip('\n')
        self.remain_time = self._convert_to_seconds(duration)
        self.timer_setup()

    def update(self):
        if self.remain_time < 0:
            self.text = 'Timer'
            self.bar.draw()
        else:
            self.text = 'Timer: ' + str(self.remain_time)
            if self.remain_time == 0 and self.timeout_cmd is not None:
                subprocess.call(self.timeout_cmd, shell=True)
            self.bar.draw()
            self.remain_time -= 1
            self.timer_setup()
