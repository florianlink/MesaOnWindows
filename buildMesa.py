# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

# Author: Florian Link (florianlink at google mail)

cmakeVersionShort = "3.2"
cmakeVersion = "3.2.3"
sconsVersion = "2.3.4"
llvmVersion  = "3.6.1"
mesaVersion  = "10.6.0"

useProxy = False
proxyDict = { 'http': 'proxy:8080' , 'ftp' : 'http://proxy:8080' }

# Make sure that you install MinGW to c:\MinGW or adjust this path:
mingw       = r"C:\MinGW"

# Tweak these if download urls change over time:
zipDownload   = "http://www.7-zip.org/a/7za920.zip"
cmakeDownload = "http://www.cmake.org/files/v" + cmakeVersionShort + "/cmake-" + cmakeVersion + "-win32-x86.zip"
llvmDownload  = "http://llvm.org/releases/" + llvmVersion + "/llvm-" + llvmVersion + ".src.tar.xz"
xml2Download  = "http://xmlsoft.org/sources/win32/python/libxml2-python-2.7.7.win32-py2.7.exe"
makoDownload  = "http://pypi.python.org/packages/source/M/Mako/Mako-1.0.1.tar.gz"
sconsDownload = "http://cznic.dl.sourceforge.net/project/scons/scons/" + sconsVersion + "/scons-" + sconsVersion + ".zip"
mingwDownload = "http://heanet.dl.sourceforge.net/project/mingw/Installer/mingw-get-setup.exe"
mesaDownload  = "ftp://ftp.freedesktop.org/pub/mesa/" + mesaVersion + "/mesa-" + mesaVersion + ".tar.xz"

# Tweak these to get 64bit/32bit or a different visual studio version
cmakeVisualStudio = "Visual Studio 12 2013 Win64"
sconsMSVC    = "MSVC_VERSION=12.0"
sconsMachine = "machine=x86_64"
llvmTarget   = "Release|x64"

import urllib2
import os
import sys
import subprocess
import shutil
import zipfile

if useProxy:
  proxy_handler = urllib2.ProxyHandler( proxyDict )
  opener = urllib2.build_opener(proxy_handler)
  urllib2.install_opener(opener)

def downloadFile(url, filename):
    print 'Downloading %s -> %s' % (url, filename)
    request = urllib2.urlopen(url)
    with open(filename + ".tmp", 'wb') as f:
      blockSize = 8192
      while True:
        blockData = request.read(blockSize)
        sys.stdout.write(".")
        sys.stdout.flush()
        if not blockData:
          break
        f.write(blockData)
    os.rename(filename + ".tmp", filename)    

pythonPath  = sys.exec_prefix
python      = sys.executable
sconsScript = pythonPath + r"\Scripts\scons.py"
pip         = pythonPath + r"\Scripts\pip.exe"
mingwBin    = mingw + r"\msys\1.0\bin"
llvmDir     = "llvm-" + llvmVersion + ".src"
mesaDir     = "mesa-" + mesaVersion
cmakeDir    = "cmake-" + cmakeVersion + "-win32-x86/bin"
sconsDir    = "scons-" + sconsVersion

if not os.path.exists("build"):
  os.mkdir("build")
os.chdir("build")
curDir = os.path.abspath(".")

if not os.path.exists("7zip.zip"):
  downloadFile(zipDownload, "7zip.zip")
  zfile = zipfile.ZipFile('7zip.zip')
  zfile.extractall(".")

sevenZip    = curDir + "/7za.exe"

########################################################
# CMake
if not os.path.exists("cmake.zip"):
  downloadFile(cmakeDownload, "cmake.zip")
  subprocess.call([sevenZip, "x", "cmake.zip"])

cmakePath = curDir + "/" + cmakeDir
#subprocess.call([cmakePath + "/cmake.exe", "--version"])

########################################################
# LLVM
llvmTar = "llvm-" + llvmVersion + ".tar.xz"
if not os.path.exists(llvmTar):
  downloadFile(llvmDownload, llvmTar)
  subprocess.call([sevenZip, "x", llvmTar])
  llvmInnerTar = "llvm-" + llvmVersion + ".tar"
  subprocess.call([sevenZip, "x", llvmInnerTar])

########################################################
# Mako
subprocess.call([pip, "install" , "Mako"])

########################################################
# libxml2
if not os.path.exists("xml2.exe"):
  downloadFile(xml2Download, "xml2.exe")
  subprocess.call(["xml2.exe"])

########################################################
# Scons
sconsDir = curDir + "/" + sconsDir
if not os.path.exists("scons.zip"):
  downloadFile(sconsDownload, "scons.zip")
  subprocess.call([sevenZip, "x", "scons.zip"])
  subprocess.call([python, sconsDir + "/setup.py", "install"])

########################################################
# Mingw
if not os.path.exists("mingw.exe"):
  downloadFile(mingwDownload, "mingw.exe")
  subprocess.call(["mingw.exe"])
  subprocess.call([mingw + r"\bin\mingw-get.exe", "install", "msys-flex", "msys-bison", "msys-wget"])

env = dict(os.environ)
env["PATH"] = mingwBin + ";" + env["PATH"]

#subprocess.call([mingwBin + "/bison.exe", "--version"])
#subprocess.call([mingwBin + "/flex.exe", "--version"])
#subprocess.call([mingwBin + "/wget.exe", "--version"])

########################################################
# MESA
mesaTar = "mesa-" + mesaVersion + ".tar.xz"
if not os.path.exists(mesaTar):
  downloadFile(mesaDownload, mesaTar)
  # alternative download with wget:
  #  subprocess.call([mingwBin + "/wget.exe","-e", "use_proxy=on", "-e", "ftp_proxy=http://tmg.mevis.lokal:8080", mesaDownload])
  subprocess.call([sevenZip, "x", mesaTar])
  subprocess.call([sevenZip, "x", "mesa-" + mesaVersion + ".tar"])

########################################################
# Configure and build LLVM
if not os.path.exists("LLVM"):
  os.chdir(llvmDir)
  if os.path.exists("buildDir"):
    shutil.rmtree("buildDir")
  os.mkdir("buildDir")
  os.chdir("buildDir")

  subprocess.call([cmakePath + "/cmake.exe", "..", "-G", cmakeVisualStudio,
                                           "-DLLVM_USE_CRT_RELEASE:STRING=MT",
                                           "-DCMAKE_INSTALL_PREFIX:PATH=" +curDir + "/LLVM"])

  print "building LLVM..."
  subprocess.call(["devenv.exe", "LLVM.sln", "/Build", llvmTarget, "/Project", "INSTALL"])
  os.chdir("..")
  os.chdir("..")

########################################################
# Configure and build MESA
os.chdir(mesaDir)
env["LLVM"] = curDir + "/LLVM"

subprocess.call([python, sconsScript, "build=release", sconsMachine, sconsMSVC, "llvm=yes", "libgl-gdi"], env = env)

if os.path.exists(r"build\windows-x86_64\gallium\targets\libgl-gdi\opengl32.dll"):
  print "WE MADE IT! We have an opengl32.dll!"
  shutil.copy(r"build\windows-x86_64\gallium\targets\libgl-gdi\opengl32.dll", "../opengl32.dll")
os.chdir("..")
