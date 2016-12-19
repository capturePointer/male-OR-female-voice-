rem Script that will process your train files into scipy.io.wavfile.readible form

@echo off

set source=train
set dest=%USERNAME%_Processed
echo i will process files from %source%\* to %dest%\*

:: cd %~dp0
if not exist %dest% mkdir %dest%

echo
echo ARE YOU READY?
pause

@echo on

for /r %%f in (.\%source%\*) do (
::echo %%f
::pause

sox %%f -b 16 .\%dest%\%%~nxf remix 
sox %%f -n stats
sox %%f .\%dest%\%%~nxf -n stats 
pause
::sox %%f  32 .\%dest%\%%~nxf 
::sox %%f .\%dest%\%%~nxf remix 1-2
)
pause