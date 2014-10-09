# -*- coding: cp1252 -*-
# Name: twoInOne vs 1
# Purpose: This script combines conversion and mosaic
# Flemming Skov - Oct2014
# Last updated: October 9, 2014

# IMPORT SYSTEM MODULES
import arcpy, traceback, sys, time, gc
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
nowTime = time.strftime('%X %x')
gc.enable
print "Landscape conversion started: " + nowTime
print "... system modules checked"

# DATA - paths to data, output gdb, scratch folder and model landscape mask
outPatch = "C:/pytest/kalo1.gdb/"                                                 # saves maps here
localSettings = "C:/pytest/project.gdb/kalomask"                                  # project folder with mask
gisDB = "C:/pytest/gis/dkgis.gdb"                                                 # input features
scratchDB = "C:/pytest/scratch"                                                   # scratch folder for tempfiles
asciiexp = "C:/pytest/ASCII_kalo.txt"                                             # export in ascii (for ALMaSS)                  
reclasstable = "C:/pytest/reclass1.txt"                                           # reclass ascii table
gis2DB = outPatch                                                                 # input to mosaic (results from conversion) to mosaic process

# MODEL SETTINGS
arcpy.env.overwriteOutput = True
arcpy.env.workspace = gisDB
arcpy.env.scratchWorkspace = scratchDB
arcpy.env.extent = localSettings
arcpy.env.mask = localSettings
arcpy.env.cellSize = localSettings
print "... model settings read"

# CONTROLS which processes are executed
# *************************************

default = 1

#MOSAIC
vejnet_c = default
bebyggelser_c = default
natur_c = default
vaadnatur_c = default
ferskvand_c = default
kultur_c = default
mosaik_c = default

#CONVERSION  - features to raster layers
landhav_c = default   #land_sea 
skrt105_c = default   #slopes along roads
vejk110_c = default   #road verges
stie112_c = default   #paths
park114_c = default   #parking areas
spor115_c = default   #vejmidt_brudt - spor (grusveje og spor)
jern120_c = default   #railways
vu30122_c = default   #small roads (<3 meter)
vu60125_c = default   #medium sized roads (3-6 meter)
vu90130_c = default   #large roads (> 6 meter)
hjsp150_c = default   #pylons
vind155_c = default   #wind turbines
lavb205_c = default   #built up areas low
hojb210_c = default   #built up areas high
byke215_c = default   #city center
indu220_c = default   #industrial areas
kirk225_c = default   #cemeteries
sprt230_c = default   #sports areas
bygn250_c = default   #buildings
skov310_c = default   #top10dk forest
krat315_c = default   #top10dk shrub
sand320_c = default   #top10dk sand flats
hede325_c = default   #top10dk heath land
vaad330_c = default   #top10dk wetland
eng_355_c = default   #protected meadows
hede360_c = default   #protected heath land
mose365_c = default   #protected swamp
over370_c = default   #protected dry grassland
seng375_c = default   #protected marshes
soe_380_c = default   #protected lakes
soer440_c = default   #freshwater lakes
aaer435_c = default   #small streams (< 2.5 meter)
aaer436_c = default   #medium streams (2.5 - 12 meter)
aaer437_c = default   #large streams (> 12 meter)
sorn420_c = default   #lake buffer
mark505_c = default   #field buffer
mark1000_c = default  #fields
dige620_c = default   #dikes
fred625_c = default   #cultural trails
rekr630_c = default   #recreational areas
hegn635_c = default   #hedgerows
trae640_c = default   #tree groups
trae641_c = default   #individual trees
raas650_c = default   #gravel pits
ais1100_c = default   #ais landcover map

#NB: these buffers are calculated automatically - mentioned here to keep track on codes
#aarn425    #buffers small streams
#aarn426    #buffers medium streams
#aarn427    #buffers large streams

print " "

#####################################################################################################

try:

# CONVERSION - from feature layers to raster
#*******************************************

# 1 - land and sea (land_hav)
  if landhav_c == 1:
    print "Processing basis map (land/sea) ..."
    if arcpy.Exists(outPatch + "landhav"):
      arcpy.Delete_management(outPatch + "landhav")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("land_hav", "Land", outPatch + "landhav", "CELL_CENTER", "NONE", "1")

