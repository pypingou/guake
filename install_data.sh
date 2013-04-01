#!/bin/sh

PREFIX=$1

# install icons
mkdir -p $PREFIX/share/pixmaps/guake/
cp data/pixmaps/* $PREFIX/share/pixmaps/guake/

# install man page
mkdir -p $PREFIX/share/man/man1/
cp data/guake.1 $PREFIX/share/man/man1/

# install icons
mkdir -p $PREFIX/share/icons/hicolor/
cp -r data/icons/ $PREFIX/share/icons/hicolor/

# install glade files
mkdir -p $PREFIX/share/guake/
cp data/*.glade $PREFIX/share/guake/

# install dbus file
mkdir -p $PREFIX/share/dbus-1/services/
cp data/org.guake.Guake.service $PREFIX/share/dbus-1/services/

# install desktop files
mkdir -p $PREFIX/share/applications/
cp data/*.desktop $PREFIX/share/applications/

