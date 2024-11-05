import os
from PIL import Image, ImageDraw
from natsort import natsorted
import argparse

def create_pdf_from_pngs(directory_path):
    # Get the last part of the directory to use for the PDF name
    ##pdf_name = os.path.basename(os.path.normpath(directory_path)) + ".pdf" ### old way

    pdf_name = directory_path.replace('../', '').replace('/', '_').strip('_') + ".pdf"

    # Get all PNG files from the directory
    png_files = [f for f in os.listdir(directory_path) if f.endswith('.png')]

    # Sort the files by their natural sort order (this takes care of similar names)
    sorted_png_files = natsorted(png_files)

    if not sorted_png_files:
        print("No PNG files found in the directory.")
        return

    # Define the grid layout (2 rows x 4 columns)
    images_per_page = 8
    grid_size = (2, 4)  # 2 rows, 4 columns

    # Define page size (A4, 595x842 points, but this is arbitrary and can be adjusted)
    page_width, page_height = (842, 595)  # Swap width and height for landscape A4 size
    image_width = page_width // grid_size[1]  # Divide width by number of columns
    image_height = page_height // grid_size[0]  # Divide height by number of rows

    # Create a list to store pages (each page will be a PIL image)
    pages = []

    # Create pages with 8 images each
    for i in range(0, len(sorted_png_files), images_per_page):
        page_images = sorted_png_files[i:i+images_per_page]

        # Create a new blank page
        page = Image.new('RGB', (page_width, page_height), (255, 255, 255))  # White background
        draw = ImageDraw.Draw(page)

        # Place the images in the grid
        for index, png_file in enumerate(page_images):
            image_path = os.path.join(directory_path, png_file)
            img = Image.open(image_path)

            # Resize image to fit into the grid cell
            img = img.resize((image_width, image_height), Image.Resampling.LANCZOS)

            # Calculate position in the grid
            row = index // grid_size[1]
            col = index % grid_size[1]
            x_position = col * image_width
            y_position = row * image_height

            # Paste the image onto the page
            page.paste(img, (x_position, y_position))

        # Append the page to the list
        pages.append(page)

    # Save all the pages as a single PDF
    if pages:
        pages[0].save(os.path.join(directory_path, pdf_name), save_all=True, append_images=pages[1:])
        print(f"PDF created successfully: {pdf_name}")

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

    # Call the function with the provided directory path
    create_pdf_from_pngs(args.directory)