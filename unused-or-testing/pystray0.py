import pystray
from PIL import Image, ImageDraw

def create_image():
    # Generate an image and draw a pattern
    width = 48
    height = 48
    color1 = (255, 0, 0)
    color2 = (0, 255, 0)
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image


class Press():
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *a, **kw):
        print(self.kwargs["text"])
        print(*a)
        print(**kw)

icon = pystray.Icon("pystray test", icon = create_image(), title = "pystray test")

def shutdown(*a, **kw):
    print("Stopping")
    print(a)
    print(kw)
    icon.stop()

entries = [pystray.MenuItem("Entry 1", Press(text = "Entry 1 pressed"), default = True),
           pystray.MenuItem("Entry 2", Press(text = "Entry 2 pressed")),
           pystray.MenuItem("Entry 3", Press(text = "Entry 3 pressed")),
           pystray.MenuItem("Entry 4", Press(text = "Entry 4 pressed")),
           pystray.MenuItem("Exit", shutdown)]
menu = pystray.Menu(*entries)
icon.menu = menu


def setup(icon):
    icon.visible = True
    print("Running :)")

icon.run(setup)

print("Ended :(")
