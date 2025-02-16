from PIL import Image

# Open the original image
icon = Image.open('app.png')

# Define the sizes for the new icons
sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]

# Create and save the .ico file with multiple sizes
icon.save('app.ico', format='ICO', sizes=sizes)

print("app.ico created successfully.")