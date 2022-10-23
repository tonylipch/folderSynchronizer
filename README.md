<h1>This test task was developed for <b>Veeam company</b></h1> 

<h2><b>The purpose of this task was:</b> </h2>

implement a program that synchronizes two folders: source and replica. The
program should maintain a full, identical copy of source folder at replica folder.

<h5>During development, I applied common libraries for working with halves and setting up a schedule for running the script.  The program meets all of the customer's requirements.<h5>

<h1>Terms of use</h1>

The program is easy to use. The principle is that the script tracks changes in the replica folder in the background and compares them with the source folder. If there are any inconsistencies with the source directory, the program <b>brings everything into a single view.</b>
  
 
  Syntax for program startup is : <b>python synchronizer.py "your source directory" "your dest dirrectory" "m(minute) h(hour) d(moth) m(month) d(week)" </b>
  
  Example : python synchronizer.py "C:\source" "C:\replica" "5 4 * * 4" . This script will be execute every  Thursday at 4:05am .





                                  
                                 
