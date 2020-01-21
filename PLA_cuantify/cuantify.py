import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets  import RectangleSelector
from PIL import Image

class Event():
    def __init__(self, image):
        self.image = image
        self.xo = None
        self.yo = None
        self.xf = None
        self.yf = None

    def on_press(self, event):
        self.xo, self.yo = event.xdata, event.ydata
    
    def on_release(self, event):
        self.xf, self.yf = event.xdata, event.ydata
        self._count_pixels()

    def _count_pixels(self):
        n_pixels_x, n_pixels_y =  self.image.size
        npixels = 0
        npixels_red = 0
        for x in range(n_pixels_x):
            for y in range(n_pixels_y):
                if x > self.xo and x < self.xf and y > self.yo and y < self.yf:
                    r, g, b = self.image.getpixel((x, y))
                    if r > g and r > b and r > 40:
                        npixels_red += 1
                        npixels += 1
                    else:
                        npixels += 1
        print("{} % of red in selected square".format(npixels_red/npixels*100))


def line_select_callback(eclick, erelease):
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

def toggle_selector(event):
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        toggle_selector.RS.set_active(False)

def main(img):
    im = Image.open(img)
    rgb_im = im.convert('RGB')
    plot = Event(rgb_im)
    img = mpimg.imread(img)

    fig, current_ax = plt.subplots()
    plt.imshow(img)
    # Plot Callbacks
    cidpress = fig.canvas.mpl_connect('button_press_event', plot.on_press)
    cidrealese= fig.canvas.mpl_connect('button_release_event', plot.on_release)
    toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                             drawtype='box', useblit=True,
                             button=[1, 3],  # don't use middle button
                             minspanx=5, minspany=5,
                             spancoords='pixels',
                             interactive=False)
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description='Calculate % of red in selected square')
    parser.add_argument('image', type=str, help='path to jpg')
    args = parser.parse_args()
    return args.image


if __name__ == "__main__":
    img = parse_args()
    main(img)

