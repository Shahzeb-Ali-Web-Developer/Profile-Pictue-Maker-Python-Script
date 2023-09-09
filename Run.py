# Professional Profile Picture Maker Python Script by Shahzeb Ali - Professional Web Developer

import requests
from PIL import Image, ImageDraw
import io
import os

# Replace with your Remove.bg API key
API_KEY = 'YMtgmGP3aUw1vYPo9yXNozZF'

# API endpoint
API_ENDPOINT = 'https://api.remove.bg/v1.0/removebg'


def remove_background(input_image_path, output_image_path):
    # Make a POST request to the Remove.bg API
    response = requests.post(
        API_ENDPOINT,
        headers={'X-Api-Key': API_KEY},
        files={'image_file': open(input_image_path, 'rb')},
    )

    # Check for a successful response
    if response.status_code == requests.codes.ok:
        # Convert the response content to an image
        img = Image.open(io.BytesIO(response.content))

        # Save the final image as a transparent PNG
        img.save(output_image_path, 'PNG')
        print("Background removed and saved to", output_image_path)
    else:
        print("Error:", response.status_code, response.text)


def crop_to_circle(img):
    # Create a mask for the circle
    mask = Image.new("L", img.size, 0)
    width, height = img.size
    radius = min(width, height) // 2
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, width, height), fill=255)

    # Apply the mask to the image
    img.putalpha(mask)

    return img


if __name__ == '__main__':
    input_image_path = 'input.jpg'  # Replace with your input image file path
    output_image_path = 'temp_removed_bg.png'  # Temporary file for removed background (PNG format)
    background_image_path = 'Files/background.jpg'  # Replace with the path to your square background image
    final_output_image_path = 'final_result.png'  # Replace with your desired output file path

    # Crop the input image into a circle
    input_image = Image.open(input_image_path)
    input_image = crop_to_circle(input_image)

    # Save the circular cropped image
    input_image.save(output_image_path, 'PNG')

    # Remove the background from the circular cropped image
    remove_background(output_image_path, output_image_path)

    # Open the removed background image
    removed_bg_image = Image.open(output_image_path)

    # Load the square background image
    background = Image.open(background_image_path)

    # Resize the removed background image to match the background's dimensions
    removed_bg_image = removed_bg_image.resize(background.size, resample=Image.LANCZOS)

    # Create a transparent overlay by adjusting the alpha (transparency)
    overlay = Image.new('RGBA', background.size, (0, 0, 0, 0))
    overlay.paste(removed_bg_image, (0, 0), removed_bg_image)

    # Composite the images
    final_image = Image.alpha_composite(background.convert('RGBA'), overlay)

    # Save the final image
    final_image.save(final_output_image_path, 'PNG')

    # Clean up temporary removed background image
    os.remove(output_image_path)

    print("Final image saved to", final_output_image_path)
