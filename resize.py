import os
import shutil
from PIL import Image

# --- Configuration ---
# The folder containing the original icons.
targeted_folder = 'icons/384-144'

# The new size for the 'big' icons (e.g., os_*.png).
new_big_size = 192

# The new size for the 'small' icons (e.g., func_*.png, arrow_*.png).
new_small_size = 96

# --- End of Configuration ---

# --- Derived Configuration ---
# Original sizes are based on the targeted_folder name
try:
    original_big_size, original_small_size = map(int, os.path.basename(targeted_folder).split('-'))
except ValueError:
    print(f"Warning: Could not determine original sizes from folder name '{targeted_folder}'. Using defaults.")
    original_big_size, original_small_size = 384, 144

# New folder name is derived from the new sizes
new_folder = f'icons/{new_big_size}-{new_small_size}'

# Calculate new size for selection-big-* images, maintaining aspect ratio
# Original selection-big-* are assumed to be 432x432
original_selection_big_size = 432
big_resize_ratio = new_big_size / original_big_size
new_selection_big_size_val = int(original_selection_big_size * big_resize_ratio)
new_selection_big_size = (new_selection_big_size_val, new_selection_big_size_val)

new_big_size_tuple = (new_big_size, new_big_size)
new_small_size_tuple = (new_small_size, new_small_size)
# --- End of Derived Configuration ---


def process_icons():
    """
    Resizes icons from the targeted_folder and saves them to the new_folder.
    - 'os_*' and 'selection-big-*' icons are resized based on 'new_big_size'.
    - 'arrow_*', 'func_*', 'tool_*' icons are resized to 'new_small_size'.
    - Other .png files are copied.
    """
    # Create the target directory if it doesn't exist
    if not os.path.exists(new_folder):
        print(f"Creating directory: {new_folder}")
        os.makedirs(new_folder)

    # Loop through all files in the source directory
    for filename in os.listdir(targeted_folder):
        if not filename.endswith('.png'):
            continue

        source_path = os.path.join(targeted_folder, filename)
        target_path = os.path.join(new_folder, filename)

        try:
            resize = True
            if filename.startswith('os_'):
                new_size = new_big_size_tuple
                print(f"Resizing big icon '{filename}' to {new_size}...")
            elif filename.startswith('selection-big-'):
                new_size = new_selection_big_size
                print(f"Resizing selection icon '{filename}' to {new_size}...")
            elif filename.startswith(('arrow_', 'func_', 'tool_')):
                new_size = new_small_size_tuple
                print(f"Resizing small icon '{filename}' to {new_size}...")
            else:
                resize = False
                print(f"Copying icon '{filename}'...")
                shutil.copy(source_path, target_path)

            if resize:
                with Image.open(source_path) as img:
                    # Resize the image using a high-quality filter
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                    # Save the resized image
                    resized_img.save(target_path, 'PNG')

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    print("\nIcon processing complete.")
    print(f"New icons are located in: {new_folder}")
    print("Don't forget to update your 'theme.conf' to use the new icons.")


if __name__ == '__main__':
    process_icons()