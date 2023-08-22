# scrape_maps

scripts for extracting panorama images from google maps

### panoids.py
opens a .har file and extracts the panoids (panorama ids) from it

the .har file is obtained using by opening firefox devtools in the "network" tab, hovering the mouse over the blue streetview lines and then right click, "save all as HAR"

### tile.py
reads all panoids and for each of them extracts tiles at zoom levels 1 and 5

### stitch.py
gets all raw tiles and stitches them in one image for each panorama and zoom level