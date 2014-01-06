#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script to load the set of images acquired in the x-ray lab.
Since we acquire lots of images before, during and after exposure it's really
annoying to manually sift through all the images in all the directories and
look for the 'best' exposure.
This script loads computes the mean of each image in each directory and gives
out the maximum of the this mean.
This should be the 'best' exposed image of all the exposures.
"""

from __future__ import division
import glob
import os
from pylab import *
import shutil

# Setup
# Threshold to delete folders with images with a mean smaller than X, folders
# where the darkest and brightest image are only X grey levels different and
# delete images which are darker than 10X % of the second darkest image
Threshold = 5

#~ StartingFolder = '/afs/psi.ch/user/h/haberthuer/EssentialMed/Dev/Images/tis'
StartingFolder = '/afs/psi.ch/project/EssentialMed/Images/' +\
    '12-GOTTHARD_and_TIS/TIS/'

# Get list of (only) directories in StartingFolder
# http://stackoverflow.com/a/973488
ListOfFolders = [x[0] for x in os.walk(StartingFolder)]

Exposures = [glob.glob(os.path.join(Folder, '*.jpg'))
             for Folder in ListOfFolders]

# os.walk includes the base directory, thus go from 1 to end...
for i in range(1, len(Exposures)):
    plt.figure(figsize=[16, 9])
    print 20 * '-', i, '/', len(Exposures) - 1, 20 * '-'
    print 'Getting the mean of', len(Exposures[i]), 'Images from',\
        os.path.basename(ListOfFolders[i])
    MeanValue = [plt.imread(Image).mean() for Image in Exposures[i]]
    print 'The mean value of the images varies between',\
        round(min(MeanValue), 2), 'and', round(max(MeanValue), 2)
    print 'A maximum of', round(max(MeanValue), 2), 'was found in image',\
        MeanValue.index(max(MeanValue)), 'which corresponds to',\
        os.path.basename(Exposures[i][MeanValue.index(max(MeanValue))])
    plt.subplot(1, 2, 1)
    plt.plot(MeanValue, label='Mean Value', marker='o')
    plt.axhline(y=max(MeanValue), color='g',
                label=''.join(['Max@', str(int(round(max(MeanValue))))]))
    plt.axhline(y=sort(MeanValue)[1] * (1 + Threshold / 100), color='r',
                label=''.join(['Deletion<',
                               str(int(round(sort(MeanValue)[1] *
                                             (1 + Threshold / 100))))]))
    plt.legend()
    plt.xlabel('Mean')
    plt.ylabel('Image index')
    plt.title(' '.join(['Mean of', str(len(Exposures[i])),
                        'images in\n',
                        str(os.path.basename(ListOfFolders[i]))]))
    plt.ylim([0, 256])
    plt.subplot(3, 2, 2)
    plt.imshow(plt.imread(Exposures[i][MeanValue.index(max(MeanValue)) - 1]),
               origin='lower')
    plt.title(' '.join(['maximal value of', str(round(max(MeanValue), 2)),
                        '\nfound in',
                        str(os.path.basename(
                            Exposures[i][MeanValue.index(max(MeanValue))])),
                        '\nshowing this image (middle) and the two adjacent']))
    plt.subplot(3, 2, 4)
    plt.imshow(plt.imread(Exposures[i][MeanValue.index(max(MeanValue))]),
               origin='lower')
    plt.subplot(3, 2, 6)
    plt.imshow(plt.imread(Exposures[i][MeanValue.index(max(MeanValue)) + 1]),
               origin='lower')
    plt.savefig(os.path.join(StartingFolder,
                             os.path.basename(ListOfFolders[i]) + '.pdf'))
    plt.show()

    # Delete unnecessary files -> Proceed with caution!
    # 	* Delete the whole image directory if *all* images are below "Threshold"
    # 	  threhold
    # 	* Delete the whole image directory if the darkest and brightest image
    #     have a difference of less than "Threshold"
    #   * Delete all images with are not "Threhold"-% brighter than the
    #     *second*-darkest image
    Delete = True
    if max(MeanValue) < Threshold:
        print
        print 'None of the images has a mean larger than the threshold of',\
            Threshold
        if Delete:
            print 'I am thus deleting the whole directory...'
            shutil.rmtree(ListOfFolders[i])
        else:
            print 'One could thus delete', ListOfFolders[i]
        print
    elif (max(MeanValue) - min(MeanValue)) < Threshold:
        print
        print 'The mean of the brightest (' + str(round(max(MeanValue), 2)) +\
            ') and the darkest image (' + str(round(min(MeanValue), 2)) +\
            ') have a difference smaller than', Threshold
        if Delete:
            print 'I am thus deleting the whole directory...'
            shutil.rmtree(ListOfFolders[i])
        else:
            print 'One could thus delete', ListOfFolders[i]
        print
    else:
        print 'Looking for images with a mean value between the minimum (' +\
            str(round(min(MeanValue), 2)) + ') and', 100 + Threshold,\
            '% of the second-brightest image (' +\
            str(round(sort(MeanValue)[1] * (1 + Threshold / 100), 2)) + ')'
        for DeletionCandidate in range(len(Exposures[i])):
            if MeanValue[DeletionCandidate] < sort(MeanValue)[1] * (1 +
                                                                    Threshold /
                                                                    100):
                print os.path.basename(Exposures[i][DeletionCandidate]),\
                    'has a mean of', round(MeanValue[DeletionCandidate], 2),
                if Delete:
                    print 'I am thus deleting it.'
                    os.remove(Exposures[i][DeletionCandidate])
                else:
                    print 'One could thus delete it'
            else:
                print os.path.basename(Exposures[i][DeletionCandidate]),\
                    'has a mean of', round(MeanValue[DeletionCandidate], 2),\
                    'thus keeping it.'

    # Open remaining images as stack in ImageJ
    # First check if the folder still exists or we deleted it above. Then open
    # ImageJ with all the files in the folder as a stack, scaled to 25%
    ShowStack = True
    if ShowStack:
        if os.path.isdir(ListOfFolders[i]):
            viewcommand = 'imagej -e "run(\\"Image Sequence...\\", \\"open=' +\
                os.path.abspath(ListOfFolders[i]) + ' scale=25\\");"'
            print 'Starting ImageJ with the command'
            print '---'
            print viewcommand
            print '---'
            print 'Quit ImageJ to proceed!'
            os.system(viewcommand)
