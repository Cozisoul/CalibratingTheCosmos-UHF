# calibrate_meerkat.py
# The main pipeline script for the "Calibrating the Cosmos" project.

# 1. ===== IMPORT NECESSARY TASKS =====
from casatasks import flagdata, bandpass, gaincal, applycal, tclean

# 2. ===== DEFINE INPUTS AND OUTPUTS =====
vis_file = '/Users/thapelomasebe/Downloads/1740033067-sdp-l0_2025-07-03T00-22-40_t1w.ms'
bandpass_table = 'cal_tables/bandpass.B'
gain_table = 'cal_tables/gain.G'
output_image = 'images/J1939-6342_UHF' # The base name for our final image

# 3. ===== THE CALIBRATION WORKFLOW =====
print("--- Starting MeerKAT Calibration Pipeline ---")

# STEP 1 & 1a: Flagging Data
print("--> Step 1: Flagging bad data regions...")
# (We can combine these into one call for efficiency in the final script)
flagdata(vis=vis_file, mode='manual', autocorr=True, flagbackup=True)
flagdata(vis=vis_file, mode='manual', spw='0:0~400;2950~3150;3800~4095', flagbackup=True)
print("--> Bad data regions flagged.")

# STEP 2: Bandpass Calibration
print("--> Step 2: Performing Bandpass Calibration...")
good_channels = '0:401~2949;3151~3799'
bandpass(vis=vis_file, caltable=bandpass_table, field='0', refant='m000', solint='inf', combine='scan', solnorm=True, spw=good_channels)
print(f"--> Bandpass calibration complete.")

# STEP 3: Gain Calibration
print("--> Step 3: Performing Gain Calibration...")
gaincal(vis=vis_file, caltable=gain_table, field='0', refant='m000', solint='int', gaintable=[bandpass_table], spw=good_channels)
print(f"--> Gain calibration complete.")

# =================================================================
# STEP 4: Applying All Calibration Solutions
# This step takes our solutions and applies them to the data.
# =================================================================
print("--> Step 4: Applying calibration solutions...")

applycal(
    vis=vis_file,
    field='0',
    gaintable=[bandpass_table, gain_table], # Apply BOTH tables
    interp=['nearest,nearest'],             # Interpolation method
    calwt=True,                             # Calibrate the weights
    flagbackup=True
)

print("--> Calibration solutions applied successfully.")
# =================================================================


# =================================================================
# STEP 5: Imaging the Calibrated Data
# This creates the final image from the corrected data.
# =================================================================
print("--> Step 5: Imaging the calibrated data with tclean...")

tclean(
    vis=vis_file,
    imagename=output_image,
    specmode='mfs',         # Multi-Frequency Synthesis - combine all channels
    imsize=[1024, 1024],    # Image size in pixels (e.g., 1024x1024)
    cell=['5arcsec'],       # Pixel size (e.g., 5 arcseconds)
    weighting='briggs',     # A good general-purpose weighting scheme
    robust=0.5,             # A standard value for the robust parameter
    niter=5000,             # Number of cleaning iterations
    threshold='0.1mJy',     # Cleaning threshold (e.g., 0.1 milli-Janskys)
    interactive=False       # Run non-interactively
)

print(f"--> Imaging complete! Image saved as {output_image}.image")
# =================================================================

print("--- Pipeline Finished ---")