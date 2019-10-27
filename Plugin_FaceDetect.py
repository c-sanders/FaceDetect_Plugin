#!/usr/bin/env python

# Description
# ===========
#
# GIMP Plugin to overlay one image on top of another.
#
#
# Running this Plugin from the command line
# =========================================
#
# I think I once read somewhere, that when a GIMP Plugin is invoked from the command line, the
# arguments need to be passed to the Plugin as strings. Attempting to do otherwise can result in
# GIMP runtime errors, such as the following;
#
#   Error: ( : 1) eval: unbound variable: DO_NOTHING
#   Error: ( : 1) Invalid type for argument 5 to python-fu-runPlugin-multiple-fromFile
#
# To invoke this Plugin from the command line, use a command which is similar to the following;
#
#   gimp --no-interface \
#        --verbose \
#        --console-messages \
#        --batch-interpreter="plug-in-script-fu-eval" \
#        --batch '( \
#                  python-fu-runPlugin-multiple-fromList \
#                  RUN-NONINTERACTIVE \
#                  "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png" \
#                  "READ_LIST_FROM_STDIN",
#                  "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/fileList.txt" \
#                  "/home/craig/temp/Animation_images_png/" \
#                  "DO_NOTHING" \
#                  "result" \
#                  "DIAGNOSTIC_DATA_NONE" \
#                 )' \
#        --batch '(gimp-quit 0)'
# 
# Alternatively, here is the same command presented all on one line so as to assist with a cut and
# paste of the command onto a command line.
# 
# gimp --no-interface --verbose --console-messages --batch-interpreter="plug-in-script-fu-eval" --batch '(python-fu-runPlugin-multiple-fromList RUN-NONINTERACTIVE "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png" "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/fileList.txt" "/home/craig/temp/Animation_images_png/" "0" "result" "0")' --batch "(gimp-quit 0)"
#
#
# Analysis of Plugin arguments
# ============================
#
# The arguments which were presented to the Plugin in the above example, are as follows;
#
# Argument 1 = RUN-NONINTERACTIVE
# Argument 2 = "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/slides/png/Eulers_formula_animation_slides-000001.png"
# Argument 3 = "/home/craig/local/source/GitHub_projects/c-sanders/Animation_build/frames/png/animation_1/fileList.txt"
# Argument 4 = "/home/craig/temp/Animation_images_png/"
# Argument 5 = "DO_NOTHING
# Argument 6 = "result"
# Argument 7 = "DIAGNOSTIC_DATA_NONE"
#
# /home/foo/fileList.txt should be a file that contains a list of those files (one per line) which
# should be operated on by the Plugin.
#
#
# Plugin locations
# ================
#
# Exmples of locations within which Gimp Plugins can reside;
#
#   - /home/foo/.gimp-2.x/plug-ins
#   - /usr/lib/gimp/2.0/plug-ins


from   os     import path
import time
import subprocess

from   gimpfu import register, main, pdb, gimp, PF_IMAGE, PF_DRAWABLE, PF_INT, PF_STRING, PF_FILE, PF_BOOL, INTERPOLATION_NONE, INTERPOLATION_LINEAR, INTERPOLATION_CUBIC, INTERPOLATION_LANCZOS, PF_RADIO
# from   diagnosticDataDialog import DiagnosticDataDialog, DIAGNOSTIC_DATA_STDOUT, DIAGNOSTIC_DATA_DIALOG, DIAGNOSTIC_DATA_BOTH, DIAGNOSTIC_DATA_NONE

DO_NOTHING = "0"

COLOUR_RED     = "COLOUR_RED"
COLOUR_GREEN   = "COLOUR_GREEN"
COLOUR_BLUE    = "COLOUR_BLUE"
COLOUR_CYAN    = "COLOUR_CYAN"
COLOUR_MAGENTA = "COLOUR_MAGENTA"
COLOUR_YELLOW  = "COLOUR_YELLOW"


