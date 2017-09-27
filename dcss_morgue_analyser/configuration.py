

class Configuration:
    _morgue_path = ""

    @property
    def morgue_path(self):
        return self._morgue_path or _(u"<unnamed>")


    @morgue_path.setter
    def morgue_path(self, value):
        if not value:
            return
        self._morgue_path = value