# 105 - slopes along larger roads (skrt105)
  if skrt105_c == 1:
    print "Processing artificial slopes along larger roads ..."
    if arcpy.Exists(outPatch + "skrt105"):
      arcpy.Delete_management(outPatch + "skrt105")
      print "... deletes existing raster"
    eucDistVejkant = EucDistance("skraent","","1","")
    skrt105 = Con(eucDistVejkant < 2.5, 105, 1)
    skrt105.save(outPatch + "skrt105")

# 110 - road verges (vejk110)
  if vejk110_c == 1:
    print "Processing road verges ..."
    if arcpy.Exists(outPatch + "vejk110"):
      arcpy.Delete_management(outPatch + "vejk110")
      print "... deletes existing raster"
    eucDistVejkant = EucDistance("vejkant","","1","")
    vejk110 = Con(eucDistVejkant < 1.75, 110, 1)
    vejk110.save(outPatch + "vejk110")

# 112 - paths (stie112)
  if stie112_c == 1:
    print "Processing paths  ..."
    if arcpy.Exists(outPatch + "stie120"):
      arcpy.Delete_management(outPatch + "stie112")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("veje_stier", "", "1", "")
    stie112 = Con(eucDistTmp < 1.51, 112, 1)
    stie112.save(outPatch + "stie112")
    
# 114 - parking areas (park114)
  if park114_c == 1:
    print "Processing parking areas ..."
    if arcpy.Exists(outPatch + "park114"):
      arcpy.Delete_management(outPatch + "park114")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("parkering", "", "1", "")
    park114 = Con(eucDistTmp < 3.0, 114, 1)
    park114.save(outPatch + "park114")

# 115 - dirt roads (spor115)
  if spor115_c == 1:
    print "Processing dirt roads  ..."
    if arcpy.Exists(outPatch + "spor115"):
      arcpy.Delete_management(outPatch + "spor115")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("veje_spor", "", "1", "")
    spor115 = Con(eucDistTmp < 2.25, 115, 1)
    spor115.save(outPatch + "spor115")    

# 120 - railway tracks (jern120)
  if jern120_c == 1:
    print "Processing railway tracks ..."
    if arcpy.Exists(outPatch + "jern120"):
      arcpy.Delete_management(outPatch + "jern120")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("jernbane_brudt", "", "1", "")
    jern120 = Con(eucDistTmp < 4.5, 120, 1)
    jern120.save(outPatch + "jern120")

 # 122 - Small roads (vu30122)
  if vu30122_c == 1:
    print "Processing small roads  ..."
    if arcpy.Exists(outPatch + "vu30122"):
      arcpy.Delete_management(outPatch + "vu30122")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("veje_vu30", "", "1", "")
    vu30122 = Con(eucDistTmp < 1.75, 122, 1)
    vu30122.save(outPatch + "vu30122")

 # 125 - Intermediate sized roads (vu60125)
  if vu60125_c == 1:
    print "Processing medium sized roads ..."
    if arcpy.Exists(outPatch + "vu60125"):
      arcpy.Delete_management(outPatch + "vu60125")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("veje_vu60", "", "1", "")
    vu60125 = Con(eucDistTmp < 3.0, 125, 1)
    vu60125.save(outPatch + "vu60125")

 # 130 - Large roads (vu90130)
  if vu90130_c == 1:
    print "Processing large roads ..."
    if arcpy.Exists(outPatch + "vu90130"):
      arcpy.Delete_management(outPatch + "vu90130")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("veje_vu90", "", "1", "")
    vu90130 = Con(eucDistTmp < 5.0, 130, 1)
    vu90130.save(outPatch + "vu90130")

# 150 - pylons (hjsp150)
  if hjsp150_c == 1:
    print "Processing pylons ..."
    if arcpy.Exists(outPatch + "hjsp150"):
      arcpy.Delete_management(outPatch + "hjsp150")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("hjspmast", "", "1", "")
    hjsp150 = Con(eucDistTmp < 1.5, 150, 1)
    hjsp150.save(outPatch + "hjsp150")

