---
title: kicadPanelizer
description: KiCAD PCB panelization helper
author: LordBlick
tags: KiCAD, PCB, EDA, electronics
created:  2014.10.03
modified: 2014.10.03

---

kicadPanelizer
=======
## Introduction

kicadPanelizer is a program for fast automatic PCB panelization proces. That's what people have been doing so far manually, sometimes wasting a lot of time, using the "Join plate" option, it is now achievable by a few clicks.

## The basic features of the software:
- gtk based

- Rotation(90° step) & matrix input.

- Margin(in mm and mils) input.

- Space(in mm and mils) for X nad Y axes input.

- Drag'n drop input file.

- Remembers last used settings.

Some screenshoot:

<!-- ![screenshoot](https://cloud.githubusercontent.com/assets/5176054/4505567/3bb70a44-4af7-11e4-91a8-0360eab9ceae.png) -->
<!-- ![screenshoot](https://cloud.githubusercontent.com/assets/5176054/4526874/25ddc384-4d63-11e4-965a-af05e8820d4a.png) -->
![screenshoot](https://cloud.githubusercontent.com/assets/5176054/4541215/b4664a38-4e10-11e4-8062-c265e0ce5612.png)

This one program is designed as a maximum to facilitate as much as possible.

## Installation
Unpack newest release to prefered dir.

## Running initially testing script.
From command line in dir with script:
> python pcbPanelize

Unix based OS user can set execute privileges to execute as any other shell script:
> chmod +x pcbPanelize

> ./pcbPanelize

To run it it's nessesary to install:
- [Python interpreter] in version 2 (On today newests is 2.7.8). Don't miss with version 3 (On today newests is 3.4.1).
- [KiCAD] compiled with allowed python scripting. Minimum BZR version is 5161.
- [GTK Libraries].
[Python interpreter]: https://www.python.org/downloads/
[KiCAD]: http://kicad-pcb.org/
[GTK Libraries]: http://www.gtk.org/download/


TO DO:
- wxWidgets version, suitable to other KiCAD programs.
- On today it recognized only straight lines of edge cutout layer.
- Last used files list.
- Own net names for every clone which has net atributes(zones, tracks, vias and pads).
