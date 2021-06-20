# CCTV_Cam
Final Year Project CCTV Face Recognition and Working Pattern recognition and anomaly detection

this project is presented in two modules.

## ML
the first section is all contained within the 'ML' directory
this section or module starts the Machine learning backend that collects images or frames from each of the configured cameras and the runs over them with two ML models to first find the faces within a given fram and then the second will attempt to recognise the face in the cropped image. 

## Web Portal
the second section of the project is in a standard Django directory strucutre under 'portal'
this section takes the footage provided by the backend and then displays it to the users on a webpage. future development will include a browser for old footage within the retention period and also addition and intergration of user accounts to record who alerts should be sent to. 
