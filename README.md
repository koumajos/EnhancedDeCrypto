# Enhanced DeCrypto
Repository for code of experiments for the paper Enhancing DeCrypto: Finding Cryptocurrency Miners based on Periodic Behavior

The following table contains description of files:

| FILE                             | Description                 |
|:--------------------------------:|:---------------------------:|
| results/                         | Folder containing results of ml_periodicity.sh script. |
| Ports.csv                        | The Ports.csv contains the well-known and registered ports of transport layer of TCP/IP model.   |
| add_dependency.py                | The add_dependency.py contains function for compute the ID of Network dependency.   |
| create_time_series_from_flow.py  | The create_time_series_from_flow.py creates the Flow Time Series (FTS) from IP flows on input.  |
| create_time_series_from_flow.sh  | The create_time_series_from_flow.sh run add_dependency.py to enhance the IP flows by ID dependency and then run create_time_series_from_flow.py  to create Flow Time Series.            |
| final_ml_periodicity.ipynb       | The final_ml_periodicity.ipynb performs the example of ML peridoicity for one setting of Scargles Significance Test (SST) and time interval of creating Flow Time Series.     |
| merge_ts.py                      | The merge_ts.py merges the Flow Time Series in specific time interval which contains the common used ports which are not well-known or registered.         |
| ml_periodicity.py                | The ml_periodicity.py contains the ML pipeline whoch is runned for K times.          |
| ml_periodicity.sh                | The ml_periodicity.sh run ml_periodicity.py for each setting of SST test.  |
| new_model.py                     | The new_model.py contains model of for perform peridoicity detection and feature mining.  |
| perform.sh                       | The perform.sh run all pipeline for build FTS, merge FTS, and perform epridoicity detection and feature mining.  |
 
 
 Copyright &copy; 2023, Czech Technical University in Prague, CESNET a.l.e., Josef Koumar (koumajos@fit.cvut.cz), Richard Plný (plnyrich@fit.cvut.cz), Tomáš Čejka (cejkat@cesnet.cz)
