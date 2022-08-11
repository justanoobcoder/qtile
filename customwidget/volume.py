import subprocess
import re

from libqtile.widget import base
from libqtile import bar

re_vol = re.compile(r"\[(\d?\d?\d?)%\]")

class CustomVolume(base._TextBox):
    defaults = [
        ('cardid', None, "Card Id"),
        ('device', 'default', "Device Name"),
        ('channel', 'Master', 'Channel'),
        ('icon', False, 'Use icon to display volume states'),
        ('update_interval', 0.5, 'Update time in seconds.'),
        ("mute_command", None, "Mute command"),
        ("volume_app", None, "App to control volume"),
        ("volume_up_command", None, "Volume up command"),
        ("volume_down_command", None, "Volume down command"),
        ("get_volume_command", None, "Command to get the current volume"),
        (
            "step",
            2,
            "Volume change for up an down commands in percentage."
            "Only used if ``volume_up_command`` and ``volume_down_command`` are not set.",
        ),
    ]

    def __init__(self, **config):
        base._TextBox.__init__(self, '0', width=bar.CALCULATED, **config)
        self.add_defaults(CustomVolume.defaults)
        self.volume = None
        self.add_callbacks(
            {
                "Button1": self.cmd_run_app,
                "Button3": self.cmd_mute,
                "Button4": self.cmd_increase_vol,
                "Button5": self.cmd_decrease_vol,
            }
        )

    def _configure(self, qtile, parent_bar):
        base._TextBox._configure(self, qtile, parent_bar)

    def timer_setup(self):
        self.timeout_add(self.update_interval, self.update)

    def create_amixer_command(self, *args):
        cmd = ["amixer"]

        if self.cardid is not None:
            cmd.extend(["-c", str(self.cardid)])

        if self.device is not None:
            cmd.extend(["-D", str(self.device)])

        cmd.extend([x for x in args])
        return cmd

    def get_volume(self):
        try:
            get_volume_cmd = self.create_amixer_command('sget', self.channel)

            if self.get_volume_command:
                get_volume_cmd = self.get_volume_command

            mixer_out = self.call_process(get_volume_cmd)
        except subprocess.CalledProcessError:
            return -1

        if "[off]" in mixer_out:
            return -1

        volgroups = re_vol.search(mixer_out)
        if volgroups:
            return int(volgroups.groups()[0])
        else:
            return -1

    def isPlugged(self):
        result = False
        cmd = """grep -A4 -ri 'Headphone Playback Switch' /proc/asound/card*/* | grep "Amp-Out vals.*0x00 0x00" -q"""
        out = subprocess.run(cmd, shell=True)
        if (out.returncode == 0):
            result = True
        return result

    def update(self):
        vol = self.get_volume()
        if vol != self.volume:
            self.volume = vol
            self._update_drawer()
            self.bar.draw()
        self.timeout_add(self.update_interval, self.update)

    def _update_drawer(self):
        if self.icon and self.volume != None:
            if self.volume == -1:
                self.text = ' ﱝ '
            elif self.volume == 0:
                self.text = ''
            elif self.volume <= 30:
                self.text = ''
            elif self.volume < 70:
                self.text = '墳'
            elif self.volume >= 70:
                self.text = ''

            if self.isPlugged():
                self.text = ''
                if self.volume == -1:
                    self.text = ' ﳌ '
            if self.volume != -1:
                self.text += " {}%".format(self.volume)
        else:
            if self.volume == -1:
                self.text = "M"
            else:
                self.text = "{}%".format(self.volume)

    def draw(self):
        base._TextBox.draw(self)

    def cmd_increase_vol(self):
        if self.volume_up_command is not None:
            subprocess.call(self.volume_up_command, shell=True)
        else:
            subprocess.call(
                self.create_amixer_command("-q", "sset", self.channel, "{}%+".format(self.step))
            )

    def cmd_decrease_vol(self):
        if self.volume_down_command is not None:
            subprocess.call(self.volume_down_command, shell=True)
        else:
            subprocess.call(
                self.create_amixer_command("-q", "sset", self.channel, "{}%-".format(self.step))
            )

    def cmd_mute(self):
        if self.mute_command is not None:
            subprocess.call(self.mute_command, shell=True)
        else:
            subprocess.call(self.create_amixer_command("-q", "sset", self.channel, "toggle"))

    def cmd_run_app(self):
        if self.volume_app is not None:
            subprocess.Popen(self.volume_app, shell=True)
