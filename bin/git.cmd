@echo off
setlocal EnableExtensions
set "REAL_GIT=C:\Program Files\Git\cmd\git.exe"

rem Only protect this docs repo (not other git repos on PATH)
set "REPO_ROOT="
for /f "delims=" %%i in ('"%REAL_GIT%" rev-parse --show-toplevel 2^>nul') do set "REPO_ROOT=%%i"
if /I not "%REPO_ROOT%"=="C:/work/projects/wchat/docs" if /I not "%REPO_ROOT%"=="C:\work\projects\wchat\docs" (
  "%REAL_GIT%" %*
  exit /b %ERRORLEVEL%
)

if /I "%~1"=="pull" goto :block
if /I "%~1"=="merge" goto :block
if /I "%~1"=="rebase" goto :block
if /I "%~1"=="reset" (
  echo %* | findstr /I /C:"--hard" >nul && goto :block
)

"%REAL_GIT%" %*
exit /b %ERRORLEVEL%

:block
if "%ALLOW_PULL%"=="1" (
  "%REAL_GIT%" %*
  exit /b %ERRORLEVEL%
)
echo.
echo [blocked] Local docs is the source of truth.
echo Remote must NOT overwrite c:\work\projects\wchat\docs
echo.
echo Daily workflow:
echo   git add -A
echo   git commit -m "msg"
echo   git push origin main
echo.
echo Emergency only (explicit overwrite):
echo   set ALLOW_PULL=1
echo   git pull
echo.
exit /b 1
