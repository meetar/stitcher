import requests
from PIL import Image
import io
import imghdr

# Base URL of the tiled image
base_url = "https://iiif.dx.artsmia.org/139987.jpg/"

# Dimensions of the entire image
image_width = 5273  # Replace with the actual width of the image
image_height = 7029  # Replace with the actual height of the image

# Tile size (in pixels)
tile_width = 512
tile_height = 512

# Calculate the number of rows and columns
num_rows = (image_height + tile_height - 1) // tile_height
num_cols = (image_width + tile_width - 1) // tile_width

# Download all tiles
all_tiles = []

for row in range(num_rows):
    for col in range(num_cols):
        # Calculate the region for the current tile
        x1 = col * tile_width
        y1 = row * tile_height
        x2 = min((col + 1) * tile_width, image_width)
        y2 = min((row + 1) * tile_height, image_height)

        # Calculate x2 and y2 based on whether it's the last column or row
        if col == num_cols - 1:
            x2 = image_width  # Last column, use the remaining width
        else:
            x2 = (col + 1) * tile_width

        if row == num_rows - 1:
            y2 = image_height  # Last row, use the remaining height
        else:
            y2 = (row + 1) * tile_height

        # Generate the URL for the current tile
        tile_url = f"{base_url}{x1},{y1},{x2 - x1},{y2 - y1}/{x2 - x1},/0/default.jpg"

        # Download the tile
        try:
          response = requests.get(tile_url)

          # Check if the response contains a valid image
          image_type = imghdr.what(None, h=response.content)

          if image_type:
              # The response content is a valid image
              tile_image = Image.open(io.BytesIO(response.content))
              all_tiles.append(tile_image)
          else:
              print(f"Invalid image at URL: {tile_url}")


        except Exception as e:
            print(f"Error opening image: {e}")


# Stitch the tiles together into a single image
stitched_image = Image.new("RGB", (image_width, image_height))

for row in range(num_rows):
    for col in range(num_cols):
        tile_image = all_tiles[row * num_cols + col]
        stitched_image.paste(tile_image, (col * tile_width, row * tile_height))

# Save the stitched image to a file
stitched_image.save("stitched_image.png")

print("All tiles downloaded and stitched successfully.")
