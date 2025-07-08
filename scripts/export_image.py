# export_image.py
# A script to convert the final CASA image into a FITS file.

# 1. ===== IMPORT THE TASK =====
from casatasks import exportfits

# 2. ===== DEFINE INPUTS AND OUTPUTS =====
# The CASA image created by tclean
input_image = 'images/J1939-6342_UHF.image'

# The name of our final, portable FITS file
output_fits = 'images/J1939-6342_UHF.fits'

# 3. ===== EXPORT THE IMAGE =====
print(f"--> Exporting {input_image} to FITS format...")

exportfits(
    imagename=input_image,
    fitsimage=output_fits,
    overwrite=True  # Overwrite the FITS file if it already exists
)

print("--- Success! ---")
print(f"--> Your final image has been saved as: {output_fits}")