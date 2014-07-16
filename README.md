kinesin
=======
Detects steps in kinesin stepping data.

Use programs in this order:

1. t_value_finder.py
2. set_threshold.py
3. stepanalysis.py

------------------------------------------------------------------------------------------
1. Inputs

Asks for folder in which data is stored. This contains csv files called 'timestamp'.csv with data in form column[0]=time, col[1] = position, col[2]=filtered position. Folder also contains noise file for each data file called 'timestamp'noise.txt with data from unbound state near run in form col[9]=position (due to the way the Labview code saves the data, could be changed to be more sensible). Give path for these folders, no final backslash, when asked.

Asks for width of data samples to be compared using t test. Typical is 1000.

1. Method

Sets up arrays of data around each point to compare using the t-test and returns the t value for each point.

Adjusts the size of the position and filtered position data so that it only includes points for which a t value has been calculated.

Runs through all files in folder.

1. Outputs

A csv file containing columns with headings containing time, t values, filtered position data and raw position data for each point. Saved in folder for analysed data as 'timestamp'_tvalues.csv. Does this for each data file.

A text file containint a timestamp from when the program first started running, the location of the files analysed and the names of the files analysed. Saved as 'current'date_time'_report.txt in the analysed data folder.

------------------------------------------------------------------------------------------

2. Inputs

Asks for a timestamp_tvalues file created using t_value_finder.py. 

Asks for an initial threshold value to try.

2. Method

Finds the t values over the threshold, calculated step position by finding the maximum t value of a sequence of points over the threshold. Plots a graph of filtered data with steps overlayed and shows graph.

Can then see if threshold is ok. Close graph and type n to try another threshold. New step values are calculated and plotted. Keep trying until satisfied with threshold then type y when asked.

2. Outputs

A csv file containing data that was plotted last, the time, t values, filtered position and unfiltered position. This is so that it can be plotted again if necessary. Saved as 'timestamp'_T'threshold'_plotdata.csv in the analysed data folder.

A csv file containing the step data. This is the Time in s, Length in s, Average position in m, Length in nm, Average force in pN and f/b/d for forward/back/detachment. Saved as 'timestamp'_T'threshold'_stepdata.csv in the analysed data folder.

A png image of the graph displayed to set the threshold. Shows the filtered data and the overlayed steps. Saved as 'timestamp'_T'threshold'.csv in the analysed data folder.


