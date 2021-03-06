
class NestId(object):
    """
    """

    def __init__(self, id_int):
        """
        id_int(int) value from 'id' column generated by database
        """
        self.id_int = id_int
        return

    def get_value(self):
        """
        returns as int
        """
        return self.id_int

    def to_slug(self):
        """
        a string value suitable for filenames, urls, etc
        has the form "NEST-<id>"
        """
        s = "NEST-" + str(self.id_int)
        return s

    def to_jdata(self):
        return self.id_int

    def __str__(self):
        #s = 'nest_id::' + str(self.get_value())
        s = self.to_slug()
        return s

    def __eq__(self, other):
        b = True
        if other is None:
            b = False
        else:
            b = (self.id_int == other.id_int)
        return b

