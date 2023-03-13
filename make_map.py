import gmplot

# Create the gmplot object
gmap = gmplot.GoogleMapPlotter(14.599498, 121.004490, 20)

# Add the point to the map
gmap.marker(14.599498, 121.004490)

# Save the map as an HTML file
gmap.draw("mymap.html")