# import dependencies

# Choose layer
layer = iface.activeLayer()
# Copy Style
mapRenderer = iface.mapCanvas().mapRenderer()
c = QgsComposition(mapRenderer)
c.setPlotStyle(QgsComposition.Print)

layer.rendererV2().symbols()
symbol_layer.properties()
# Choose composer

# Choose columns

# 1) GENERATE

# Create layer group

# Duplicate layer using style
renderer = layer.rendererV2()
layer2.setRenderer(renderer)


# 2) EXPORT

# Switch on / off layers > different visibilities

# Export image
# dpi = c.printResolution()
# dpmm = dpi / 25.4
# width = int(dpmm * c.paperWidth())
# height = int(dpmm * c.paperHeight())
#
# # create output image and initialize it
# image = QImage(QSize(width, height), QImage.Format_ARGB32)
# image.setDotsPerMeterX(dpmm * 1000)
# image.setDotsPerMeterY(dpmm * 1000)
# image.fill(0)
#
# # render the composition
# imagePainter = QPainter(image)
# sourceArea = QRectF(0, 0, c.paperWidth(), c.paperHeight())
# targetArea = QRectF(0, 0, width, height)
# c.render(imagePainter, targetArea, sourceArea)
# imagePainter.end()
#
# image.save("out.png", "png")


def return_toc(self):

    # Revert layers back to pre-script state (on/off)
    legend = self.iface.legendInterface()
    for wanted in turn_on:
        legend.setLayerVisible(wanted, True)
    for unwanted in turn_off:
        legend.setLayerVisible(unwanted, False)