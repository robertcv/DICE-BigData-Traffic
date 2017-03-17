import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.img_tiles import OSM


class PlotOnMap():
    def __init__(self, lng, lat, title):
        self.lng = lng
        self.lat = lat
        self.title = title
        self.plt = plt

    def generate(self, figsize, dpi, zoom, markersize):
        imagery = OSM()
        self.plt.figure(figsize=figsize, dpi=dpi)
        ax = self.plt.axes(projection=imagery.crs)
        ax.set_extent((min(self.lng) - 0.02, max(self.lng) + 0.02, min(self.lat) - 0.01, max(self.lat) + 0.01))
        ax.add_image(imagery, zoom)
        self.plt.plot(self.lng, self.lat, 'bo', transform=ccrs.Geodetic(), markersize=markersize)
        self.plt.title(self.title)

    def label(self, labels, offset, fontsize):
        for i in range(len(labels)):
            plt.text(self.lng[i] + offset[0], self.lat[i] + offset[1], labels[i], horizontalalignment='left',
                     fontsize=fontsize, transform=ccrs.Geodetic())

    def save(self, dir, file_name):
        plt.savefig(dir + file_name)
