:: mirror dist folder into
::   - desktop
::   - stavanger analysis folder
::   - norway analysis folder

title UPDATE DESKTOP
robocopy /mir "c:\Users\rarossi\git\yoshimi\Qt\ResultsVisualiser\dist" "C:\Users\rarossi\OneDrive - TECHNIPFMC\Desktop\Apps\src\ResultsVisualiser\dist"
::pause

title UPDATE STAVANGER 
robocopy /mir "c:\Users\rarossi\git\yoshimi\Qt\ResultsVisualiser\dist" "I:\Stavanger\02 STVR BU ManCom and Dept\05 - Engineering\051 Analysis\Apps\src\ResultsVisualiser\dist"
::pause

title UPDATE NORWAY
robocopy /mir "c:\Users\rarossi\git\yoshimi\Qt\ResultsVisualiser\dist\results_visualiser" "I:\Depts\Engineering\5_Disciplines\051_ Subsea Installation\orcaflex toolbox\apps\dist\results_visualiser"


pause
