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

#Set input variables (Hard-wired)
inputFile = 'V:/ARGOSTracking/Data/ARGOSData/1997dg.txt'
outputFC = "V:/ARGOSTracking/Scratch/ARGOStrack.shp"

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
        
        #print results to see how we're doing
        print(tagID, "Lat:"+obsLat, "Long:"+obsLon, obsDate, obsTime, obsLC)
        
    #move to next line so while loop progresses (even if doesnt contain "Date :")
    lineString = inputFileObj.readline()
    
#close the file object
inputFileObj.close()