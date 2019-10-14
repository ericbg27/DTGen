import os
import argparse
import colored
from colored import stylize
from PIL import Image, ImageDraw

def ParseCommandLine():
	global image_arg

	parser = argparse.ArgumentParser()
	parser.add_argument("size", help="size of the tree to be created", type=int)
	parser.add_argument("dir", help="Directory for which the tree will be created")
	parser.add_argument('-i', "--image", help="Variable that defines if an image will be created [y or n]", default="n")
	args = parser.parse_known_args()

	if args[0].size < 1:
		print("Size must be at least 1. Finishing execution...")
		return

	if not os.path.isdir(args[0].dir):
		print("Not a valid directory. Finishing execution...")
		return
	else:
		os.chdir(args[0].dir)

	if args[0].image.lower() == "y":
		image_dir_parser = argparse.ArgumentParser()
		image_dir_parser.add_argument('-d', "--image_dir", help="Directory in which tree image will be saved, if desired. [Default: Directory for which tree will be created]", default=os.getcwd())
		image_arg = image_dir_parser.parse_known_args()[0].image_dir

	return args

def MemoizedDTGen(tree_depth, root_dir):
	dir_dict = {}
	childs = {}

	return DTGen(tree_depth, root_dir, dir_dict, childs)


def DTGen(tree_depth, parent_dir, dir_dict, childs):
	if tree_depth == 0:
		return (dir_dict, childs)
	else:
		#print(os.getcwd())
		list_dir = os.listdir(os.getcwd())

		dir_dict[os.getcwd()] = list_dir

		tree_depth = tree_depth - 1

		childs[os.getcwd()] = []

		for entry in list_dir:
			if os.path.isdir(entry):
				childs[os.getcwd()].append(entry)
				os.chdir(entry)
				(dir_dict, childs) = DTGen(tree_depth, os.getcwd(), dir_dict, childs)
				os.chdir(parent_dir)

		return dir_dict, childs

def CheckSize(actual_width, actual_height):
	global image_height
	global image_width

	if actual_height >= image_height - 50:
		image_height = actual_height + 100

	if actual_width >= image_width - 50:
		image_width = actual_width + 100

def PrintTree(tree_depth, d, spacing_counter, root_dir, l, c, specs):
	global image_width
	global image_height
	global img
	global draw

	current = os.getcwd()
	spacing_counter = spacing_counter + 4

	tree_depth = tree_depth - 1

	specs[1] = 10

	for j, entry in enumerate(d):
		if os.getcwd() != root_dir:
			i = 0
			while i < spacing_counter - 4:
				if i % 4 == 0 and i != 0:
					specs[1] = specs[1] + 12
					CheckSize(specs[1], specs[0])

					if l[i//4-1] != c[i//4-1]:
						print("|", end='')
						draw_dict[(specs[1], specs[0])] = ("|", "black")
					else:
						print(" ", end='')
				print(" ", end='')
				i = i + 1
			
			specs[1] = specs[1] + 12
			CheckSize(specs[1], specs[0])

			if l[len(l)-1] != c[len(c)-1]:
				print("|", end='')
				draw_dict[(specs[1], specs[0])] = ("|", "black")
			else:
				print(" ", end='')
		
		for i in range(4):
			print(" ", end='')

		if not os.path.isdir(entry):
			specs[1] = specs[1] + 12
			CheckSize(specs[1], specs[0])

			print("|__ " + stylize(entry, colored.fg("green")))
			draw_dict[(specs[1], specs[0])] = ("|__ ", "black")

			specs[1] = specs[1] + 20
			CheckSize(specs[1] + len(entry), specs[0])

			draw_dict[(specs[1], specs[0])] = (entry, "green")

			specs[1] = 10
			specs[0] = specs[0] + 10
			CheckSize(specs[1], specs[0])

		if os.path.isdir(entry):
			specs[1] = specs[1] + 12
			CheckSize(specs[1], specs[0])

			print("|__ " + stylize(entry, colored.fg("red")))
			draw_dict[(specs[1], specs[0])] = ("|__ ", "black")

			specs[1] = specs[1] + 20
			CheckSize(specs[1] + len(entry), specs[0])

			draw_dict[(specs[1], specs[0])] = (entry, "red")

			specs[1] = 10
			specs[0] = specs[0] + 10
			CheckSize(specs[1], specs[0])

			parent_dir = os.getcwd()
			os.chdir(entry)
			if tree_depth != 0:
				size = len(l)
				l.append(len(d)-1)
				c.append(j)

				PrintTree(tree_depth, dir_dict[os.getcwd()], spacing_counter, root_dir, l, c, specs)

				l = l[0:size]
				c = c[0:size]
			os.chdir(parent_dir)

	return

def DrawTree(image_name):
	global image_width
	global image_height
	global draw_dict

	img = Image.new('RGB', (image_width, image_height), color = "white")

	draw = ImageDraw.Draw(img)

	draw.text((10, 10), "|__ " + root_dir, fill="black")

	for key, elem in draw_dict.items():
		draw.text(key, elem[0], fill=elem[1])

	img.save(image_name)

	print("\n")
	print("Tree image created at: " + image_name)

if __name__ == "__main__":	
	image_arg = ""

	args = ParseCommandLine()

	tree_depth = args[0].size
	root_dir = os.getcwd()

	
	(dir_dict, childs) = MemoizedDTGen(tree_depth, root_dir)

	spacing_counter = 0
	lengths = []
	counters = []

	print("|__ " + root_dir)

	dir_name = os.getcwd().split('/')

	image_specs = [20,10]

	image_height = 300
	image_width = 300

	draw_dict = {}
	
	PrintTree(tree_depth, dir_dict[root_dir], spacing_counter, root_dir, lengths, counters, image_specs)

	if args[0].image.lower() == "y":
		image_name = dir_name[-1] + "_DTree.png"

		if image_arg[-1] == '/':
			image_name = image_arg + image_name
		else:
			image_name = image_arg + '/' + image_name

		DrawTree(image_name)