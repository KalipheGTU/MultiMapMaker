
def getLayers(self):
    pass

def getLayerColumns(self):
    pass

def duplicateLayer(self, layer, fields):
    layer.saveNamedStyle('C:\Users\l.versluis\Style.qml')
    ranges = layer.rendererV2().ranges()
    for field in fields:
        new_layer = QgsVectorLayer(layer.source(), layer.name(), layer.providerType())
        new_layer.loadNamedStyle('C:\Users\l.versluis\Style.qml')
        new_layer.setGraduatedSymbolRenderer(new_layer, ranges, field)
        QgsMapLayerRegistry.instance().addMapLayer(new_layer)

def getPluginPath(name, basepath=None):
    if not basepath:
      basepath = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(basepath, name)

def getLayerStyle(self, layer):
    ranges = layer.rendererV2().ranges()
    renderer = layer.rendererV2()
    transparency = layer.layerTransparency()

def setLayerStyle(self, layer, renderer):

    layer.setRendererV2(renderer)

def getRenderer(self, layer):
    return layer.rendererV2()

def setGraduatedSymbolRenderer(self, layer, ranges, field ):
    new_renderer = QgsGraduatedSymbolRendererV2(field, ranges)
    layer.setRendererV2(new_renderer)



def getComposition(self):
    composerId = 0
    composers = iface.activeComposers()
    for item in composers:
        if item.composerWindow().windowTitle() == 'Horizontal':
            break
        composerId += 1

    return composers[composerId].composition()

def savePDF():
    mapRenderer = iface.mapCanvas().mapRenderer()
    c = QgsComposition(mapRenderer)


    c.setPlotStyle(QgsComposition.Print)
    x, y = 0, 0
    w, h = c.paperWidth(), c.paperHeight()
    composerMap = QgsComposerMap(c, x ,y, w, h)
    rect = iface.mapCanvas().currentLayer().extent()
    composerMap.setNewExtent(rect)
    print composerMap.currentMapExtent()
    c.addItem(composerMap)

    legend = QgsComposerLegend(c)
    legend.model().setLayerSet(mapRenderer.layerSet())
    c.addItem(legend)

    outpath = “\\\\ba-fs-nc\\data\\Broker Support\\Cat Modeling\\QGIS\\NBIC_2.pdf”
    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(outpath)
    printer.setPaperSize(QSizeF(c.paperWidth(), c.paperHeight()), QPrinter.Millimeter)
    printer.setFullPage(True)
    printer.setColorMode(QPrinter.Color)
    printer.setResolution(c.printResolution())

    pdfPainter = QPainter(printer)
    paperRectMM = printer.pageRect(QPrinter.Millimeter)
    paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
    c.render(pdfPainter, paperRectPixel, paperRectMM)
    pdfPainter.end()

    QTimer.singleShot(3000, savePDF)

def sort_toc(self):

    # Turn on/off layers as required by search type
    legend = self.iface.legendInterface()
    layers = legend.layers()
    wanted_layers = metal_wanted
    global turn_on, turn_off, atlas_desktop
    turn_off = []
    turn_on = []
    all_layers = []
    for layer in layers:
        layername = layer.name()
        all_layers.append(layername)
        layerid = layer.id()
        if layername == "desktop_search":
            atlas_desktop = layer
        if layername in wanted_layers and legend.isLayerVisible(layer) is False:
            turn_off.append(layer)
            legend.setLayerVisible(layer, True)
        if layername not in wanted_layers and legend.isLayerVisible(layer) is True:
            turn_on.append(layer)
            legend.setLayerVisible(layer, False)
        else:
            pass

    # Checks for required layers missing from map file
    for layer in wanted_layers:
        missing = []
        if layer not in all_layers:
            missing.append(layer)
        else:
            pass
    if not missing:
        pass
    else:
        QMessageBox.warning(self.iface.mainWindow(), "Missing layers", "Required layers are missing from your map file. Details: %s" % (str(missing)))
    return atlas_desktop

def quick_export(self, ref, stype, scale):

    # Add all layers in map canvas to render
    myMapRenderer = self.iface.mapCanvas().mapRenderer()

    # Load template from file
    myComposition = QgsComposition(myMapRenderer)
    myFile = os.path.join(os.path.dirname(__file__), 'MMR_Template.qpt')
    myTemplateFile = file(myFile, 'rt')
    myTemplateContent = myTemplateFile.read()
    myTemplateFile.close()
    myDocument = QDomDocument()
    myDocument.setContent(myTemplateContent)
    myComposition.loadFromTemplate(myDocument)

    # Get map composition and define scale
    myAtlasMap = myComposition.getComposerMapById(0)
    myAtlasMap.setNewScale(int(scale))

    # Setup Atlas
    myAtlas = QgsAtlasComposition(myComposition)
    myAtlas.setCoverageLayer(atlas_desktop) # Atlas run from desktop_search
    myAtlas.setComposerMap(myAtlasMap)
    myAtlas.setFixedScale(True)
    myAtlas.fixedScale()
    myAtlas.setHideCoverage(False)
    myAtlas.setFilterFeatures(True)
    myAtlas.setFeatureFilter("reference = '%s'" % (str(ref)))
    myAtlas.setFilterFeatures(True)

    # Generate atlas
    myAtlas.beginRender()
    for i in range(0, myAtlas.numFeatures()):
        myAtlas.prepareForFeature( i )
        jobs = r"\\MSUKSERVER\BusinessMan Docs\Jobs"
        job_fol = os.path.join(jobs, str(ref))
        output_jpeg = os.path.join(job_fol, ref + "_BMS_plan.jpg")
        myImage = myComposition.printPageAsRaster(0)
        myImage.save(output_jpeg)
    myAtlas.endRender()

def return_toc(self):

    # Revert layers back to pre-script state (on/off)
    legend = self.iface.legendInterface()
    for wanted in turn_on:
        legend.setLayerVisible(wanted, True)
    for unwanted in turn_off:
        legend.setLayerVisible(unwanted, False)