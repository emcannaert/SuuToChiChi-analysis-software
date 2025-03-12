import os
from PIL import Image, ImageDraw
import argparse
import re

# Function to perform natural sorting without natsort
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def create_pdf_from_pngs(directory_path):
    # Get the last part of the directory to use for the PDF name
    pdf_name = directory_path.replace('../', '').replace('/', '_').strip('_') + ".pdf"

    # Create the "pdf" folder in the same directory as this script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_directory = os.path.join(script_directory, 'pdf')

    # Create the folder if it doesn't exist
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    # Full path to save the PDF
    output_path = os.path.join(pdf_directory, pdf_name)

    # Get all PNG files from the directory
    png_files = [f for f in os.listdir(directory_path) if f.endswith('.png')]

    # Sort the files naturally
    sorted_png_files = sorted(png_files, key=natural_sort_key)

    if not sorted_png_files:
        print "No PNG files found in the directory."
        return

    # Define the grid layout (2 rows x 4 columns)
    images_per_page = 8
    grid_size = (2, 4)

    # Define page size (A4 landscape: 842x595 points)
    page_width, page_height = (7000, 4000)
    image_width = page_width // grid_size[1]
    image_height = page_height // grid_size[0]

    # Create a list to store pages
    pages = []

    # Create pages with 8 images each
    for i in range(0, len(sorted_png_files), images_per_page):
        page_images = sorted_png_files[i:i+images_per_page]

        # Create a new blank page
        page = Image.new('RGB', (page_width, page_height), (255, 255, 255))

        # Place the images in the grid
        for index, png_file in enumerate(page_images):
            image_path = os.path.join(directory_path, png_file)
            img = Image.open(image_path)

            # Resize image to fit the grid cell
            img = img.resize((image_width, image_height), Image.ANTIALIAS)

            # Calculate grid position
            row = index // grid_size[1]
            col = index % grid_size[1]
            x_position = col * image_width
            y_position = row * image_height

            # Paste the image onto the page
            page.paste(img, (x_position, y_position))

        # Append the page
        pages.append(page)

    # Save all pages as a single PDF in the "pdf" folder
    if pages:
        pages[0].save(output_path, save_all=True, append_images=pages[1:])
        print "PDF created successfully: {}".format(output_path)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Convert PNG files in a directory to a single PDF with 8 images per page.")
    parser.add_argument(
        "directory", 
        type=str, 
        help="Path to the directory containing PNG files."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the function
    create_pdf_from_pngs(args.directory)