def runPlugin(

  filename_input,
  filename_result,
  filename_face_detect,
  filename_cascade,
  colour_rectangle
) :

	"""
	This function gets registered with GIMP as it implements the following Plugin : Detect Faces

	This function will attempt to detect faces within an image, and any faces which it does detect it will frame with a rectangle. Once it has finished doing this,
	it will save the resulting image into a file.


	Parameters:

	filename_input (String) :
	The filename of the input image.

	filename_result (String) :
	The filename of the file into which the resulting image will be saved.

	filename_cascade (String) :
	The filename of the Harr Transform Cascade file which should be used to detect the faces.

	colour_rectangle (String) :
	The colour to use for the face framing rectangles.


	Returns:

	NA


	Invoked by :

	GIMP


	Invokes:

	None
	"""


	nameProcedure = "runPlugin_single"


	print("%s : Enter" % (nameProcedure))

	print("%s : %s" % (nameProcedure, filename_input))
	print("%s : %s" % (nameProcedure, filename_result))
	print("%s : %s" % (nameProcedure, colour_rectangle))

	# Open and display withih GIMP, the input image.

	image_input = pdb.gimp_file_load(filename_input, filename_input)

	pdb.gimp_display_new(image_input)

	# "Clean" the following image by setting its Dirty (Edit) counter to 0. 
	#
	# If this is not done and the user attempts to close the image, then GIMP will complain that the image has
	# unsaved changes.

	pdb.gimp_image_clean_all(image_input)

	# Run the Face detection code on the Input image.
	#
	# At the time this Plugin was developed, Python and its Plugins could only be implemented using Python 2; whereas the Face detection code has 
	# unfortunately been implemented using Python 3 source code and modules. Therefore, if this Plugin were to try and run the Face detection code
	# directly, then the Python Runtime system would fail. It is for this reason that the Face detection code has been invoked below as a separate
	# processs.

	subprocess.call(
	  [
	   "python3",
	   filename_face_detect,
	   filename_cascade,
	   filename_input,
	   filename_result,
	   colour_rectangle
	  ]
	)

	# Open and display within GIMP, the result image.

	image_result = pdb.gimp_file_load(filename_result, filename_result)

	pdb.gimp_display_new(image_result)

	# "Clean" the following image by setting its Dirty (Edit) counter to 0. 
	#
	# If this is not done and the user attempts to close the image, then GIMP will complain that the image has
	# unsaved changes.

	pdb.gimp_image_clean_all(image_result)

	print("%s : Exit" % (nameProcedure))


register(
	"runPlugin",                  # The name of the command.
	"Detect Faces in an Image.",  # A brief description of the command.
	"Detect Faces in an Image.",  # Help message.
	"Craig Sanders",              # Author.
	"Craig Sanders",              # Copyright holder.
	"2019",                       # Date.
	"Detect Faces",               # The way the script will be referred to in the menu.
	# "RGB*, GRAY*",              # Image mode
	"",                           # Create a new image, don't work on an existing one.
	[
		(PF_FILE,
		 "filename_input",
		 "Filename of Input Image",
		 "/home/craig/Pictures/Daddy and James.jpg"
		),
		(PF_FILE,
		 "filename_result",
		 "Filename of Resulting Image",
		 "/home/craig/Pictures/result.jpg"
		),
		(PF_FILE,
		 "filename_face_detect",
		 "Filename of Face detect Python code",
		 "/home/craig/gimp-2.8/plug-ins/FaceDetect/face_detect_cv3.py"
		),
		(PF_FILE,
		 "filename_cascade",
		 "Filename of Cascade file",
		 "/home/craig/local/source/GitHub_projects/other/FaceDetect/haarcascade_frontalface_default.xml"
		),
		(PF_RADIO,
		"filename_manipulation_method",
		"Colour for face detect rectangles",
		COLOUR_GREEN,
			(
				("Red",     "COLOUR_RED"),
				("Green",   "COLOUR_GREEN"),
				("Blue",    "COLOUR_BLUE"),
				("Cyan",    "COLOUR_CYAN"),
				("Magenta", "COLOUR_MAGENTA"),
				("Yellow",  "COLOUR_YELLOW")
			)
		)
	],
	[],
	runPlugin,
	menu="<Image>/Image/Craig's Utilities/")


main()
