# -*- coding: cp1252 -*-
# Name: Konvertering vs. 3
# Formål: Dette script skal konvertere de nødvendige vektorlag til rasterlag
# Flemming Skov - februar - 2013
# Sidst opdateret: 18 maj 2014

# Ændringer: Stier ændret; også nyt marklag - hvor Bedrifts-ID'en er ændret, så tallene ikke overstiger 10 digits ..

# IMPORT SYSTEM MODULES
import arcpy, traceback, sys, time
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
nowTime = time.strftime('%X %x')
print "Konvertering påbegyndt: " + nowTime
print "... systemmoduler fundet og indlæst"

# DATA - HER SÆTTES LINKS TIL DIVERSE GEODATABASER OG FOLDERS
outPatch = "E:/Landskabsgenerering/landskaber/Vejlerne/vejlerne.gdb/"                     # Her gemmes de færdige rasterkort
localSettings = "E:/Landskabsgenerering/landskaber/Vejlerne/project.gdb/vejlerne_mask"    # Projektfolder med mask
gisDB = "E:/LandskabsGenerering/gis/dkgis.gdb"                                            # Her findes feature gis lagene
scratchDB = "E:/LandskabsGenerering/landskaber/Vejlerne/scratch"                          # Folder til temporære raster

# VIGTIGT-VIGTIGT-VIGTIGT:  Husk at ændre reference til det konkrete marklag i lagene 505 og 1000!!!

arcpy.env.overwriteOutput = True
arcpy.env.workspace = gisDB
arcpy.env.scratchWorkspace = scratchDB
arcpy.env.extent = localSettings
arcpy.env.mask = localSettings
arcpy.env.cellSize = localSettings
print "... geoprocessing settings indlæst"

print "This is a merge changes test"
print "It worked ..."


# VIGTIGT - styrer hvilke lag, der bliver konverteret; '1' køres scriptet; '0' gør det ikke
default = 1

landhav_c = default   #land_hav  - det faste land - og havet 

skrt105_c = default  #skraent - skrænter langs veje
vejk110_c = default  #vejkant
stie112_c = default  #stier - stier (inkl. cykelstier og grusstier af enhver art)
park114_c = default  #parkering - parkeringspladser
spor115_c = default  #vejmidt_brudt - spor (grusveje og spor)
jern120_c = default  #jernbane_brudt - jernbaner
vu30122_c = default  #vejmidt_brudt - små veje (under 3 meter)
vu60125_c = default  #vejmidt_brudt - mellemstore veje (3-6 meter)
vu90130_c = default  #vejmidt_brudt - store veje (over 6 meter)
# OBS: de følgende to lag tilknyttes foreløbig vejlaget for at sikre, at de ender øverst i mosaikken
hjsp150_c = default  #højspændingsmaster
vind155_c = default  #vindøller

lavb205_c = default   #lavbebyg - lav bebyggelse
hojb210_c = default   #hojbebyg - høj bebyggelse
byke215_c = default   #bykerne
indu220_c = default   #industri - industriområder
kirk225_c = default   #kirkegrd - kirkegaarde
sprt230_c = default   #sportanlaeg - sportsanlæg
bygn250_c = default   #bygning

skov310_c = default   #top10dk skov (alle typer)
krat315_c = default   #top10dk krat_bevoksning
sand320_c = default   #top10dk sand - især langs kyster
hede325_c = default   #top10dk hede - 'hede' dækker også klitter og overdrev
vaad330_c = default   #top10dk vaadområde - moser, enge, mv.

eng_355_c = default   #paragraf 3 eng
hede360_c = default   #paragraf 3 hede
mose365_c = default   #paragraf 3 mose
over370_c = default   #paragraf 3 overdrev
seng375_c = default   #paragraf 3 strandeng
soe_380_c = default   #paragraf 3 sø

soer440_c = default   #soer - søer
aaer435_c = default   #vandloeb_brudt - små vandløb (< 2.5 meter)
aaer436_c = default   #vandloeb_brudt - mellemstore vandløb (2.5 - 12 meter)
aaer437_c = default   #vandloeb_brudt - store vandløb (> 12 meter)
sorn420_c = default   #soer - randzone om søer

#NB: disse tre randzoner beregnes automatisk - de er nævnt her for at holde styr på koderne
#aarn425        #vandloeb_brudt - randzone om små vandløb
#aarn426        #vandloeb_brudt - randzone om mellemstore vandløb
#aarn427        #vandloeb_brudt - randzone om store vandløb

