"""PCPPPriceDropTracker object call translater.

Translater calls between a list of objects.

"""

from .dataStructures import ActiveObjectList


__all__ = ["Translater"]

class Translater():
    """Call translater handler"""
    def __init__(self, objects, active = 0):
        """Setup.

        objects - List of objects to translate between | list
        active - Active object index | integer

        """
        self._active = [active]
        self.objects = ActiveObjectList(objects, self._active)
        self.translate = TranslaterCore(self.objects, self._active)

    @property
    def active(self):
        """Get active index."""
        return self._active[0]

    def set_active(self, n):
        """Set active index.

        n - index | integer

        """
        if n < 0 or n >= len(self.objects):
            raise IndexError("Out of objects list range.")
        self._active[0] = n


class TranslaterCore():
    """Call Translater."""
    def __init__(self, objects, active):
        """Setup.

        objects - List of objects to translate between | list
        active - List with index 0 been the active index | list

        """
        self._active = active
        self._objects = objects

    def __getattr__(self, attr):
        return getattr(self._objects[self._active[0]], attr)


if __name__ == '__main__':
    from tools import main
    main(__doc__)
