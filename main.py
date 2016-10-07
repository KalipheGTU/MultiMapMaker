Import qgis.core

# Choose layer

# Copy Style

# Choose composer

# Choose columns

# 1) GENERATE

# Create layer group

# Duplicate layer using style

# 2) EXPORT

# Switch on / off layers > different visibilities

# Export image
mapRenderer = iface.mapCanvas().mapRenderer()
c = QgsComposition(mapRenderer)
c.setPlotStyle(QgsComposition.Print)




def return_toc(self):

    # Revert layers back to pre-script state (on/off)
    legend = self.iface.legendInterface()
    for wanted in turn_on:
        legend.setLayerVisible(wanted, True)
    for unwanted in turn_off:
        legend.setLayerVisible(unwanted, False)