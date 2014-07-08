kinesin
=======
Detects steps in kinesin stepping data.

Asks for folder in which data is stored. This contains csv files called 'timestamp'.csv with data in form column[0]=time, col[1] = position, col[2]=filtered position. Folder also contains noise file for each data file called 'timestamp'noise.txt with data from unbound state near run in form col[9]=position (due to the way the Labview code saves the data, could be changed to be more sensible). Give path for these folders, no final backslash, when asked.

Asks for threshold for the t test data. Typical is 10.

Asks for width of data samples to be compared using t test. Typical is 1000.
