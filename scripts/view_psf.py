# view_psf.py
# A script to view the Point Spread Function (PSF).

from casatools import image
import matplotlib.pyplot as plt

ia = image()

psf_image = 'images/J1939-6342_UHF.psf'
output_file = 'images/psf_image_view.png'

print(f"--> Opening CASA image: {psf_image}")

try:
    ia.open(psf_image)
    pixel_data = ia.getchunk().squeeze()
finally:
    ia.close()

print("--> PSF data loaded. Creating plot...")

# For the PSF, a logarithmic scale often works best to see the faint structure
from astropy.visualization import LogStretch, ImageNormalize
norm = ImageNormalize(pixel_data, stretch=LogStretch())

fig, ax = plt.subplots(figsize=(10, 10))
im = ax.imshow(pixel_data, origin='lower', cmap='hot', norm=norm)
ax.set_title('Point Spread Function (PSF)')
ax.set_xlabel('Offset')
ax.set_ylabel('Offset')
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label('Response')

fig.savefig(output_file)
print(f"--> View of PSF image saved to: {output_file}")