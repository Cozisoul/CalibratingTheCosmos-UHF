# view_residual.py
# A script to view the residual image after cleaning.

from astropy.io import fits
from astropy.visualization import ZScaleInterval
import matplotlib.pyplot as plt
import numpy as np

# Define the path to your CASA residual image
# Note: We can't use the FITS file; we must access the CASA .residual image directory
# To do this, we need to use a different tool. Let's adapt the bandpass plotter!
from casatools import image

# Create an instance of the image tool
ia = image()

residual_image = 'images/J1939-6342_UHF.residual'
output_file = 'images/residual_image_view.png'

print(f"--> Opening CASA image: {residual_image}")

# Open the CASA image and get the pixel data
try:
    ia.open(residual_image)
    pixel_data = ia.getchunk().squeeze()
finally:
    ia.close()

print("--> Residual data loaded. Creating plot...")

fig, ax = plt.subplots(figsize=(10, 10))
zscale = ZScaleInterval()
vmin, vmax = zscale.get_limits(pixel_data)
im = ax.imshow(pixel_data, origin='lower', cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_title('Residual Image (Post-Clean)')
ax.set_xlabel('Right Ascension')
ax.set_ylabel('Declination')
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label('Flux Density')

fig.savefig(output_file)
print(f"--> View of residual image saved to: {output_file}")