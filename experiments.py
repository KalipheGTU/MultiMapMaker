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