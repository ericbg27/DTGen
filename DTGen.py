import os
import argparse
import colored
from colored import stylize


def ParseCommandLine():
	parser = argparse.ArgumentParser()
	parser.add_argument("size", help="size of the tree to be created", type=int)
	parser.add_argument("dir", help="directory for which the tree will be created")
	args = parser.parse_args()

	if args.size < 1:
		print("Size must be at least 1. Finishing execution...")
		return

	if not os.path.isdir(args.dir):
		print("Not a valid directory. Finishing execution...")
		return
	else:
		os.chdir(args.dir)

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

def PrintTree(tree_depth, d, spacing_counter, root_dir, l, c):
	current = os.getcwd()
	spacing_counter = spacing_counter + 4

	tree_depth = tree_depth - 1

	for j, entry in enumerate(d):
		if os.getcwd() != root_dir:
			i = 0
			while i < spacing_counter - 4:
				if i % 4 == 0 and i != 0:
					if l[int(i/4)-1] != c[int(i/4)-1]:
						print("|", end='')
					else:
						print(" ", end='')
				print(" ", end='')
				i = i + 1
			if l[len(l)-1] != c[len(c)-1]:
				print("|", end='')
			else:
				print(" ", end='')
		for i in range(4):
			print(" ", end='')
		if not os.path.isdir(entry):
			print("|__ " + stylize(entry, colored.fg("green")))
		if os.path.isdir(entry):
			print("|__ " + stylize(entry, colored.fg("red")))
			parent_dir = os.getcwd()
			os.chdir(entry)
			if tree_depth != 0:
				size = len(l)
				l.append(len(d)-1)
				c.append(j)

				PrintTree(tree_depth, dir_dict[os.getcwd()], spacing_counter, root_dir, l, c)
				
				l = l[0:size]
				c = c[0:size]
			os.chdir(parent_dir)

	return



if __name__ == "__main__":
	args = ParseCommandLine()

	tree_depth = args.size
	root_dir = os.getcwd()

	
	(dir_dict, childs) = MemoizedDTGen(tree_depth, root_dir)

	#print(dir_dict)
	#print(childs)

	print("|__ " + root_dir)

	spacing_counter = 0
	lengths = []
	counters = []
	
	PrintTree(tree_depth, dir_dict[root_dir], spacing_counter, root_dir, lengths, counters)