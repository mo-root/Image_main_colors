from flask import Flask, request, render_template
from PIL import Image
import webcolors

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        image = Image.open(request.files["image"].stream)
        image = image.convert("RGBA")

        # Resize image for faster processing
        image.thumbnail((128, 128))

        # Get the pixels from the image
        pixels = image.getdata()

        # Count the frequency of each color in the image
        color_frequency = {}
        for pixel in pixels:
            if pixel[3] == 0:
                continue  # Skip transparent pixels
            if pixel[:3] in color_frequency:
                color_frequency[pixel[:3]] += 1
            else:
                color_frequency[pixel[:3]] = 1

        # Get the specified number of most frequent colors
        num_colors = int(request.form["num_colors"])
        main_colors = sorted(color_frequency.items(), key=lambda x: x[1], reverse=True)[:num_colors]

        # Convert the RGB values to hex codes
        main_colors = [(webcolors.rgb_to_hex(color[0]), webcolors.rgb_to_hex(color[0])) for color in main_colors]

        return render_template("result.html", main_colors=main_colors)

    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
