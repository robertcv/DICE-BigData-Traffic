import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM


class PlotOnMap():
    """
    This class enables plotting geographic points onto a map.
    """

    def __init__(self, lng, lat, title):
        """
        Initialize PlotOnMap class.

        Args:
            lng (list of float): List of longitudes.
            lat (list of float): List of latitudes.
            title (str): Plot title.

        """
        self.lng = lng
        self.lat = lat
        self.title = title
        self.plt = plt

    def generate(self, figsize, dpi, zoom, markersize):
        """
        This generates the basic map and draws dots on the given location.

        Args:
            figsize (tuple of int): Figure size.
            dpi (int): Dots per inch.
            zoom (int): Map zoom.
            markersize (int): Size of dots.

        """
        imagery = OSM()
        self.plt.figure(figsize=figsize, dpi=dpi)
        ax = self.plt.axes(projection=imagery.crs)
        ax.set_extent((min(self.lng) - 0.02, max(self.lng) + 0.02,
                       min(self.lat) - 0.01, max(self.lat) + 0.01))
        ax.add_image(imagery, zoom)
        self.plt.plot(self.lng, self.lat, 'bo', transform=ccrs.Geodetic(),
                      markersize=markersize)
        self.plt.title(self.title)

    def label(self, labels, offset, fontsize):
        """
        This draws labels above the dots.

        Args:
            labels (list of str): List of labels.
            offset (tuple of float): Offset of labels from dots.
            fontsize (int): Size of labels.

        """
        for i in range(len(labels)):
            plt.text(self.lng[i] + offset[0], self.lat[i] + offset[1],
                     labels[i], horizontalalignment='left',
                     fontsize=fontsize, transform=ccrs.Geodetic())

    def save(self, dir, file_name):
        """
        This saves plot into a file.

        Args:
            dir (str): Absolute location of directory in which to save plot.
            file_name (str): Name of saved file.

        """
        plt.savefig(dir + file_name)
