pip install pyinstaller

pyinstaller --onefile -w tabel_calendar_load.py

xcopy %~dp0dist\tabel_calendar_load.exe %~dp0 /Y

del tabel_calendar_load.spec /q
rmdir %~dp0build /S /Q
rmdir %~dp0dist /S /Q
rmdir %~dp0__pycache__ /S /Q

pause