##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2020
## Author: hannah.g.smith@duke.edu (for ENV859)
##---------------------------------------------------------------------

#Import modules
import sys, os, arcpy 

# Allow arcpy to overwrite outputs
arcpy.env.overwriteOutput = True

#Set input variables (Hard-wired)
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997dg.txt'
outputFC = "V:/ARGOSTracking/Scratch/ARGOStrack.shp"
outputSR = arcpy.SpatialReference(54002)

# Create an empty feature class to which we'll add features
outPath, outName = os.path.split(outputFC)
arcpy.CreateFeatureclass_management(outPath, outName, "POINT",'','','', outputSR)

# Add field to our new feature class
arcpy.AddField_management(outputFC,"TagID","LONG")
arcpy.AddField_management(outputFC,"LC","TEXT")
arcpy.AddField_management(outputFC,"Date","DATE")

# Create and Insert cursor
cur = arcpy.da.InsertCursor(outputFC, ['Shape@', 'TagID', 'LC','Date'])
#%% Constuct a while loop to iterate through all lines in the datafile
#Open the ARGOS data file for reading
inputFileObj = open(inputFile, 'r')

#Get the ifrst line of data so we can use the while loop
lineString = inputFileObj.readline()

#Start the while loop 
#(while there is a valid lineString, meaning it has any characters at all)
while lineString:
    
    #set code to run only if the line contrains the string "Date :"
    #this is the unique substring for all data lines
    if ("Date :" in lineString):
        
        #parse line into a list
        lineData = lineString.split()
        
        #extract attributes from the datum header line
        tagID = lineData[0]
        obsDate = lineData[3]
        obsTime = lineData[4]
        obsLC = lineData[7]
        
        #extract location info from the next line
        line2String = inputFileObj.readline()
        
        #parse the line into a list
        line2Data = line2String.split()
        
        #extract the data we need to variable
        obsLat = line2Data[2]
        obsLon = line2Data[5]
        
        try:
            
            # Convert raw coordinate string to numbers
            if obsLat[-1] == 'N':
                obsLat = float(obsLat[:-1])
            else:
                obsLat = float(obsLat[:-1]) * -1
            if obsLon[-1] == 'E':
                obsLon = float(obsLon[:-1])
            else:
                obsLon = float(obsLon[:-1]) * -1
            
            # Create a point object
            obsPoint = arcpy.Point()
            obsPoint.X = obsLon
            obsPoint.Y = obsLat
                    
        except Exception as e:
            print(f"Error adding record {tagID} to the output")
            
        # Convert point to a geometric point, with spatial reference
        inputSR = arcpy.SpatialReference(4326)
        obsGeomPoint = arcpy.PointGeometry(obsPoint, inputSR)
            
        # Add a feature using our insert cursor
        feature = cur.insertRow((obsPoint,tagID,obsLC,obsDate.replace(".","/") + " " + obsTime))
        
    # Move to the next line so the while loop progresses
    lineString = inputFileObj.readline()
    
#Close the file object
inputFileObj.close()

#Delete the cursor
del cur