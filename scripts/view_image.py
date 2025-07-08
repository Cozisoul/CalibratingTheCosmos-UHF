# view_image.py
# A script to view the final FITS image using astropy and matplotlib.

from astropy.io import fits
from astropy.visualization import ZScaleInterval
import matplotlib.pyplot as plt
import numpy as np

# Define the path to your FITS file
fits_file = 'images/J1939-6342_UHF.fits'

print(f"--> Opening FITS file: {fits_file}")

# Open the FITS file
with fits.open(fits_file) as hdul:
    # The image data is usually in the primary "HDU" (Header Data Unit)
    # The data is often in a 4D cube (RA, Dec, Freq, Stokes)
    # We take a slice to get the 2D image data.
    image_data = hdul[0].data.squeeze()

print("--> FITS data loaded. Creating plot...")

# Create a figure and axes
fig, ax = plt.subplots(figsize=(10, 10))

# Use ZScale for good astronomical contrast
zscale = ZScaleInterval()
vmin, vmax = zscale.get_limits(image_data)

# Display the image
im = ax.imshow(image_data, origin='lower', cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_title('J1939-6342 (Calibrated)')
ax.set_xlabel('Right Ascension')
ax.set_ylabel('Declination')
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label('Flux Density')

# Save the plot
output_file = 'images/final_image_view.png'
fig.savefig(output_file)

print(f"--> View of final image saved to: {output_file}")
