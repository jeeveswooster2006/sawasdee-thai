@echo off
rem Double-click to make the French course pictures (Coco the rooster) with ComfyUI + Flux.
rem First run: makes 4 versions of Coco to choose from. After Claude saves the chosen one
rem as courses\fr\art\mascot.png, run it again to make all 43 unit pictures.
rem It checks ComfyUI is running on the graphics card (not the processor's built-in graphics),
rem offers to fix that, then makes all 43 pictures into courses\fr\art\units. Safe to run again: finished
rem pictures are skipped.
rem To undo the graphics fix later: reg delete HKCU\Environment /v HIP_VISIBLE_DEVICES /f
setlocal EnableExtensions
title Making the French pictures
cd /d "%~dp0"

echo.
echo  ===============================================
echo    Making the French pictures (Coco)
echo  ===============================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo  Python isn't installed ^(the "py" command is missing^). Install Python 3.12 from python.org.
  goto end
)

echo  Getting the latest picture script...
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/jeeveswooster2006/sawasdee-thai/main/tools/art/generate_unit_art_comfyui.py' -OutFile 'tools\art\generate_unit_art_comfyui.py'; Write-Host '  Up to date.' } catch { Write-Host '  Could not download it - using the copy already here.' }"

:run
echo.
if exist "courses\fr\art\mascot.png" (
  py -3.12 tools\art\generate_unit_art_comfyui.py --course fr --all
) else (
  py -3.12 tools\art\generate_unit_art_comfyui.py --course fr --units fr-mascot --variants 4
)
set RESULT=%ERRORLEVEL%
if "%RESULT%"=="0" goto done
if "%RESULT%"=="2" goto nocomfy
if "%RESULT%"=="3" goto wronggpu
echo.
echo  Something went wrong. Copy everything in this window and paste it to Claude.
goto end

:nocomfy
echo.
echo  ComfyUI isn't running yet. Open ComfyUI, wait until it has finished loading,
echo  then press any key here.
pause >nul
goto run

:wronggpu
if defined HIP_VISIBLE_DEVICES goto stillwrong
echo.
echo  ComfyUI is using the little graphics chip built into your processor instead of
echo  your RX 7800 XT. I can fix that by telling Windows to only show ComfyUI the
echo  graphics card. ^(This sets HIP_VISIBLE_DEVICES=1 for your Windows account.^)
echo.
choice /c YN /m "  Fix it now"
if errorlevel 2 goto end
setx HIP_VISIBLE_DEVICES 1 >nul
set HIP_VISIBLE_DEVICES=1
echo.
echo  Done. Now:
echo    1. CLOSE ComfyUI completely ^(also right-click its icon by the clock and Quit, if it has one^).
echo       If you use the command-line ComfyUI, close that window and start it in a NEW window.
echo    2. Open ComfyUI again and wait until it has finished loading.
echo    3. Come back to this window and press any key.
pause >nul
goto run

:stillwrong
echo.
echo  ComfyUI is still on the built-in graphics chip. Make sure you closed ComfyUI
echo  completely and opened it again ^(restarting the PC also works^).
echo  If that doesn't help: Device Manager ^> Display adapters ^> right-click
echo  "AMD Radeon(TM) Graphics" ^> Disable device ^(only if your monitor cable goes into
echo  the graphics card^), then restart ComfyUI.
echo.
choice /c YN /m "  Try again now"
if errorlevel 2 goto end
goto run

:done
echo.
echo  All done! Opening the pictures folder...
start "" "%~dp0courses\fr\art\units"

:end
echo.
pause
