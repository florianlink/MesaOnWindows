# MesaOnWindows

This repository contains scripts to download and build Mesa3D and LLVMPipe on Windows.
It will download all required tools and build LLVM and Mesa3D using the Visual Studio compiler.
The resulting opengl32.dll will be placed into the top-most build directory.

This build script has been tested with Mesa 10.6.0 and LLVM 3.6.1 on Visual Studio 2013 X64.

If you want to build a different version combination or a newer Mesa/LLVM version, you can edit the
version numbers in the *buildMesa.py* file.

NOTE: Some of the installers that are downloaded are not silent, you are supposed to install them
to their default location. If you install MinGW to a different place than C:\MinGW you will need to edit
buildMesa.py as well.

Have fun with the scripts and I hope they make your life easier!
