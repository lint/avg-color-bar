# avg-color-bar

Generates a bar of colors for a given number of images.
Images must be in a folder called "images" and numbered sequentially in the order to be processed.

Finds the average rgb, hsv, hue, and uses kmeans, xyz, lab, and the most common color to create the bar.

To extract the frames I used ffmpeg with the command:
        ffmpeg -i input.mkv -vf fps=.25 images/%04d.jpg
