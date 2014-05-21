Module 6
Fill file 'initial_data.txt' in UTF-8, where
script_num is number of script (required for all scripts).
script_num can contain several numbers of scripts, separated by a space.
Tabs are between names and numbers.
Then run the executable file 'setup.py' (also UTF-8)

Example of file 'initial_data.txt':

script_num	1 2 3 4 5 6 7
wavelength	0.7
azimuth_angle	0
cone_angle	90

SCRIPT1:
The angular distribution of radiation coming from the structure normalized by the 
spectrum of the radiation source for set wavelength

initial data:
wavelength

input files:
far.d

output files:
angular.txt
angular_xy.txt
pic.png
intensity.html

SCRIPT2:
The dependence of the intensity released radiation on the polar angle

initial data:
wavelength

input files:
far.d

output files:
intensity_polar_angle.txt
intensity_polar_angle.xml

SCRIPT3:
The dependence of the intensity on the polar angle for a given azimuth angle

initial data:
wavelength
azimuth angle

input files:
far.d

output files:
intensity_azimuth_angle.txt
intensity_azimuth_angle.xml

SCRIPT4:
Spectral efficiency of light emission

initial data:
cone angle

input files:
if cone_angle = 90:
spectra.d
power.d

if cone_angle < 90:
far.d
power.d

output files:
efficiency.txt
efficiency.xml

SCRIPT5:
The passive optical characteristics of the structure

input files:
rta.d

output files:
tra.txt
tra.xml

SCRIPT6:
The electromagnetic field distribution in the device

initial data:
wavelength

input files:
detectors.d

output files:
field_intensity.txt

SCRIPT7:
Current-voltage characteristic of OLED and SC

input files:
j_sc.d for Solar cells
j.d for OLED
or one of them

output files:
CVC_sc.txt for Solar cells
cvc_sc.xml for solar cells
cvc.xml for OLED

SCRIPT 8:
The distribution of charge carriers excited states and currents
initial data:
voltage

input files:
mV.d where V is number (for example, m0.05.d)

output files:
xJnJp.txt
xnp.txt
xST.txt
xJnJp.xml
xnp.xml
xST.xml

SCRIPT 9:
Calculation of chromaticity temperatura

initial data: cone angle

input files:
spectr.dat
far.d 
power.d
chrom_curves.txt

output files:
chromaticity_temperatura.txt

SCRIPT 11 and SCRIPT 12:
Calculation of dependence of the efficiency on the voltage and dependence of the heat losses on the voltage

initial data: cone angle

input files:
j.d
R.d
spectr.dat
spectra.d
far.d
power.d

output files:
efficacy.xml
heat_losses.xml