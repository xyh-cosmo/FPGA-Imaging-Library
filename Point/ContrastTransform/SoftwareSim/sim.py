"""
Project
FPGA-Imaging-Library

Design
ContrastTransform

Function
Change the contrast of an image.

Module
Software simulation.

Version
1.0

Modified
2015-05-16

Copyright (C) 2015 Tianyu Dai (dtysky) <dtysky@outlook.com>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

Homepage for this project:
	http://fil.dtysky.moe

Sources for this project:
	https://github.com/dtysky/FPGA-Imaging-Library

My e-mail:
	dtysky@outlook.com

My blog:
	http://dtysky.moe
"""

__author__ = 'Tianyu Dai (dtysky)'

from PIL import Image
import os, json
from ctypes import *
user32 = windll.LoadLibrary('user32.dll')
MessageBox = lambda x:user32.MessageBoxA(0, x, 'Error', 0) 

FileFormat = ['.jpg', '.bmp']
Conf = json.load(open('../ImageForTest/conf.json', 'r'))['conf']
Debug = False

def show_error(e):
	MessageBox(e)
	exit(0)

def name_format(root, name, ex, conf):
	ct_scale = conf['ct_scale']
	return '%s-%s-soft%s' % (name, ct_scale, '.bmp')

def transform(im, conf):
	mode = im.mode
	ct_scale = conf['ct_scale']
	if mode not in ['RGB', 'L']:
		show_error('This module just supports RGB and Gray-scale images, check your images !')
	if ct_scale < 0:
		show_error('''"ct_scale" must be greater than 0 !''')
	im_res = im.point(lambda p : p * ct_scale)
	return im_res

def debug(im, conf):
	mode = im.mode
	ct_scale = conf['ct_scale']
	data_src = im.getdata()
	data_res = ''
	for p in data_src:
		if mode == 'RGB':
			r = int(p[0] * ct_scale)
			g = int(p[1] * ct_scale)
			b = int(p[2] * ct_scale)
			data_res += '%d %d %d\n' % (r, g, b)
		else:
			data_res += '%d\n' % int(p * ct_scale)
	return data_res

FileAll = []
for root, dirs, files in os.walk('../ImageForTest'):
    for f in files:
    	name, ex = os.path.splitext(f)
        if ex in FileFormat:
        	FileAll.append((root+'/', name, ex))
for root, name, ex in FileAll:
	im_src = Image.open(root + name + ex)
	for c in Conf:
		if Debug:
			open('../SimResCheck/%s.dat' \
				% name_format(root, name, ex, c), 'w').write(debug(im_src, c))
			continue
		transform(im_src, c).save('../SimResCheck/%s' % name_format(root, name, ex, c))