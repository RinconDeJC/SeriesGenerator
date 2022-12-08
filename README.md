# SeriesGenerator
 Script to create images for a swimming competition from an official PDF from FMN with the series organized by events.

 ## Dependencies

 There are certain dependencies in which the script relies:

 - Python 3.7 or higher. It might work with previous versions, but it 
 hasn't been checked. It can be found in the 
 [Python official web](https://www.python.org/downloads).
 - `PyPDF2` and `Pillow` libraries. They can be installed via 
[pip](https://bootstrap.pypa.io/get-pip.py) with user permissions or in
a virtual environment, as the user prefers.

 ## Directory structure

 The directories names are specified in `PathHelper`. There are some 
 directories and files that must be created in orther for the script to 
 work. These are:
 
 - Directory for all the resources (`P_RESOURCES`).
 - Directory for the base image (`P_IMAGE`).
 - Direcroty for the PDFs to be parsed (`P_PDFS`).
 - Directory for the fonts (`P_FONTS`).
 - Directory the options (`P_OPTIONS`).
 - JSON options file in `P_OPTIONS`.
 - PDF that will be parsed in `P_PDFS`.
 - Base Image specified in `options.json` in `P_IMAGE`.

 If any of these things is missing the script will output an exit with error
 code 1 if a directory is missing or 2 if a file is so.

 ## About `options.json`

 This file in the options folder contains information useful for the 
 parsing and image generation process. Some of its aspects will be explained
 here while others will have to be looked up inside the code.

 ### Parsing data

 With the parsing process the `range`, `file_name`, `competition_data`, and
`parsing_data` fields are useful.

- `range` indicates from which page of the pdf parsing is started and to 
which page to parse. This last part only if `until_end` is set to `false`.
- `file_name` indicates the PDF to be parsed, unless a name is provided
manually executing the function `execute` in `main`.
- `competition_data` holds the expected names that will appear in the PDF
refering to the different styles and distances to be swum. They should 
match exactly the way they appear in the file (case sensitive, spaces, 
etc).
- `parsing_data` has information that helps parse and format the text 
of the output. Mainly if a capital letter appears before a field it 
indicates the folowing: L a length, C a character, S a string and N a 
number. The use of them is best looked up in the code. Additional 
comments might be found inside the json file regarding some fields. 

### Image generation data

The field `image_generation` is used in `ImageGenerator.py`. First two
fields are the font of the text to be printed and the base image that
will be printed behind the text in the `P_GALLERY_CHECKING` directory.
`IMAGES_PER_FOLDER` is the number of images that will be stored in each
numbered index directory. This is useful if some streaming software
will be used alongside that limits the amount of images to be loaded
in an image slides object. The rest of the values are trial an error values
to format the text so that it fits the base image. It is best seen its use
inside the code or, simply, by trial and error manipulation.

## Image in project

All of the image generation process is done to fit the 
base image. You can modifie it in any way you want, and if you need
the original .svg file from wich it was exported it can be provided asking
at [jcdiaz.lasenda@gmail.com](jcdiaz.lasenda@gmail.com)
