#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, Image, sys, base64

RESERVED_PIXELS = 10

def convert_to_binary(string):
	return "".join(bin(ord(char))[2:].zfill(8) for char in string)

def convert_to_string(string):
	return "".join(chr(int(bin, 2)) for bin in re.findall(r'.{8}', string))

def pixels(len):
	for i in xrange(len[1]):
		for j in xrange(len[0]):
			yield (j, i)

def encrypt(msg):
	return base64.b64encode(msg)

def decrypting(msg):
	return base64.b64decode(msg)

def insert_text(img, dest, msg):
	image = Image.open(img)
	width, height = image.size

	if image.mode[:3] != "RGB" or width * height * 3 < len(msg) + RESERVED_PIXELS * 3:
		raise IndexError("Unable to use this picture")

	bits = bin(len(msg))[2:].zfill(RESERVED_PIXELS * 3)
	msg = bits + msg

	msg = enumerate(msg + "0" * (3 - len(msg) % 3))
	p = image.load()

	for i, j in pixels(image.size):
		try:
			rgb = map(lambda color, bit: color - (color % 2) + int(bit), p[i, j][:3], [msg.next()[1] for _ in xrange(3)])
			p[i, j] = tuple(rgb)
		except StopIteration:
			image.save(dest, "PNG", quality = 100)
			return

def extract_text(img):
	image = Image.open(img)
	length = image.size
	p = image.load()
	
	leng = ""
	for pix in pixels(length):
		leng += "".join("1" if color % 2 else "0" for color in p[pix][:3])
		if len(leng) >= RESERVED_PIXELS * 3:
			leng = int(leng, 2)
			break

	binary_information = ""
	for pix in pixels(length):
		binary_information += "".join("1" if color % 2 else "0" for color in p[pix][:3])

	return binary_information[RESERVED_PIXELS * 3 : leng + RESERVED_PIXELS * 3]

def Main():
	args = len(sys.argv)
	argument = sys.argv

	if args == 4 and argument[1] == "-i":
		msg = raw_input("Enter the text: ")
		insert_text(argument[2], argument[3], convert_to_binary(encrypt(msg)))
	elif args == 3 and argument[1] == "-e":
		print decrypting(convert_to_string(extract_text(argument[2])))

if __name__ == "__main__":
	Main()