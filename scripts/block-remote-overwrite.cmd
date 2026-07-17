@echo off
if "%ALLOW_PULL%"=="1" exit /b 0
echo [blocked] Local docs is source of truth. Do NOT pull (avoids remote overwrite).
echo Daily: git add / commit / push origin main
echo Emergency overwrite: set ALLOW_PULL=1 ^&^& git pull
echo   or: git fetch origin ^&^& git reset --hard origin/main
exit /b 1