# 155 - wind turbines (vind155)
  if vind155_c == 1:
    print "Processing wind turbines ..."
    if arcpy.Exists(outPatch + "vind155"):
      arcpy.Delete_management(outPatch + "vind155")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("vindmoel", "", "1", "")
    vind155 = Con(eucDistTmp < 1.5, 155, 1)
    vind155.save(outPatch + "vind155")     

# 205 - built area - low (lavb205)
  if lavb205_c == 1:
    print "Processing built areas (low) ..."
    if arcpy.Exists(outPatch + "lavb205"):
      arcpy.Delete_management(outPatch + "lavb205")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("lavbebyg", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    lavb205 = Con(rasIsNull == 1, 1, 205)
    lavb205.save(outPatch + "lavb205")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 210 - built area - high (lavb210)
  if hojb210_c == 1:
    print "Processing built areas (high) ..."
    if arcpy.Exists(outPatch + "hojb210"):
      arcpy.Delete_management(outPatch + "hojb210")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("hojbebyg", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    hojb210 = Con(rasIsNull == 1, 1, 210)
    hojb210.save(outPatch + "hojb210")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 215 - city center  - (byke205)
  if byke215_c == 1:
    print "Processing city center ..."
    if arcpy.Exists(outPatch + "byke215"):
      arcpy.Delete_management(outPatch + "byke215")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("bykerne", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    byke215 = Con(rasIsNull == 1, 1, 215)
    byke215.save(outPatch + "byke215")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 220 - industry (indu220)
  if indu220_c == 1:
    print "Processing industrial areas ..."
    if arcpy.Exists(outPatch + "indu220"):
      arcpy.Delete_management(outPatch + "indu220")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("industri", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    indu220 = Con(rasIsNull == 1, 1, 220)
    indu220.save(outPatch + "indu220")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 225 - cemeteries (225)
  if kirk225_c == 1:
    print "Processing cemeteries ..."
    if arcpy.Exists(outPatch + "kirk225"):
      arcpy.Delete_management(outPatch + "kirk225")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("kirkegrd", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    kirk225 = Con(rasIsNull == 1, 1, 225)
    kirk225.save(outPatch + "kirk225")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 230 - sports fields (230)
  if sprt230_c == 1:
    print "Processing sports fields ..."
    if arcpy.Exists(outPatch + "sprt230"):
      arcpy.Delete_management(outPatch + "sprt230")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("sportanlaeg", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    sprt230 = Con(rasIsNull == 1, 1, 230)
    sprt230.save(outPatch + "sprt230")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 250 - buildings (bygn250)
  if bygn250_c == 1:
    print "Processing buildings ..."
    if arcpy.Exists(outPatch + "bygn250"):
      arcpy.Delete_management(outPatch + "bygn250")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("bygning", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    bygn250 = Con(rasIsNull == 1, 1, 250)
    bygn250.save(outPatch + "bygn250")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 310 - forests (skov310)
  if skov310_c == 1:
    print "Processing forests ..."
    if arcpy.Exists(outPatch + "skov310"):
      arcpy.Delete_management(outPatch + "skov310")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("skov", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    skov310 = Con(rasIsNull == 1, 1, 310)
    skov310.save(outPatch + "skov310")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 315 - shrubs  (krat315)
  if krat315_c == 1:
    print "Processing shrubs ..."
    if arcpy.Exists(outPatch + "krat315"):
      arcpy.Delete_management(outPatch + "krat315")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("krat_bevoksning", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    krat315 = Con(rasIsNull == 1, 1, 315)
    krat315.save(outPatch + "krat315")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 320 - sand flat - mainly beaches (sand320)
  if sand320_c == 1:
    print "Processing sand flats ..."
    if arcpy.Exists(outPatch + "sand320"):
      arcpy.Delete_management(outPatch + "sand320")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("sand", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    sand320 = Con(rasIsNull == 1, 1, 320)
    sand320.save(outPatch + "sand320")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 325 - heath land (hede325)
  if hede325_c == 1:
    print "Processing heath land ..."
    if arcpy.Exists(outPatch + "hede325"):
      arcpy.Delete_management(outPatch + "hede325")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("hede", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    hede325 = Con(rasIsNull == 1, 1, 325)
    hede325.save(outPatch + "hede325")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 330 - wetland (vaad330)
  if vaad330_c == 1:
    print "Processing wetland ..."
    if arcpy.Exists(outPatch + "vaad330"):
      arcpy.Delete_management(outPatch + "vaad330")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("vaadomraade", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    vaad330 = Con(rasIsNull == 1, 1, 330)
    vaad330.save(outPatch + "vaad330")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 355 - protected meadows (eng_355)
  if eng_355_c == 1:
    print "Processing protected meadows ..."
    if arcpy.Exists(outPatch + "eng_355"):
      arcpy.Delete_management(outPatch + "eng_355")
      print "... deletes existing raster"
    feat_class = "paragraf3"
    feat_layer = "eng_355"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3055')
    eucDisttmp = EucDistance("eng_355","","1","")
    eng_355 = Con(eucDisttmp < 3, 355, 1)
    eng_355.save(outPatch + "eng_355")

# 360 - protected heath land (hede360)
  if hede360_c == 1:
    print "Processing protected heath land ..."
    if arcpy.Exists(outPatch + "hede360"):
      arcpy.Delete_management(outPatch + "hede360")
      print "... deletes existing raster"
    feat_class = "paragraf3"
    feat_layer = "hede360"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3060')
    eucDisttmp = EucDistance("hede360","","1","")
    hede360 = Con(eucDisttmp < 3, 360, 1)
    hede360.save(outPatch + "hede360")

# 365 - protected swamp 3065 (mose365)
  if mose365_c == 1:
    print "Processing protected swamp ..."
    if arcpy.Exists(outPatch + "mose365"):
      arcpy.Delete_management(outPatch + "mose365")
      print "... deletes existing raster"
    feat_class = "paragraf3"
    feat_layer = "mose365"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3065')
    eucDisttmp = EucDistance("mose365","","1","")
    mose365 = Con(eucDisttmp < 3, 365, 1)
    mose365.save(outPatch + "mose365")

# 370 - protected dry grassland 3070 (over370)
  if over370_c == 1:
    print "Processing protected dry grassland ..."
    if arcpy.Exists(outPatch + "over370"):
      arcpy.Delete_management(outPatch + "over370")
      print "... deletes existing raster"
    feat_class = "paragraf3"
    feat_layer = "over370"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3070')
    eucDisttmp = EucDistance("over370","","1","")
    over370 = Con(eucDisttmp < 3, 370, 1)
    over370.save(outPatch + "over370")

# 375 - protected marsh 3075 (seng375)
  if seng375_c == 1:
    print "Processing protected marsh ..."
    if arcpy.Exists(outPatch + "seng375"):
      arcpy.Delete_management(outPatch + "seng375")
      print "... deletes existing raster"
    feat_class = "paragraf3"
    feat_layer = "seng375"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3075')
    eucDisttmp = EucDistance("seng375","","1","")
    seng375 = Con(eucDisttmp < 3, 375, 1)
    seng375.save(outPatch + "seng375")

# 380 - protected lakes 3080 (soe_380)
  if soe_380_c == 1:
    print "Processing protected lakes ..."
    if arcpy.Exists(outPatch + "soe_380"):
      arcpy.Delete_management(outPatch + "soe_380")
      print "... deletes existing raster"
    feat_class = "paragraf3"
    feat_layer = "soe_380"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3080')
    eucDisttmp = EucDistance("soe_380","","1","")
    soe_380 = Con(eucDisttmp < 1, 380, 1)
    soe_380.save(outPatch + "soe_380")

# 440 - lakes (soer440)
  if soer440_c == 1:
    print "Processing lakes ..."
    if arcpy.Exists(outPatch + "soer440"):
      arcpy.Delete_management(outPatch + "soer440")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("soer", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    soer440 = Con(rasIsNull == 1, 1, 440)
    soer440.save(outPatch + "soer440")
    # arcpy.Delete_management(outPatch + "tmpRaster")

# 425/435 - Small streams (2.5-12) (vandloeb_brudt)+ buffer  OBS:  remember to use 'ukendte'
  if aaer435_c == 1:
    print "Processing small streams (0 - 2.5 meter)"
    if arcpy.Exists(outPatch + "aaer435"):
      arcpy.Delete_management(outPatch + "aaer435")
      print "... deletes existing raster"
    if arcpy.Exists(outPatch + "aaer425"):
      arcpy.Delete_management(outPatch + "aaer425")
      print "... deletes existing raster"
    feat_class = "vandloeb_brudt"
    feat_layer = "aaer415"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"MIT_BREDDE" = \'0 - 2,5 m\'')
    arcpy.SelectLayerByAttribute_management(feat_layer, "ADD_TO_SELECTION", '"MIT_BREDDE" = \'Ukendt\'')
    eucDistTmp = EucDistance("aaer415","","1","")
    aaer435 = Con(eucDistTmp < 0.95, 435, 1)
    aaer435.save(outPatch + "aaer435")
    aaer425 = Con(eucDistTmp < 2.01, 425, 1)
    aaer425.save(outPatch + "aaer425")

# 426/436 - medium streams (2.5-12) (vandloeb_brudt)+ buffer
  if aaer436_c == 1:
    print "Processing medium streams (2.5 - 12 meter)"
    if arcpy.Exists(outPatch + "aaer436"):
      arcpy.Delete_management(outPatch + "aaer436")
      print "... deletes existing raster"
    if arcpy.Exists(outPatch + "aaer426"):
      arcpy.Delete_management(outPatch + "aaer426")
      print "... deletes existing raster"
    feat_class = "vandloeb_brudt"
    feat_layer = "aaer416"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"MIT_BREDDE" = \'2,5 - 12 m\'')
    eucDistTmp = EucDistance("aaer416","","1","")
    aaer436 = Con(eucDistTmp < 5, 436, 1)
    aaer436.save(outPatch + "aaer436")
    aaer426 = Con(eucDistTmp < 7, 426, 1)
    aaer426.save(outPatch + "aaer426")

# 427/437 - large streams (> 12 meter) (vandloeb_brudt)+ buffer
  if aaer437_c == 1:
    print "Processing large streams (> 12 meter)"
    if arcpy.Exists(outPatch + "aaer437"):
      arcpy.Delete_management(outPatch + "aaer437")
      print "... deletes existing raster"
    if arcpy.Exists(outPatch + "aaer427"):
      arcpy.Delete_management(outPatch + "aaer427")
      print "... deletes existing raster"
    feat_class = "vandloeb_brudt"
    feat_layer = "aaer417"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"MIT_BREDDE" = \'over 12 m\'')
    eucDistTmp = EucDistance("aaer417","","1","")
    aaer437 = Con(eucDistTmp < 5, 437, 1)
    aaer437.save(outPatch + "aaer437")
    aaer427 = Con(eucDistTmp < 7, 427, 1)
    aaer427.save(outPatch + "aaer427")

# 420 - lake buffer zones (soer410)
  if sorn420_c == 1:
    print "Processing lake buffer zones  ..."
    if arcpy.Exists(outPatch + "sorn420"):
      arcpy.Delete_management(outPatch + "sorn420")
      print "... deletes existing raster"
    eucDistVejkant = EucDistance("soer","","1","")
    sorn420 = Con(eucDistVejkant < 2.05, 420, 1)
    sorn420.save(outPatch + "sorn420") 

# 505 - field buffer zones (mark505)  # Not used anymore
  if mark505_c == 1:
    print "Processing field buffers ..."
    if arcpy.Exists(outPatch + "mark505"):
      arcpy.Delete_management(outPatch + "mark505")
      print "... deletes existing raster"
    eucDistVejkant = EucDistance("MarkVJID12","","1","")
    mark505 = Con(eucDistVejkant < 1.05, 505, 1)
    mark505.save(outPatch + "mark505")

# mark1000 plus - converts field polygons and provides each polygon a unique id
  if mark1000_c == 1:
    print "Processing field polygons ..."
    if arcpy.Exists(outPatch + "mark1000"):
      arcpy.Delete_management(outPatch + "mark1000")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("MarkVJID12", "NYID", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    tmpIsNull = IsNull(outPatch + "tmpRaster")
    markNummerFirst = (Plus(outPatch + "tmpRaster", 0))
    markNummer = Int(markNummerFirst)
    mark10000 = Con(tmpIsNull == 1, 1, markNummer)
    mark10000.save(outPatch + "mark1000") 
   # arcpy.Delete_management(outPatch + "tmpRaster")

# 620 - dikes (dige620)
  if dige620_c == 1:
    print "Processing dikes ..."
    if arcpy.Exists(outPatch + "dige620"):
      arcpy.Delete_management(outPatch + "dige620")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("dige", "", "1", "")
    dige620 = Con(eucDistTmp < 1.2, 620, 1)
    dige620.save(outPatch + "dige620")

# 625 - ancient culture trails (fred625)
  if fred625_c == 1:
    print "Processing ancient cultural trails ..."
    if arcpy.Exists(outPatch + "fred625"):
      arcpy.Delete_management(outPatch + "trae640")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("fred_fortid", "", "1", "")
    fred625 = Con(eucDistTmp < 6, 625, 1)
    fred625.save(outPatch + "fred625")

# 630 - recreational areas (rekr630)
  if rekr630_c == 1:
    print "Processing recreational areas ..."
    if arcpy.Exists(outPatch + "rekr630"):
      arcpy.Delete_management(outPatch + "rekr630")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("rekromr", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    rekr630 = Con(rasIsNull == 1, 1, 630)
    rekr630.save(outPatch + "rekr630")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 635 - hdgerows (hegn635)
  if hegn635_c == 1:
    print "Processing hedgerows..."
    if arcpy.Exists(outPatch + "hegn635"):
      arcpy.Delete_management(outPatch + "hegn635")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("hegn", "", "1", "")
    hegn635 = Con(eucDistTmp < 2, 635, 1)
    hegn635.save(outPatch + "hegn635")

# 640 - tree groups (trae640)
  if trae640_c == 1:
    print "Processing tree groups ..."
    if arcpy.Exists(outPatch + "trae640"):
      arcpy.Delete_management(outPatch + "trae640")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("traegruppe", "", "1", "")
    trae640 = Con(eucDistTmp < 8, 640, 1)
    trae640.save(outPatch + "trae640")

# 641 - individual trees (trae641)
  if trae641_c == 1:
    print "Processing individual trees ..."
    if arcpy.Exists(outPatch + "trae641"):
      arcpy.Delete_management(outPatch + "trae641")
      print "... deletes existing raster"
    eucDistTmp = EucDistance("trae", "", "1", "")
    trae641 = Con(eucDistTmp < 4, 641, 1)
    trae641.save(outPatch + "trae641")

# 650- gravel pits (raas650)
  if raas650_c == 1:
    print "Processing gravel pits ..."
    if arcpy.Exists(outPatch + "raas650"):
      arcpy.Delete_management(outPatch + "raas650")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("raastof", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    raas650 = Con(rasIsNull == 1, 1, 650)
    raas650.save(outPatch + "raas650")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 1100- AIS map (ais1100)
  if ais1100_c == 1:
    print "Processing AIS map ..."
    if arcpy.Exists(outPatch + "ais1100"):
      arcpy.Delete_management(outPatch + "ais1100")
      print "... deletes existing raster"
    arcpy.PolygonToRaster_conversion("ais100", "LUATYPE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    ais1100 = Con(rasIsNull == 1, 1, outPatch + "tmpRaster")
    ais1100.save(outPatch + "ais1100")
    arcpy.Delete_management(outPatch + "tmpRaster")

  gc.collect()  # Adresses memory problems

# MOSAIC
#*******************************************************************

  arcpy.env.workspace = gis2DB   #workspace input for the mosaic process
  print " "

  if vejnet_c == 1:   #Assembles a transportation theme for roads and road verges
    print "Processing roads theme ..."
    if arcpy.Exists(outPatch + "T1_vejnet"):
      arcpy.Delete_management(outPatch + "T1_vejnet")
      print "... deletes existing raster"
    vejRastList = [Raster ("vejk110"), Raster ("stie112"), Raster ("spor115"), Raster ("hjsp150"), Raster ("vind155"),
                   Raster ("jern120"), Raster ("vu30122"), Raster ("vu60125"), Raster ("vu90130"), Raster ("park114"), Raster("landhav")]
    vejnet = CellStatistics(vejRastList, "MAXIMUM", "DATA")    
       #  use next line if the road themes should be shrinked - remember to change 'vejnet' above to 'vejnet0'
       #  may result in 'stripes' or other artificial looking features
       #  vejnet = Shrink(vejnet0, 1, 1)
    vejnet.save (outPatch + "T1_vejnet")
    
  if bebyggelser_c == 1:   #Assembles a built up theme 
    print "Processing bebyggelser ..."
    if arcpy.Exists(outPatch + "T2_bebyggelser"):
      arcpy.Delete_management(outPatch + "T2_bebyggelser")
      print "... deletes existing raster"
    bebyggelserRastList = [Raster ("lavb205"), Raster ("hojb210"), Raster ("byke215"), Raster ("kirk225"), Raster ("bygn250"), Raster ("sprt230"), Raster ("indu220"), Raster ("landhav")]
    bebyggelser = CellStatistics(bebyggelserRastList, "MAXIMUM", "DATA")
    bebyggelser.save (outPatch + "T2_bebyggelser")

  if natur_c == 1:   #Assembles a natural areas theme 
    print "Processing natural areas ..."
    if arcpy.Exists(outPatch + "T3_natur"):
      arcpy.Delete_management(outPatch + "T3_natur")
      print "... deletes existing raster"
    naturRastList = [Raster ("skrt105"), Raster ("skov310"), Raster ("krat315"), Raster ("sand320"), Raster ("hede325"), Raster ("vaad330"), Raster ("eng_355"), Raster ("hede360"), Raster ("mose365"), Raster ("over370"), Raster ("seng375"), Raster ("soe_380"), Raster ("landhav")]
    natur = CellStatistics(naturRastList, "MAXIMUM", "DATA")
    natur.save (outPatch + "T3_natur")  

  if vaadnatur_c == 1:   #Assembles a 'wet nature' theme 
    print "Processing wet natural areas ..."
    if arcpy.Exists(outPatch + "T3_vaadnatur"):
      arcpy.Delete_management(outPatch + "T3_vaadnatur")
      print "... deletes existing raster"
    vaadnaturRastList = [Raster ("mose365"), Raster ("soe_380"), Raster ("landhav")]
    vaadnatur = CellStatistics(vaadnaturRastList, "MAXIMUM", "DATA")
    vaadnatur.save (outPatch + "T3_vaadnatur")  

  if ferskvand_c == 1:   #Assembles a fresh water theme 
    print "Processing streams and lakes ..."
    if arcpy.Exists(outPatch + "T4_vand"):
      arcpy.Delete_management(outPatch + "T4_vand")
      print "... deletes existing raster"
    vandRastList = [Raster ("soer440"), Raster ("aaer435"), Raster ("aaer436"), Raster ("aaer437"),
                    Raster ("sorn420"), Raster ("aaer425"), Raster ("aaer426"), Raster ("aaer427"), Raster ("landhav")]
    vand = CellStatistics(vandRastList, "MAXIMUM", "DATA")
    vand.save (outPatch + "T4_vand")

  if kultur_c == 1:   # Assembles a theme of cultural features
    print "Processing hedgerows, dikes, trees, etc ..."
    if arcpy.Exists(outPatch + "T5_kultur"):
      arcpy.Delete_management(outPatch + "T5_kultur")
      print "... deletes existing raster"
      # "fred625" = fredede fortidsminder
    kulturRastList = [Raster ("dige620"), Raster ("fred625"), Raster ("rekr630"), Raster ("hegn635"), Raster ("trae640"), Raster ("trae641"),
                    Raster ("raas650"), Raster ("landhav")]
      # Denne raekkefoelge burde give mere mening.               
    kultur = CellStatistics(kulturRastList, "MAXIMUM", "DATA")
    kultur.save (outPatch + "T5_kultur")

  gc.collect()  # Adresses memory problems

  if mosaik_c == 1:   # Assemble the raw mosaic - controls which layers have priorithy and end on top
    print "Processing mosaic for all themes ..."
    if arcpy.Exists(outPatch + "Mosaik_rekl"):
      arcpy.Delete_management(outPatch + "Mosaik_rekl")
    if arcpy.Exists(outPatch + "Mosaik_raa"):
      arcpy.Delete_management(outPatch + "Mosaik_raa")
    if arcpy.Exists(outPatch + "Mosaik_almass"):
      arcpy.Delete_management(outPatch + "Mosaik_almass")
      
    print "... deleting existing rasters"
    print " "

 #  The raw mosaic is put together here. The script controls which layers a prioritized (on top) 
    T1ve = Raster("T1_vejnet")
    T2be = Raster("T2_bebyggelser")
    T3na = Raster("T3_natur")
    T3ana = Raster("T3_vaadnatur")
    T4va = Raster("T4_vand")
    T5ku = Raster("T5_kultur")
    ais1100 = Raster("ais1100")  
    mark1 = Raster("mark505")    # field boundary
    mark2 = Raster("mark1000")   # fields
    landhav = Raster("landhav")
    bygn = Raster("bygn250")

    step1 = Con(mark2 > 999, mark2, 1)                    # fields first
    print "fields added to mosaic ..."
    step2 = Con(T4va == 1, step1, T4va)                   # fresh water on top
    print "fresh water added to mosaic ..."
    step3 = Con(step2 == 1, T3na, step2)                  # natural areas on NOT (fields, water)
    print "natural areas added to mosaic ..."
    step4 = Con(step3 == 1, T2be, step3)                  # built up areas on NOT (fields, water, natural areas)
    print "built up areas added to mosaic ..."
    step4a = Con(T3ana == 1, step4, T3ana)                # wet natural areas on top
    print "wet natural areas added to mosaic  ..."
    step5 = Con(T5ku == 1, step4a, T5ku)                  # cultural features on top
    print "cultural landscape features added to mosaic ..."
    step6 = Con(T1ve == 1, step5, T1ve)                   # roads on top
    print "roads added to mosaic ..."
    step7 = Con(bygn == 1, step6, bygn)                   # buildings on top
    print "buildings added to mosaic ..."
    mosaik01 = Con(landhav == 1, step7, 0)                # sea added
    print "sea added to mosaic ..."
    mosaik1 = Con(mosaik01 == 1, ais1100, mosaik01) # laegger ais-laget, hvor der ikke er andet
    mosaik1.save (outPatch + "Mosaik_raa")
    nowTime = time.strftime('%X %x')
    print "Raw mosaic assembled ..." + nowTime

# reclassify to ALMaSS raster values
    mosaik2 = ReclassByASCIIFile(mosaik1, reclasstable, "DATA")
    mosaik2.save(outPatch + "Mosaik_rekl")
    nowTime = time.strftime('%X %x')
    print "Reclassification done ..." + nowTime

# regionalise map
    regionALM = RegionGroup(mosaik2,"EIGHT","WITHIN","ADD_LINK","")
    regionALM.save(outPatch + "Mosaik_almass")
    nowTime = time.strftime('%X %x')
    print "Regionalisation done ..." + nowTime

# convert regionalised map to export ascii  - keep the file name - the program to make the lsb file will be looking for it.
    arcpy.RasterToASCII_conversion(regionALM, asciiexp)
    print "Conversion to ASCII done ..." + nowTime

  endTime = time.strftime('%X %x')
  print ""
  print "The End: " + endTime


except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n     " +        str(sys.exc_type) + ": " + str(sys.exc_value) + "\n"
    msgs = "ARCPY ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    arcpy.AddError(msgs)
    arcpy.AddError(pymsg)

    print msgs
    print pymsg

    arcpy.AddMessage(arcpy.GetMessages(1))
    print arcpy.GetMessages(1)



