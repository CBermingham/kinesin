kinesin
=======
Detects steps in kinesin stepping data.

Asks for folder in which data is stored. This contains csv files called 'timestamp'.csv with data in form column[0]=time, col[1] = position, col[2]=filtered position. Folder also contains noise file for each data file called 'timestamp'noise.txt with data from unbound state near run in form col[9]=position (due to the way the Labview code saves the data, could be changed to be more sensible). Give path for these folders, no final backslash, when asked.

Asks for threshold for the t test data. Typical is 10.

Asks for width of data samples to be compared using t test. Typical is 1000.


Outputs:

2 graphs for each data file: 
-trace.png shows the filtered position data against time and the steps overlayed onto it. Use this to see if threshold and width settings are ok. 
-ttest.png shows the t test values for each time and the position of the threshold.

2 csv files for each data file:
-stepdata.csv contains the position in time and displacement, length in time and distance, force and direction of each step. This is used in the stepanalysis.py program to analyse the data from lots of runs.
-trace.csv contains the time and filtered position data for replotting if needed.

All the files and graphs are preceded in name by the timestamp of the raw data file from which that are made.



