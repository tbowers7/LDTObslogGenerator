LDTObslogGenerator
====================================

![logo](Tools/resources/images/Lore.png)

Quickstart:
===========
- Change 'self.headers' to the FITS keyword headers you want.
- Change 'self.instrument' to something OTHER than 'HAWCFlight' to search for 
.FITS files normally; 'HAWCFlight' is a workaround for HAWC+ specifically.
- Make sure the flight plan file is readable before flight; see below.
- FITS keyword panel is notional at this time and doesn't change anything.
- python SOFIACruiseDirector.py

Slowstart:
===========
Python packages required:
    python >= 2.7 (should work ok in Python >= 3.6)
    pytz, numpy, scipy, astropy, PyQt5

NOTE: If you use anaconda, you're probably already set.

Start it by:
python SOFIACruiseDirector.py

The other files need to be in the same directory but you shouldn't ever have to
touch them.

Usage:
Most buttons should be self explanatory.  'Open Flight Plan' will ask you for a
.mis file to load in and set parameters in the GUI accordingly.

But!  If you have a non-siderial target, you'll have to remove the extra line
underneath the "Target: ..." line in the leg header.  For example, a recent
FLITECAM flight plan contained.

Leg 8 (Asteroid with naif_id =2000016) Start: 09:03:38     Leg Dur: 01:02:48   Req. Alt: 42000 ft  
ObspID: 02_0066     Blk: OB_02_0066_07  Priority: C         Obs Dur: 00:52:48   
Target: Asteroid with naif_id =2000016 RA: 05h27m19.65s    Dec: 19d26m56.0s    Equinox: J2000.0    
NAIF ID: 2000016    
Elev: [37.1, 45.8]  ROF: [331.4, 326.5] rate: [-0.09, -0.07] deg/min  Moon Angle: 14

That "NAIF ID: ..." line is the one that has to go.  I should probably add a
check to do that automatically but I've obviously haven't.

Recent (2016) flight plans now also change the way departure/arrival legs are 
denoted; make sure that the ( ) next to "Leg N" say "Departure" or "Arrival" 
rather than the waypoint names (such as "ROSIN").

The FITS keyword panel is functional within itself, but at this point
purely aspirational and does nothing of use.  I struggled in my head with how
to deal with changing keywords if the log is already written/started, or
at least changing the order of the keywords.  That struggle never was resolved,
so it's non-functional.  So if you want to change the FITS headers that are 
queried, look at SOFIACruiseDirector.py:229 and change what you need there.  It
should be commented enough to read through briefly and at least find the
relevant section if you need/want to tinker with something but that varies
greatly since I wrote the bulk of this while transitioning to a night schedule
in the day or two before flights.

Also, change self.instrument to what you'd like.  The dropdown menu to choose
the instrument is there but disconnected.  'HAWCFlight' is a special
case that queries/looks for files in the specific way to get around how
HAWC+ writes fits files

It works best if you "Choose Output Filename" for the Cruise Director Log tab
before you put anything in it to make sure your first comments are saved.
Additionally, the "Data Log Output" file will only be written when new files
arrive in the list.  So if you set the output file first, then point it to the
directory, then it'll be guaranteed to write to the file the first run through.
Any notes that you add won't be added until it finds a new file and adds that
file to the list, which just needs some simple rewiring of the logic flow to
make that not a pain like that.

Description:
============
The main package is PyQt5, that handles all of the window and GUI things.  The
nice thing about that is there's a GUI for making GUIs, QtCreator, that offers
a drag-and-drop interface to do stuff.  Once you have your design you can use a
simple command-line tool to take that GUI output and turn it into a python file
that you can import into your project, and *then* and assign actions to all the
different buttons.  That keeps the GUI divorced from the actions so you can
move stuff around without having to actually change the meat of your code.

'SOFIACruiseDirectorPanel.ui' is the actual GUI design file,
'SOFIACruiseDirectorPanel.py' is the python automatically translated
equivalent, and 'SOFIACruiseDirector.py' is where all the actions/magic
happens.  There's an additional file 'newparse.py' that I wrote 
to read and parse .mis files into python structures that I rolled into this as
well since it was convenient.
