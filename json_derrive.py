# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 11:24:13 2017

@author: Mike

Quick script for building base jsonLd files for site
"""

# Assumptions. English as standard?
language = ""


content = {
 "@context":"ons-context.jsonld",
 "id":"",
 "type":"Dataset",
 "identifier":"",
 "title":"",
 "description":"",
 "issued":"",
 "language":language,
 "keyword":[""],
 "publisher":{
    "type": "Organization",
    "name": "Office of National Statistics",
    "homepage": "https://www.ons.gov.uk/"
 },
 "contactPoint":{
    "name": "",
    "email": "",
    "tel": "",
 },
 "accessRights":{
    "dataLicence": "http://www.nationalarchives.gov.uk/doc/open-government-licence",
    "contentLicence": "http://www.nationalarchives.gov.uk/doc/open-government-licence",
    "attributionText": "Contains public sector information licensed under the Open Government Licence v3.0",
    "copyrightNotice": "Crown Copyright",
    "reuserGuidelines": "https://www.ons.gov.uk/help/termsandconditions",    
    "attributionLink": ""
 },
 "landingPage":"",
 "theme":"",
 "dct:source":"",
 "stat:dimension":[
   { 
     "type": "qb:Dimension",
     "name": "" 
   },
   { 
     "type": "qb:Dimension",
     "name": "" 
   },    
   { 
     "type": "qb:Dimension",
     "name": "" 
   },
   { 
     "type": "qb:Dimension",
     "name": "" 
   }],
 "dct:temporal":"",
 "dct:spatial":"", 
 "distribution":[{
    "title": "",
    "description": "",
    "issued": "",
    "language": language,
    "accessURL": "",
    "downloadURL": "",
    "mediaType": "http://www.iana.org/assignments/media-types/application/vnd.ms-excel",
    "license": "http://www.nationalarchives.gov.uk/doc/open-government-licence",
    "rights": {
        "dataLicence": "http://www.nationalarchives.gov.uk/doc/open-government-licence",
        "contentLicence": "http://www.nationalarchives.gov.uk/doc/open-government-licence",
        "attributionText": "Contains public sector information licensed under the Open Government Licence v3.0",
        "copyrightNotice": "Crown Copyright",
        "reuserGuidelines": "https://www.ons.gov.uk/help/termsandconditions",    
        "attributionLink": "https://onsdigital.github.io/dp-ux-prototypes/dist/sprint-06-dataset/dataset.html"
    }
 }]
}


import pandas as pd
import json

# Get all the dimension labels from the load file
def derDimensionLabels(df):
    
    # geo hierarchies are in code form, be ready to tidy them up
    tidyCodes = {
               '2011WARDH':'2011 Administrative Hierarchy',
               '2011STATH':'2011 Statistical Geography Hierarchy',
               '2011PCONH':'2011 Westminster Parliamentary Constituency Hierarchy',
               '2012WARDH':'2012 Administrative Hierarchy',
               '2013HEALTHH':'2013 Health Area Hierarchy',
               'UKWARD':'2013 UK Ward Hierarchy',
               '2013WARDH':'2013 WARDH',
               '2015EUROSTATH':'2015 NUTS'
               } # TODO - actualy use this :)
               
    dimensionLabels = []
    headers = [x for x in df.columns.values if 'Dimension_Name' in x]
    for h in headers:
        assert len(df[h]) != 1, "{h} has more than one label: {ex}".format(h=h, ex=df[h].unique())
        if h in tidyCodes.keys():
            h = tidycodes[h]
        dimensionLabels.append({"type": "qb:Dimension", "name": df[h].unique()[0]})

    return dimensionLabels
    
    
    
# Takes a list of geo codes and creates a spacial statement for metadata
# TODO - using a json scrape, this will need to change when the APIs sorted
def defSpacialFromCodes(allCodes, chosenHier):
    
    with open('jsonDUMP.json', 'r') as f:
        jsonMassData = json.load(f)
        
        for hier in jsonMassData:
            for k in hier.keys():
                if k == chosenHier:                            
                    levelList = [x['level_name'] for x in hier[k] if x != None and x['code'] in allCodes and x]
                    finalList = [] # TODO - just nasty
                    for ll in levelList:
                        if ll not in finalList: finalList.append(ll)
        return finalList
        

# Get the spacial data
def derSpacial(df):
    geoHierarchies = ['2011WARDH','2011STATH','2011PCONH','2012WARDH',
                      '2013HEALTHH','UKWARD', '2013WARDH', '2015EUROSTATH']
                      
    possibleHierarchies = [x for x in df if 'Dimension_Hierarchy_' in x]

    for hier in possibleHierarchies:
        items = df[hier].unique()
        if len(items) == 1:
            if items[0] in geoHierarchies:
                # Found it, now get the codes
                allCodes = df['Dimension_Value_' + hier[-1:]].unique()
                chosenHier = hier
    
    return defSpacialFromCodes(allCodes, df[chosenHier].unique()[0])
    

    
def derTemporal(df):
    
    # find the unique items in Dimension_Value_1 (time)
    uniqueTimes = df['Dimension_Value_1'].unique()
    assert len(uniqueTimes) > 0, 'Error: Cannot find any times in Dimension_Value_1'

    # if its 1, its a year so return early
    if len(uniqueTimes) == 1: return str(uniqueTimes[0]).replace('.0', '') # just incase replace

    # if its a range of years
    if [x for x in uniqueTimes if len(x) == 4] == len(uniqueTimes):
        start = min([x for x in uniqueTimes if len(x) == 4])
        end = [x for x in uniqueTimes if len(x) == 4]
        return str(start) + ' to '  + str(end)
    
    # if its a range of quarters
    yearOnly = [x[:4] for x in uniqueTimes]
    minYear = min(yearOnly)
    maxYear = max(yearOnly)
    
    #if its quarters
    quarterFinds = [x for x in uniqueTimes if 'Q1' in x or 'Q2' in x]
    monthFinds = [x for x in uniqueTimes if '.01' in x or '.02' in x or '.03' in x]

    if len(monthFinds) > 0 and len(quarterFinds) > 0: 
        raise ValueError("Both Quarter and Months in time")

    if len(quarterFinds) > 0:
        for qrt in ['.Q4','.Q3', '.Q2', '.Q1']:
            if minYear + qrt in uniqueTimes:
                    minYear = minYear + qrt
        for qrt in ['.Q1','.Q2', '.Q3', '.Q4']:
            if maxYear + qrt in uniqueTimes:
                    maxYear = maxYear + qrt                    
                    
        return minYear[-2:] + ' ' + minYear[:4] + ' to ' + maxYear[-2:] + ' ' + maxYear[:4]
                
    
    
def main(csvName):
    df = pd.read_csv(csvName)
    
    content['stat:dimension'] = derDimensionLabels(df)
    content['dct:spatial'] = derSpacial(df)
    content['dct:temporal'] = derTemporal(df)

    with open('Meta_'+csvName[:-4]+'.jsonld', 'w') as jFile:
        json.dump(content, jFile, sort_keys=True)
    
    
import sys
tryFile = sys.argv[1]
main(tryFile)

