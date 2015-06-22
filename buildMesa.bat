
rem Adapt this call to setup the environment for your visual studio version and 32/64 bit:
call "C:\Program Files (x86)\Microsoft Visual Studio 12.0\VC\vcvarsall.bat" amd64

rem Run the build script
python buildMesa.py
