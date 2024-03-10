# scrape_maps

scripts for extracting panorama images from google maps

### panoids.py
opens a .har file and extracts the panoids (panorama ids) from it

the .har file is obtained using by opening firefox devtools in the "network" tab, hovering the mouse over the blue streetview lines and then right click, "save all as HAR"

### panoids2.py
obtains panoids from a set of coordinates that determine vertices of rectangles in a map

### tile.py
reads all panoids and for each of them downloads tiles at zoom levels 1 and 5

### stitch.py
gets all raw tiles and stitches them in one image for each panorama and zoom level

### ocr.py
runs ocr (optical character recognition) on all high resolution images. saves the recognized text in a .json file
