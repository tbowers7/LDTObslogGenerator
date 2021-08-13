# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 16:40:05 2015
Modified: Tue Aug 10 2021

@author: rhamilton
@contriutor: tbowers
"""
# Regen the UI Py file via:
#   pyuicX LDTObslogGeneratorPanel.ui -o LDTObslogGeneratorPanel.py
# Where X = your Qt version

import sys
import csv
import pytz
import glob
import fnmatch
import datetime
import itertools
from os import listdir, walk
from os.path import join, basename, getmtime

import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
import astropy.io.fits as pyf
import ephem

from . import FITSKeywordPanel as fkwp
from . import LDTObslogGeneratorPanel as logp


def headerList(infile, headerlist, HDU=0):
    """
    Given a FITS file and a list of header keywords of interest,
    parse those two together and return the result as a tuple of
    base filename and an sequential list of the keywords.
    """
    key = ''
    bname = basename(infile)
    try:
        hed = pyf.getheader(infile, ext=HDU)
    except:
        hed = ' '

    item = []
    for key in headerlist:
        try:
            item.append(hed[key])
        except:
            item.append('')

    return bname, item


def headerDict(infile, headerlist, HDU=0):
    """
    Given a filename (with path), return a dict of the desired header
    keywords.
    """
    item = {}
    bname = basename(infile)

    # NOTE: This isn't just called 'filename' beacuse I didn't want to risk
    #   it getting clobbered if the user was actually interested in
    #   a FITS keyword called "FILENAME" at some point in the future...
    item['PhysicalFilename'] = bname
    try:
        hed = pyf.getheader(infile, ext=HDU)
        failed = False
    except:
        failed = True

    for key in headerlist:
        if failed is False:
            try:
                item[key] = hed[key]
            except:
                item[key] = ''
        else:
            item[key] = ''

    return item


class FITSKeyWordDialog(QtWidgets.QDialog, fkwp.Ui_FITSKWDialog):
    def __init__(self, parent=None):
        super(FITSKeyWordDialog, self).__init__(parent)

        self.setupUi(self)

        # Hooks for the various buttons
        self.fitskw_add.clicked.connect(self.getkeywordfromuser)
        self.fitskw_remove.clicked.connect(self.removekeywordfromlist)
        self.fitskw_model = self.fitskw_listing.model()
        self.fitskw_model.layoutChanged.connect(self.reorderedheadlist)

        self.fitskw_savelist.clicked.connect(self.kwsavelist)
        self.fitskw_loadlist.clicked.connect(self.kwloadlist)

        self.fitskw_dialogbutts.accepted.connect(self.accept)
        self.fitskw_dialogbutts.rejected.connect(self.reject)

        self.utcnow = self.parent().utcnow

        # Grab a few things from the parent widget to use here
        self.headers = self.parentWidget().headers
        self.fitshdu = self.parentWidget().fitshdu
        self.reorderkwwidget()
        self.updateheadlist()

    def reorderedheadlist(self):
        self.updateheadlist()
        self.txt_fitskw_status.setText("Unsaved Changes!")

    def kwsavelist(self):
        self.selectKWFile(kind='save')
        if self.kwname != '':
            try:
                f = open(self.kwname, 'w')
                writer = csv.writer(f)
                rowdata = []
                for column in range(len(self.headers)):
                    if column is not None:
                        rowdata.append(str(self.headers[column]))
                    else:
                        rowdata.append('')
                writer.writerow(rowdata)
                f.close()
                statusline = "File Written: %s" % str(self.kwname)
                self.txt_fitskw_status.setText(statusline)
            except Exception as why:
                print(str(why))
                self.txt_fitskw_status.setText("ERROR WRITING TO FILE!")

    def kwloadlist(self):
        self.selectKWFile(kind='load')
        if self.kwname != '':
            try:
                f = open(self.kwname, 'r')
                self.headers = []
                reader = csv.reader(f)
                for row in reader:
                    self.headers.append(row)
                statusline = "File Loaded: %s" % str(self.kwname)
                self.txt_fitskw_status.setText(statusline)
            except Exception as why:
                print(str(why))
                self.txt_fitskw_status.setText("ERROR READING THE FILE!")
            finally:
                f.close()
                # Loading could have left us with a list of lists, so flatten
                self.headers = list(itertools.chain(*self.headers))
                self.reorderkwwidget()

    def reorderkwwidget(self):
        self.fitskw_listing.clear()
        for key in self.headers:
            self.fitskw_listing.addItem(QtWidgets.QListWidgetItem(key))

    def getkeywordfromuser(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Add Keyword",
                                                  "New Keyword:",
                                                  QtWidgets.QLineEdit.Normal,
                                                  QtCore.QDir.home().dirName())
        text = str(text)
        if ok and text != '':
            text = text.strip()
            text = text.upper()
            self.fitskw_listing.addItem(QtWidgets.QListWidgetItem(text))
            self.reorderkwwidget()
            self.updateheadlist()
            self.txt_fitskw_status.setText("Unsaved Changes!")

    def removekeywordfromlist(self):
        for it in self.fitskw_listing.selectedItems():
            self.fitskw_listing.takeItem(self.fitskw_listing.row(it))
        self.txt_fitskw_status.setText("Unsaved Changes!")
        self.updateheadlist()
        self.reorderkwwidget()

    def selectKWFile(self, kind='save'):
        """
        Spawn the file chooser diaglog box and return the result, attempting
        to both open and write to the file.

        """
        defaultname = "KWList_" + self.parentWidget().instrument +\
            self.utcnow.strftime("_%Y%m%d.txt")
        if kind == 'save':
            self.kwname = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                "Save File",
                                                                defaultname)[0]
        if kind == 'load':
            self.kwname = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                "Load File",
                                                                defaultname)[0]

    def updateheadlist(self):
        self.headers = []
        for j in range(self.fitskw_listing.count()):
            ched = self.fitskw_listing.item(j).text()
            self.headers.append(str(ched))
        self.headers = [hlab.upper() for hlab in self.headers]


class LDTObslogGeneratorApp(QtWidgets.QMainWindow, logp.Ui_MainWindow):
    """
    Main class driving the GUI.
    """
    def __init__(self):
        # Since the LDTObslogGeneratorPanel file will be overwritten each time
        #   we change something in the design and recreate it, we will not be
        #   writing any code in it, instead we'll create a new class to
        #   combine with the design code
        super(self.__class__, self).__init__()

        # This is defined in LDTObslogGeneratorPanel.py file automatically;
        #   It sets up layout and widgets that are defined
        self.setupUi(self)

        # Set up locale ephemeris information
        self.ldt = ephem.Observer()
        self.ldt.lat, self.ldt.lon = "34.7443", "-111.4223"
        self.ldt.elevation = 2361

        # Some constants/tracking variables and various defaults
        self.successparse = False
        self.outputname = ''
        self.localtz = pytz.timezone('America/Phoenix')

        # Is a list really the best way of handling this? Don't know yet.
        self.startdatalog = False
        self.data_current = []
        self.data_previous = []
        self.datatable = []
        self.datafilenames = []
        self.logoutnme = ''
        self.headers = []
        self.fitshdu = 0

        # Set tracker variable for instrument
        self.selected_instrument = self.datalog_instrumentselect.currentText()

        # The inst_list attribute will be a dictionary of dictionaries
        self.inst_list = {}
        for inst in ['LMI','DeVeny','NIHTS','RC1','RC2']:
            self.inst_list[inst] = {}

        # NOTE: This setup presumes we might want to have additional dictionary
        #  entries for each instrument beyond 'headers'.  If not, then the
        #  structure of this can simply be one dictionary with the instrument
        #  as the key and the list of header keywords as the value.

        # Create the list of applicable headers for each instrument
        self.inst_list['LMI']['headers'] = ['date-obs','object','obstype',
                                            'telra','teldec','telalt','telaz',
                                            'airmass','exptime','filters',
                                            'ccdsum','telfocus','rotframe',
                                            'skyvpa']
        self.inst_list['DeVeny']['headers'] = ['date-obs','object','obstype',
                                            'telra','teldec','telalt','telaz',
                                            'airmass','exptime','grating',
                                            'grangle','slitasec','collfoc',
                                            'filtrear','lampcal','telfocus',
                                            'rotframe','rotangle','skyvpa']
        self.inst_list['NIHTS']['headers'] = ['date-obs','object','obstype',
                                            'telra','teldec','telalt','telaz',
                                            'airmass','exptime','telfocus',
                                            'rotframe','rotangle','skyvpa']
        self.inst_list['RC1']['headers'] = ['date-obs','object','obstype',
                                            'telra','teldec','telalt','telaz',
                                            'airmass','exptime','telfocus',
                                            'rotframe','rotangle','skyvpa']
        self.inst_list['RC2']['headers'] = ['date-obs','object','obstype',
                                            'telra','teldec','telalt','telaz',
                                            'airmass','exptime','telfocus',
                                            'rotframe','rotangle','skyvpa']

        # Set self.instrument and self.headers attributes
        self.set_instrument_attrs()

        # Things are easier if the keywords are always in CAPS
        self.headers = [each.upper() for each in self.headers]
        # The addition of the NOTES column happens in here
        self.updatetablecols()

        # Looks prettier with this stuff
        self.table_datalog.resizeColumnsToContents()
        self.table_datalog.resizeRowsToContents()

        # Actually show the table
        self.table_datalog.show()

        # Data Log Hooks
        self.datalog_opendir.clicked.connect(self.selectDir)
        self.datalog_savefile.clicked.connect(self.selectLogOutputFile)
        self.datalog_forcewrite.clicked.connect(self.writedatalog)
        self.datalog_forceupdate.clicked.connect(self.updateDatalog)
        self.datalog_editkeywords.clicked.connect(self.spawnkwwindow)
        self.datalog_addrow.clicked.connect(self.adddatalogrow)
        self.datalog_deleterow.clicked.connect(self.deldatalogrow)
        # Add an action that detects when a cell is changed by the user
        #  in table_datalog!

        # Generic timer setup stuff
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showlcd)
        timer.start(500)
        self.showlcd()


    def set_instrument_attrs(self):
        # The self.instrument and self.headers attributes are set based on the
        #  currently selected instrument
        self.instrument = self.selected_instrument
        self.headers = self.inst_list[self.selected_instrument]['headers']



    def spawnkwwindow(self):
        window = FITSKeyWordDialog(self)
        result = window.exec_()
        if result == 1:
            self.fitshdu = np.int(window.fitskw_hdu.value())
            self.newheaders = window.headers
            print(self.newheaders)

            # NOT WORKING YET
            # Update the column data itself if we're actually logging
            if self.startdatalog is True:
                self.repopulateDatalog(rescan=False)

        # Explicitly kill it
        # del window

    def updatetablecols(self):
        # This always puts the NOTES col. right next to the filename
        self.table_datalog.insertColumn(0)

        # Add the number of columns we'll need for the header keys given
        for hkey in self.headers:
            colPosition = self.table_datalog.columnCount()
            self.table_datalog.insertColumn(colPosition)
        self.table_datalog.setHorizontalHeaderLabels(['NOTES'] + self.headers)

    def selectDir(self):
        dtxt = 'Select Data Directory'
        self.datalogdir = QtWidgets.QFileDialog.getExistingDirectory(self, dtxt)
        if self.datalogdir != '':
            self.txt_datalogdir.setText(self.datalogdir)
            self.startdatalog = True

    def selectLogOutputFile(self):
        """
        Spawn the file chooser diaglog box and return the result, attempting
        to both open and write to the file.

        """
        defaultname = "DataLog_" + self.utcnow.strftime("%Y%m%d.csv")
        self.logoutnme = QtWidgets.QFileDialog.getSaveFileName(self,
                                                               "Save File",
                                                               defaultname)[0]

        if self.logoutnme != '':
            self.txt_datalogsavefile.setText("Writing to: " +
                                             basename(str(self.logoutnme)))

    def update_times(self):
        """
        Grab the current UTC and local timezone time, and populate the strings.
        We need to throw away microseconds so everything will count together,
        otherwise it'll be out of sync due to microsecond delay between
        triggers/button presses.
        """
        self.utcnow = datetime.datetime.utcnow()
        self.utcnow = self.utcnow.replace(microsecond=0)
        self.utcnow_str = self.utcnow.strftime(' %H:%M:%S UTC')
        self.utcnow_datetimestr = self.utcnow.strftime('%m/%d/%Y %H:%M:%S $Z')
        self.utcnow_datestr = self.utcnow.strftime('%Y-%m-%d')

        # Safest way to sensibly go from UTC -> local timezone...?
        self.localnow = self.utcnow.replace(
            tzinfo=pytz.utc).astimezone(self.localtz)
        self.localnow_str = self.localnow.strftime(' %-I:%M:%S %p')
        self.localnow_datetimestr = self.localnow.strftime(
            '%m/%d/%Y %H:%M:%S')
        self.localnow_datestr = self.localnow.strftime('%a %h %d, %Y')

        # Compute Local Sunrise / Sunset times, Sun Elevation status
        self.ldt.date = ephem.Date(self.utcnow)
        self.sun = ephem.Sun(self.ldt)
        self.sunel_str = f"Elevation: {self.sun.alt / np.pi * 180.:.2f}º"
        self.sunaz_str = f"Azimuth: {self.sun.az}"
        self.localsunrise = ephem.localtime(
            self.ldt.previous_rising(ephem.Sun()))
        self.localsunrise_str = self.localsunrise.strftime('%Y-%m-%d %H:%M:%S')
        self.localsunset = ephem.localtime(self.ldt.next_setting(ephem.Sun()))
        self.localsunset_str = self.localsunset.strftime('%Y-%m-%d %H:%M:%S')
        if (sun_alt := self.sun.alt / np.pi * 180.) > 0:
            self.skystat_str = "Daylight"
        elif sun_alt > -6:
            self.skystat_str = "Civil Twilight"
        elif sun_alt > -12:
            self.skystat_str = "Nautical Twilight"
        elif sun_alt > -18:
            self.skystat_str = "Astronomical Twilight"
        else:
            self.skystat_str = "Dark"


    def showlcd(self):
        """
        The main loop for the code.

        Contains the clock logic code for all the various timers.

        Since the times were converted to local elsewhere,
        we ditch the tzinfo to make everything naive to subtract easier.
        """
        # Update the current local/utc times before computing timedeltas
        self.update_times()

        self.txt_utcdate.setText(self.utcnow_datestr)
        self.txt_localdate.setText(self.localnow_datestr)
        self.txt_utc.setText(self.utcnow_str)
        self.txt_localtime.setText(self.localnow_str)
        self.txt_sunel.setText(self.sunel_str)
        self.txt_skystat.setText(self.skystat_str)

        # If the selected instrument is changed, update the columns
        if (sel_inst := self.datalog_instrumentselect.currentText()) != \
            self.selected_instrument:
            # print(sel_inst)
            self.selected_instrument = sel_inst
            self.set_instrument_attrs()
            # NEED TO FIGURE OUT HOW TO REPOPULATE THE TABLE WITHOUT CRASHING...
            self.repopulateDatalog()
   
        if self.startdatalog is True and \
           self.datalog_autoupdate.isChecked() is True:
            if self.utcnow.second % self.datalog_updateinterval.value() == 0:
                self.updateDatalog()
                # print self.datatable

    def adddatalogrow(self):
        rowPosition = self.table_datalog.rowCount()
        self.table_datalog.insertRow(rowPosition)
        self.datafilenames.append('--> ')
        # Actually set the labels for rows
        self.table_datalog.setVerticalHeaderLabels(self.datafilenames)
        self.writedatalog()

    def deldatalogrow(self):
        bad = self.table_datalog.currentRow()
        # -1 means we didn't select anything
        if bad != -1:
            # Clear the data we don't need anymore
            del self.datafilenames[bad]
            self.table_datalog.removeRow(self.table_datalog.currentRow())

            # Redraw
            self.table_datalog.setVerticalHeaderLabels(self.datafilenames)
            self.writedatalog()

    def repopulateDatalog(self, rescan=False):
        """
        After changing the column ordering or adding/removing keywords,
        use this to redraw the table in the new positions.
        """
        # Disable fun stuff while we update
        self.table_datalog.setSortingEnabled(False)
        self.table_datalog.horizontalHeader().setSectionsMovable(False)
        self.table_datalog.horizontalHeader().setDragEnabled(False)
        self.table_datalog.horizontalHeader().setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)

        thedlist = ['NOTES'] + self.headers

        # First, grab the data
        tablist = []
        for n in range(0, self.table_datalog.rowCount()):
            rowdata = {}
            for m, hkey in enumerate(thedlist):
                if rescan is True:
                    # Need to somehow remap the basename'd row label to the
                    #   original listing of files (with path) to go rescan
                    fname = ''
                    rowdata = headerDict(fname, self.headers,
                                         HDU=self.fitshdu)
                else:
                    rdat = self.table_datalog.item(n, m)
                    if rdat is not None:
                        rowdata[hkey] = rdat.text()
                    else:
                        rowdata[hkey] = ''
            tablist.append(rowdata)

        # Clear out the old data, since we could have rearranged columns
        self.table_datalog.clear()

        # Actually assign the new headers
        self.headers = self.newheaders

        # Update with the new number of colums
        self.table_datalog.setColumnCount(len(self.headers) + 1)

        # Update with the new column labels
        self.updatetablecols()

        # Actually set the labels for rows
        self.table_datalog.setVerticalHeaderLabels(self.datafilenames)

        # Create the data table items and populate things
        #   Note! This is for use with headerDict style of grabbing stuff
        for n, row in enumerate(tablist):
            for m, hkey in enumerate(self.headers):
                print(n, m, row, hkey, row[hkey])
                newitem = QtWidgets.QTableWidgetItem(str(row[hkey]))
                self.table_datalog.setItem(n, m+1, newitem)

        # Resize to minimum required, then display
        self.table_datalog.resizeRowsToContents()

        # Seems to be more trouble than it's worth, so keep this commented
        # self.table_datalog.setSortingEnabled(True)

        # Reenable fun stuff
        self.table_datalog.horizontalHeader().setSectionsMovable(True)
        self.table_datalog.horizontalHeader().setDragEnabled(True)
        self.table_datalog.horizontalHeader().setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        # Looks prettier with this stuff
        self.table_datalog.resizeColumnsToContents()
        self.table_datalog.resizeRowsToContents()

        self.table_datalog.show()

        # Should add this as a checkbox option to always scroll to bottom
        #   whenever a new file comes in...
        self.table_datalog.scrollToBottom()

    def updateDatalog(self):
        """
        General notes:
          glob.glob returns a randomly ordered result, so that can lead
            to jumbled results if you just use it blindly. Sort by modification
            time to get a sensible listing.
            (can't use creation time cross-platform)
        """
        # Get the current list of FITS files in the location
        if self.instrument == 'HAWCFlight':
            self.data_current = glob.glob(str(self.datalogdir) + "/*.grabme")
        elif self.instrument == 'FIFI-LS':
            curdata = []
            for root, dirnames, filenames in walk(str(self.datalogdir)):
                for filename in fnmatch.filter(filenames, '*.fits'):
                    curdata.append(join(root, filename))
            self.data_current = curdata
        else:
            self.data_current = glob.glob(str(self.datalogdir) + "/*.fits")

        # Correct the file listing to be ordered by modification time
        self.data_current.sort(key=getmtime)

        # Ok, lets try this beast again.
        #   Main difference here is the addition of a basename'd version
        #   of current and previous data. Maybe it's a network path bug?
        #   (grasping at any and all straws here)
        bncur = [basename(x) for x in self.data_current]

        if self.instrument == "HAWCFlight":
            bnpre = [basename(x)[:-4] + 'grabme' for x in self.datafilenames]
        else:
            bnpre = [basename(x) for x in self.datafilenames]

        if len(bncur) != len(bnpre):
            self.datanew = []
            # Make the unique listing of old files
            s = set(bnpre)

            # Compare the new listing to the unique set of the old ones
            #   Previous logic was:
            # diff = [x for x in self.data_current if x not in s]
            # Unrolled logic (might be easier to spot a goof-up)
            diff = []
            idxs = []
            for i, x in enumerate(bncur):
                if x not in s:
                    idxs.append(i)
                    diff.append(x)

            # Capture the last row position so we know where to start
            self.lastdatarow = self.table_datalog.rowCount()

            print("PreviousFileList:", bnpre)
            print("CurrentFileList:", bncur)
            # Actually query the files for the desired headers
            for idx in idxs:
                # REMEMBER: THIS NEEDS TO REFERENCE THE ORIGINAL LIST!
                if self.instrument == "HAWCFlight":
                    realfile = self.data_current[idx][:-6] + 'fits'
                else:
                    realfile = self.data_current[idx]
                print("Newfile: %s" % (realfile))
                # Save the filenames
                self.datafilenames.append(basename(realfile))
                # Add number of rows for files to go into first
                rowPosition = self.table_datalog.rowCount()
                self.table_datalog.insertRow(rowPosition)
                # Actually get the header data
                theData = headerDict(realfile, self.headers, HDU=self.fitshdu)
                # self.allData.append(theData)
                self.datanew.append(theData)

            self.setTableData()
            self.writedatalog()

    def setTableData(self):
        if len(self.datanew) != 0:
            # Disable fun stuff while we update
            self.table_datalog.setSortingEnabled(False)
            self.table_datalog.horizontalHeader().setSectionsMovable(False)
            self.table_datalog.horizontalHeader().setDragEnabled(False)
            self.table_datalog.horizontalHeader().setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)

            # Actually set the labels for rows
            self.table_datalog.setVerticalHeaderLabels(self.datafilenames)

            # Create the data table items and populate things
            #   Note! This is for use with headerDict style of grabbing stuff
            for n, row in enumerate(self.datanew):
                for m, hkey in enumerate(self.headers):
                    newitem = QtWidgets.QTableWidgetItem(str(row[hkey]))
                    self.table_datalog.setItem(n + self.lastdatarow,
                                               m+1, newitem)

            # Resize to minimum required, then display
            # self.table_datalog.resizeColumnsToContents()
            self.table_datalog.resizeRowsToContents()

            # Seems to be more trouble than it's worth, so keep this commented
            # self.table_datalog.setSortingEnabled(True)

            # Reenable fun stuff
            self.table_datalog.horizontalHeader().setSectionsMovable(True)
            self.table_datalog.horizontalHeader().setDragEnabled(True)
            self.table_datalog.horizontalHeader().setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

            # Looks prettier with this stuff
            self.table_datalog.resizeColumnsToContents()
            self.table_datalog.resizeRowsToContents()

            self.table_datalog.show()

            # Should add this as a checkbox option to always scroll to bottom
            #   whenever a new file comes in...
            self.table_datalog.scrollToBottom()
        else:
            print("No new files!")

    def writedatalog(self):
        if self.logoutnme != '':
            try:
                f = open(self.logoutnme, 'w')
                writer = csv.writer(f)
                # Write the column labels first...assumes that the
                #   filename and notes column are first and second
                clabs = ['FILENAME', 'NOTES'] + self.headers
                writer.writerow(clabs)
                for row in range(self.table_datalog.rowCount()):
                    rowdata = []
                    rowdata.append(self.datafilenames[row])
                    for column in range(self.table_datalog.columnCount()):
                        item = self.table_datalog.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
                f.close()
            except Exception as why:
                print(str(why))
                self.txt_datalogsavefile.setText("ERROR WRITING TO FILE!")


def main():
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("./SOFIACruiseTools/resources/fonts/digital_7/digital-7_mono.ttf")
    form = LDTObslogGeneratorApp()
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':
    main()
