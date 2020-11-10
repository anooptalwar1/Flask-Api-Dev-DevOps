cls
@echo off
cd %temp%
del %temp%\*.* /f /s /q 
for /D %%f in (%temp%\*) do rmdir "%%f" /s /q

del c:\windows\temp\*.* /f /s /q
for /D %%f in (c:\windows\temp\*) do rmdir "%%f" /s /q

del C:\Windows\Prefetch\*.* /f /s /q
for /D %%f in (C:\Windows\Prefetch\*) do rmdir "%%f" /s /q

del "C:\Users\%username%\AppData\Local\Microsoft\Windows\Temporary Internet Files\*.*" /f /s /q
for /D %%f in ("C:\Users\%username%\AppData\Local\Microsoft\Windows\Temporary Internet Files\*") do rmdir "%%f" /s /q

del "C:\Documents and Settings\%username%\Local Settings\Temporary Internet Files\*.*" /f /s /q
for /D %%f in ("C:\Documents and Settings\%username%\Local Settings\Temporary Internet Files\*") do rmdir "%%f" /s /q

RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 8
RunDll32.exe InetCpl.cpl,ClearMyTracksByProcess 2
cls
echo *********************** Operation Completed ********************
pause