mark505_c = default   #markrandzoner
mark1000_c = default  #marker

dige620_c = default   #diger
fred625_c = default   #fred_fortid  - fredede fortidsminder
rekr630_c = default   #rekromr - rekreative områder - vel i reglen græs
hegn635_c = default   #levende hegn
trae640_c = default   #trægrupper
trae641_c = default   #enkeltstående træ
raas650_c = default   #raastof - raastofudvinding

ais1100_c = default   #ais arealanvendelse 100 kort

print " "

#####################################################################################################

try:

# 1 - land og hav (landhav)
  if landhav_c == 1:
    print "Processerer basiskort med land og hav ..."
    if arcpy.Exists(outPatch + "landhav"):
      arcpy.Delete_management(outPatch + "landhav")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("land_hav", "Land", outPatch + "landhav", "CELL_CENTER", "NONE", "1")

# 105 - Skrænter til raster (skrt105)
  if skrt105_c == 1:
    print "Processerer kunstige skrænter ved vejanlæg ..."
    if arcpy.Exists(outPatch + "skrt105"):
      arcpy.Delete_management(outPatch + "skrt105")
      print "... sletter eksisterende raster"
    eucDistVejkant = EucDistance("skraent","","1","")
    skrt105 = Con(eucDistVejkant < 2.5, 105, 1)
    skrt105.save(outPatch + "skrt105")

# 110 - Vejkanter til raster (vejk110)
  if vejk110_c == 1:
    print "Processerer vejkanter ..."
    if arcpy.Exists(outPatch + "vejk110"):
      arcpy.Delete_management(outPatch + "vejk110")
      print "... sletter eksisterende raster"
    eucDistVejkant = EucDistance("vejkant","","1","")
    vejk110 = Con(eucDistVejkant < 1.75, 110, 1)
    vejk110.save(outPatch + "vejk110")

# 112 - Stier til raster (stie112)
  if stie112_c == 1:
    print "Processerer stier  ..."
    if arcpy.Exists(outPatch + "stie120"):
      arcpy.Delete_management(outPatch + "stie112")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("veje_stier", "", "1", "")
    stie112 = Con(eucDistTmp < 1.51, 112, 1)
    stie112.save(outPatch + "stie112")
    
# 114 - Parkeringsarealer til raster (park114)
  if park114_c == 1:
    print "Processerer parkeringsområder ..."
    if arcpy.Exists(outPatch + "park114"):
      arcpy.Delete_management(outPatch + "park114")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("parkering", "", "1", "")
    park114 = Con(eucDistTmp < 3.0, 114, 1)
    park114.save(outPatch + "park114")

# 115 - Spor til raster (spor115)
  if spor115_c == 1:
    print "Processerer spor  ..."
    if arcpy.Exists(outPatch + "spor115"):
      arcpy.Delete_management(outPatch + "spor115")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("veje_spor", "", "1", "")
    spor115 = Con(eucDistTmp < 2.25, 115, 1)
    spor115.save(outPatch + "spor115")    

# 120 - Jernbaner til raster (jern120)
  if jern120_c == 1:
    print "Processerer jernbanespor ..."
    if arcpy.Exists(outPatch + "jern120"):
      arcpy.Delete_management(outPatch + "jern120")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("jernbane_brudt", "", "1", "")
    jern120 = Con(eucDistTmp < 4.5, 120, 1)
    jern120.save(outPatch + "jern120")

 # 122 - Små veje til raster (vu30122)
  if vu30122_c == 1:
    print "Processerer små veje  ..."
    if arcpy.Exists(outPatch + "vu30122"):
      arcpy.Delete_management(outPatch + "vu30122")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("veje_vu30", "", "1", "")
    vu30122 = Con(eucDistTmp < 1.75, 122, 1)
    vu30122.save(outPatch + "vu30122")

 # 125 - Mellemstore veje til raster (vu60125)
  if vu60125_c == 1:
    print "Processerer mellemstore veje ..."
    if arcpy.Exists(outPatch + "vu60125"):
      arcpy.Delete_management(outPatch + "vu60125")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("veje_vu60", "", "1", "")
    vu60125 = Con(eucDistTmp < 3.0, 125, 1)
    vu60125.save(outPatch + "vu60125")

 # 130 - Store veje til raster (vu90130)
  if vu90130_c == 1:
    print "Processerer store veje ..."
    if arcpy.Exists(outPatch + "vu90130"):
      arcpy.Delete_management(outPatch + "vu90130")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("veje_vu90", "", "1", "")
    vu90130 = Con(eucDistTmp < 5.0, 130, 1)
    vu90130.save(outPatch + "vu90130")

