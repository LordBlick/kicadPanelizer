---
title: kicadPanelizer
description: KiCAD PCB panelization helper
author: LordBlick
tags: KiCAD, PCB, EDA, electronics
created:  2014.10.03
modified: 2015.09.09

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
<!-- ![screenshoot](https://cloud.githubusercontent.com/assets/5176054/4541215/b4664a38-4e10-11e4-8062-c265e0ce5612.png) -->
![screenshoot](https://cloud.githubusercontent.com/assets/5176054/4544490/b44583de-4e33-11e4-86ea-30b0c47d15d2.png)

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
- Split Margin setup onto independent X and Y axes (almost done already).
- Support for positioning fiducial (first draw done in secret ugly code with not yet working dialog).
- Very useful will be using settings file per project with output directory choice etc.
- Last used files list.
- Drop custom layers clonning.
- Direct output to Gerber(already supported) and drill(I'm not sure yet that drill is supported in KiCAD pcbnew scripting) files.
- Own net names for every clone which has net attributes(zones, tracks, vias and pads).
- Add some edge cutout visualization.
- Add support for complement 180° rotation with cutout by generated on the fly NPTH oval or micro-drill pads with preselected tool diameter. This has the advantage that you do not need to create an additional program for CNC milling machines, because everything is contained in the drilling file.
- Recognized more complicated lines of edge cutout layer.
