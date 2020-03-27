@echo off

call setEnv.bat
echo sakura="%sakuraHome%"
echo source="%fromHome%"
::  echo para = "%grepPara%"
echo output="%outputDir%"

set keywordFile=grepkeyword.txt
set string=""

setlocal enabledelayedexpansion

:: 1 keyword file check
if not exist %keywordFile% (
    echo --1-- keyword file is not exist
	pause
	exit
) else (
    echo --1-- keyword file exist
)

:: 2 create output file
set time=%date:~2,5%%date:~8,2%%date:~11,2%%time:~0,2%%time:~3,2%%time:~6,2%
set "time=%time: =%"
set outputFileName=%outputDir%\%time%

if not exist %outputFileName% (
    MD %outputFileName%
	echo --2-- create output file success
) else (
    echo --2-- output file already exist
	exit
)

:: 3. loop keywordFile by line
for /f "tokens=1-4 delims=," %%a in (%keywordFile%) do (
    set flag=%%a
	set file=%%b
	set mdir=%%c
	set str=%%d
	
	if "%%a" == "1" (
	    call:keywordGrep
	)
)

echo --4-- grep end;

:: functions 

:keywordGrep
    set outfile=%outputFileName%\%file%
	
	echo keyword="%str%" directory="%fromHome%" ooufile="%outfile%"
	if "%mdir%" == "-" (
	    echo %sakuraHome% -GREPMODE -GKEY="%str%" -GFILE="*.*" -GFOLDER="%fromHome%" -GCODE=99 -GOPT=SPRO > %outfile%
	) else (
	    echo %sakuraHome% -GREPMODE -GKEY="%str%" -GFILE="*.*" -GFOLDER="%fromHome%\%mdir%" -GCODE=99 -GOPT=SPRO > %outfile%
	)
goto:END

:END