##### OBS: Højspændingsmaster og vindmøller sat ind i vejlaget; da de skal øverst i mosaikken

# 150 - Højspændingsmaster
  if hjsp150_c == 1:
    print "Processerer højspændingsmaster ..."
    if arcpy.Exists(outPatch + "hjsp150"):
      arcpy.Delete_management(outPatch + "hjsp150")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("hjspmast", "", "1", "")
    hjsp150 = Con(eucDistTmp < 1.5, 150, 1)
    hjsp150.save(outPatch + "hjsp150")

# 155 - Højspændingsmaster
  if vind155_c == 1:
    print "Processerer vindmøller ..."
    if arcpy.Exists(outPatch + "vind155"):
      arcpy.Delete_management(outPatch + "vind155")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("vindmoel", "", "1", "")
    vind155 = Con(eucDistTmp < 1.5, 155, 1)
    vind155.save(outPatch + "vind155")
     

# 205 - Lav bebyggelse
  if lavb205_c == 1:
    print "Processerer lav bebyggelse ..."
    if arcpy.Exists(outPatch + "lavb205"):
      arcpy.Delete_management(outPatch + "lavb205")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("lavbebyg", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    lavb205 = Con(rasIsNull == 1, 1, 205)
    lavb205.save(outPatch + "lavb205")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 210 - Høj bebyggelse
  if hojb210_c == 1:
    print "Processerer høj bebyggelse ..."
    if arcpy.Exists(outPatch + "hojb210"):
      arcpy.Delete_management(outPatch + "hojb210")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("hojbebyg", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    hojb210 = Con(rasIsNull == 1, 1, 210)
    hojb210.save(outPatch + "hojb210")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 215 - Bykerne
  if byke215_c == 1:
    print "Processerer bykerner ..."
    if arcpy.Exists(outPatch + "byke215"):
      arcpy.Delete_management(outPatch + "byke215")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("bykerne", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    byke215 = Con(rasIsNull == 1, 1, 215)
    byke215.save(outPatch + "byke215")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 220 - Industri
  if indu220_c == 1:
    print "Processerer industriområder ..."
    if arcpy.Exists(outPatch + "indu220"):
      arcpy.Delete_management(outPatch + "indu220")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("industri", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    indu220 = Con(rasIsNull == 1, 1, 220)
    indu220.save(outPatch + "indu220")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 225 - Kirkegårde
  if kirk225_c == 1:
    print "Processerer kirkegårde ..."
    if arcpy.Exists(outPatch + "kirk225"):
      arcpy.Delete_management(outPatch + "kirk225")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("kirkegrd", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    kirk225 = Con(rasIsNull == 1, 1, 225)
    kirk225.save(outPatch + "kirk225")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 230 - Sportsanlæg
  if sprt230_c == 1:
    print "Processerer sportsanlæg ..."
    if arcpy.Exists(outPatch + "sprt230"):
      arcpy.Delete_management(outPatch + "sprt230")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("sportanlaeg", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    sprt230 = Con(rasIsNull == 1, 1, 230)
    sprt230.save(outPatch + "sprt230")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 250 - Bygninger
  if bygn250_c == 1:
    print "Processerer bygninger ..."
    if arcpy.Exists(outPatch + "bygn250"):
      arcpy.Delete_management(outPatch + "bygn250")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("bygning", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    bygn250 = Con(rasIsNull == 1, 1, 250)
    bygn250.save(outPatch + "bygn250")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 310 - skove (OBS: har kun et tema for skov kan ikke underopdeles) (skov310)
  if skov310_c == 1:
    print "Processerer skove ..."
    if arcpy.Exists(outPatch + "skov310"):
      arcpy.Delete_management(outPatch + "skov310")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("skov", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    skov310 = Con(rasIsNull == 1, 1, 310)
    skov310.save(outPatch + "skov310")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 315 - krat (OBS: har kun et tema for skov kan ikke underopdeles) (krat315)
  if krat315_c == 1:
    print "Processerer kratvegetation ..."
    if arcpy.Exists(outPatch + "krat315"):
      arcpy.Delete_management(outPatch + "krat315")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("krat_bevoksning", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    krat315 = Con(rasIsNull == 1, 1, 315)
    krat315.save(outPatch + "krat315")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 320 - sand (svarer mest til sand ved kysten) (sand315)
  if sand320_c == 1:
    print "Processerer sandflader ..."
    if arcpy.Exists(outPatch + "sand320"):
      arcpy.Delete_management(outPatch + "sand320")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("sand", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    sand320 = Con(rasIsNull == 1, 1, 320)
    sand320.save(outPatch + "sand320")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 325 - hede (OBS: dækker både hede og overdrev og til dels klit) (hede325)
  if hede325_c == 1:
    print "Processerer hedevegetation ..."
    if arcpy.Exists(outPatch + "hede325"):
      arcpy.Delete_management(outPatch + "hede325")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("hede", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    hede325 = Con(rasIsNull == 1, 1, 325)
    hede325.save(outPatch + "hede325")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 330 - vaadomraade (vaad330)
  if vaad330_c == 1:
    print "Processerer vaadomraader ..."
    if arcpy.Exists(outPatch + "vaad330"):
      arcpy.Delete_management(outPatch + "vaad330")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("vaadomraade", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    vaad330 = Con(rasIsNull == 1, 1, 330)
    vaad330.save(outPatch + "vaad330")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 355 - p3 eng 3055 (eng_355)
  if eng_355_c == 1:
    print "Processerer paragraf3-enge ..."
    if arcpy.Exists(outPatch + "eng_355"):
      arcpy.Delete_management(outPatch + "eng_355")
      print "... sletter eksisterende raster"
    feat_class = "paragraf3"
    feat_layer = "eng_355"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3055')
    eucDisttmp = EucDistance("eng_355","","1","")
    eng_355 = Con(eucDisttmp < 3, 355, 1)
    eng_355.save(outPatch + "eng_355")

# 360 - p3 hede 3060 (hede360)
  if hede360_c == 1:
    print "Processerer paragraf3-heder ..."
    if arcpy.Exists(outPatch + "hede360"):
      arcpy.Delete_management(outPatch + "hede360")
      print "... sletter eksisterende raster"
    feat_class = "paragraf3"
    feat_layer = "hede360"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3060')
    eucDisttmp = EucDistance("hede360","","1","")
    hede360 = Con(eucDisttmp < 3, 360, 1)
    hede360.save(outPatch + "hede360")

# 365 - p3 mose 3065 (mose365)
  if mose365_c == 1:
    print "Processerer paragraf3-moser ..."
    if arcpy.Exists(outPatch + "mose365"):
      arcpy.Delete_management(outPatch + "mose365")
      print "... sletter eksisterende raster"
    feat_class = "paragraf3"
    feat_layer = "mose365"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3065')
    eucDisttmp = EucDistance("mose365","","1","")
    mose365 = Con(eucDisttmp < 3, 365, 1)
    mose365.save(outPatch + "mose365")

# 370 - p3 overdrev 3070 (over370)
  if over370_c == 1:
    print "Processerer paragraf3-overdrev ..."
    if arcpy.Exists(outPatch + "over370"):
      arcpy.Delete_management(outPatch + "over370")
      print "... sletter eksisterende raster"
    feat_class = "paragraf3"
    feat_layer = "over370"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3070')
    eucDisttmp = EucDistance("over370","","1","")
    over370 = Con(eucDisttmp < 3, 370, 1)
    over370.save(outPatch + "over370")

# 375 - p3 strandeng 3075 (seng375)
  if seng375_c == 1:
    print "Processerer paragraf3-strandeng ..."
    if arcpy.Exists(outPatch + "seng375"):
      arcpy.Delete_management(outPatch + "seng375")
      print "... sletter eksisterende raster"
    feat_class = "paragraf3"
    feat_layer = "seng375"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3075')
    eucDisttmp = EucDistance("seng375","","1","")
    seng375 = Con(eucDisttmp < 3, 375, 1)
    seng375.save(outPatch + "seng375")

# 380 - p3 sø 3080 (soe_380)
  if soe_380_c == 1:
    print "Processerer paragraf3-sø ..."
    if arcpy.Exists(outPatch + "soe_380"):
      arcpy.Delete_management(outPatch + "soe_380")
      print "... sletter eksisterende raster"
    feat_class = "paragraf3"
    feat_layer = "soe_380"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"OBJEKTKODE" = 3080')
    eucDisttmp = EucDistance("soe_380","","1","")
    soe_380 = Con(eucDisttmp < 1, 380, 1)
    soe_380.save(outPatch + "soe_380")

# 440 - Ferskvandssøer
  if soer440_c == 1:
    print "Processerer søer ..."
    if arcpy.Exists(outPatch + "soer440"):
      arcpy.Delete_management(outPatch + "soer440")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("soer", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    soer440 = Con(rasIsNull == 1, 1, 440)
    soer440.save(outPatch + "soer440")
    # arcpy.Delete_management(outPatch + "tmpRaster")

# 425/435 - Små vandløb (2.5-12) (vandloeb_brudt)+ buffer  OBS:  HUske at tilføje de 'ukendte'
  if aaer435_c == 1:
    print "Processerer små vandløb (0 - 2.5 meter)"
    if arcpy.Exists(outPatch + "aaer435"):
      arcpy.Delete_management(outPatch + "aaer435")
      print "... sletter eksisterende raster"
    if arcpy.Exists(outPatch + "aaer425"):
      arcpy.Delete_management(outPatch + "aaer425")
      print "... sletter eksisterende raster"
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

# 426/436 - Mellemstore vandløb (2.5-12) (vandloeb_brudt)+ buffer
  if aaer436_c == 1:
    print "Processerer mellemstore vandløb (2.5 - 12 meter)"
    if arcpy.Exists(outPatch + "aaer436"):
      arcpy.Delete_management(outPatch + "aaer436")
      print "... sletter eksisterende raster"
    if arcpy.Exists(outPatch + "aaer426"):
      arcpy.Delete_management(outPatch + "aaer426")
      print "... sletter eksisterende raster"
    feat_class = "vandloeb_brudt"
    feat_layer = "aaer416"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"MIT_BREDDE" = \'2,5 - 12 m\'')
    eucDistTmp = EucDistance("aaer416","","1","")
    aaer436 = Con(eucDistTmp < 5, 436, 1)
    aaer436.save(outPatch + "aaer436")
    aaer426 = Con(eucDistTmp < 7, 426, 1)
    aaer426.save(outPatch + "aaer426")

# 427/437 - Store vandløb (> 12 meter) (vandloeb_brudt)+ buffer
  if aaer437_c == 1:
    print "Processerer store vandløb (> 12 meter)"
    if arcpy.Exists(outPatch + "aaer437"):
      arcpy.Delete_management(outPatch + "aaer437")
      print "... sletter eksisterende raster"
    if arcpy.Exists(outPatch + "aaer427"):
      arcpy.Delete_management(outPatch + "aaer427")
      print "... sletter eksisterende raster"
    feat_class = "vandloeb_brudt"
    feat_layer = "aaer417"
    arcpy.MakeFeatureLayer_management(feat_class,feat_layer)
    arcpy.SelectLayerByAttribute_management(feat_layer, "NEW_SELECTION", '"MIT_BREDDE" = \'over 12 m\'')
    eucDistTmp = EucDistance("aaer417","","1","")
    aaer437 = Con(eucDistTmp < 5, 437, 1)
    aaer437.save(outPatch + "aaer437")
    aaer427 = Con(eucDistTmp < 7, 427, 1)
    aaer427.save(outPatch + "aaer427")

# 420 - randzoner om søer (sat til 2 meter på hver side (soer410)
  if sorn420_c == 1:
    print "Processerer randzoner om søer ..."
    if arcpy.Exists(outPatch + "sorn420"):
      arcpy.Delete_management(outPatch + "sorn420")
      print "... sletter eksisterende raster"
    eucDistVejkant = EucDistance("soer","","1","")
    sorn420 = Con(eucDistVejkant < 2.05, 420, 1)
    sorn420.save(outPatch + "sorn420") 

# 505 - randzoner ved marker (sat til 1 meter på hver side (mark505)
  if mark505_c == 1:
    print "Processerer markers randzoner ..."
    if arcpy.Exists(outPatch + "mark505"):
      arcpy.Delete_management(outPatch + "mark505")
      print "... sletter eksisterende raster"
    eucDistVejkant = EucDistance("MarkVJID12","","1","")
    mark505 = Con(eucDistVejkant < 1.05, 505, 1)
    mark505.save(outPatch + "mark505")

# mark1000 plus - konverterer markblokke således at hver markpolygon får sin unikke id
  if mark1000_c == 1:
    print "Processerer markpolygoner ..."
    if arcpy.Exists(outPatch + "mark1000"):
      arcpy.Delete_management(outPatch + "mark1000")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("MarkVJID12", "NYID", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    tmpIsNull = IsNull(outPatch + "tmpRaster")
    markNummerFirst = (Plus(outPatch + "tmpRaster", 0))
    markNummer = Int(markNummerFirst)
    mark10000 = Con(tmpIsNull == 1, 1, markNummer)
    mark10000.save(outPatch + "mark1000") 
   # arcpy.Delete_management(outPatch + "tmpRaster")

# 620 - konververing af diger (dige620)
  if dige620_c == 1:
    print "Processerer diger ..."
    if arcpy.Exists(outPatch + "dige620"):
      arcpy.Delete_management(outPatch + "dige620")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("dige", "", "1", "")
    dige620 = Con(eucDistTmp < 1.2, 620, 1)
    dige620.save(outPatch + "dige620")

# 625 - Fredede fortidsminder
  if fred625_c == 1:
    print "Processerer fredede fortidsminder ..."
    if arcpy.Exists(outPatch + "fred625"):
      arcpy.Delete_management(outPatch + "trae640")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("fred_fortid", "", "1", "")
    fred625 = Con(eucDistTmp < 6, 625, 1)
    fred625.save(outPatch + "fred625")

# 630 - Rekreative områder
  if rekr630_c == 1:
    print "Processerer rekreative områder ..."
    if arcpy.Exists(outPatch + "rekr630"):
      arcpy.Delete_management(outPatch + "rekr630")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("rekromr", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    rekr630 = Con(rasIsNull == 1, 1, 630)
    rekr630.save(outPatch + "rekr630")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 635 - konververing af levende hegn (hegn635)
  if hegn635_c == 1:
    print "Processerer levende hegn ..."
    if arcpy.Exists(outPatch + "hegn635"):
      arcpy.Delete_management(outPatch + "hegn635")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("hegn", "", "1", "")
    hegn635 = Con(eucDistTmp < 2, 635, 1)
    hegn635.save(outPatch + "hegn635")


# 640 - konvertering af enkeltstående trægrupper (trae640)
  if trae640_c == 1:
    print "Processerer grupper af enkeltstående træer ..."
    if arcpy.Exists(outPatch + "trae640"):
      arcpy.Delete_management(outPatch + "trae640")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("traegruppe", "", "1", "")
    trae640 = Con(eucDistTmp < 8, 640, 1)
    trae640.save(outPatch + "trae640")

# 641 - konvertering af enkeltstående træer (trae641)
  if trae641_c == 1:
    print "Processerer enkeltstående træer ..."
    if arcpy.Exists(outPatch + "trae641"):
      arcpy.Delete_management(outPatch + "trae641")
      print "... sletter eksisterende raster"
    eucDistTmp = EucDistance("trae", "", "1", "")
    trae641 = Con(eucDistTmp < 4, 641, 1)
    trae641.save(outPatch + "trae641")

# 650- Raastofudvinding
  if raas650_c == 1:
    print "Processerer områder med råstofudvinding ..."
    if arcpy.Exists(outPatch + "raas650"):
      arcpy.Delete_management(outPatch + "raas650")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("raastof", "FEAT_KODE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    raas650 = Con(rasIsNull == 1, 1, 650)
    raas650.save(outPatch + "raas650")
    arcpy.Delete_management(outPatch + "tmpRaster")

# 1100- AIS kortlægning til at udfylde baggrund
  if ais1100_c == 1:
    print "Processerer AIS arealanvendelseskort ..."
    if arcpy.Exists(outPatch + "ais1100"):
      arcpy.Delete_management(outPatch + "ais1100")
      print "... sletter eksisterende raster"
    arcpy.PolygonToRaster_conversion("ais100", "LUATYPE", outPatch + "tmpRaster", "CELL_CENTER", "NONE", "1")
    rasIsNull = IsNull(outPatch + "tmpRaster")
    ais1100 = Con(rasIsNull == 1, 1, outPatch + "tmpRaster")
    ais1100.save(outPatch + "ais1100")
    arcpy.Delete_management(outPatch + "tmpRaster")    


  endTime = time.strftime('%X %x')
  print ""
  print "Konvertering færdig: " + endTime



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



