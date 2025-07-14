# calibrate_meerkat.py
# The main pipeline script for the "Calibrating the Cosmos" project.

import os
import argparse
from casatasks import flagdata, bandpass, gaincal, applycal, tclean

def flag_bad_data(vis_file):
    """
    Flags bad data regions in the visibility file.
    """
    print("--> Step 1: Flagging bad data regions...")
    flagdata(
        vis=vis_file,
        mode='manual',
        autocorr=True,
        spw='0:0~400;2950~3150;3800~4095',
        flagbackup=True
    )
    print("--> Bad data regions flagged.")

def perform_bandpass_calibration(vis_file, bandpass_table, good_channels):
    """
    Performs bandpass calibration.
    """
    print("--> Step 2: Performing Bandpass Calibration...")
    bandpass(
        vis=vis_file,
        caltable=bandpass_table,
        field='0',
        refant='m000',
        solint='inf',
        combine='scan',
        solnorm=True,
        spw=good_channels
    )
    print(f"--> Bandpass calibration complete.")

def perform_gain_calibration(vis_file, gain_table, bandpass_table, good_channels):
    """
    Performs gain calibration.
    """
    print("--> Step 3: Performing Gain Calibration...")
    gaincal(
        vis=vis_file,
        caltable=gain_table,
        field='0',
        refant='m000',
        solint='int',
        gaintable=[bandpass_table],
        spw=good_channels
    )
    print(f"--> Gain calibration complete.")

def apply_calibration_solutions(vis_file, bandpass_table, gain_table):
    """
    Applies calibration solutions to the data.
    """
    print("--> Step 4: Applying calibration solutions...")
    applycal(
        vis=vis_file,
        field='0',
        gaintable=[bandpass_table, gain_table],
        interp=['nearest,nearest'],
        calwt=True,
        flagbackup=True
    )
    print("--> Calibration solutions applied successfully.")

def image_calibrated_data(vis_file, output_image):
    """
    Images the calibrated data using tclean.
    """
    print("--> Step 5: Imaging the calibrated data with tclean...")
    tclean(
        vis=vis_file,
        imagename=output_image,
        specmode='mfs',
        imsize=[1024, 1024],
        cell=['5arcsec'],
        weighting='briggs',
        robust=0.5,
        niter=5000,
        threshold='0.1mJy',
        interactive=False
    )
    print(f"--> Imaging complete! Image saved as {output_image}.image")

def main():
    """
    The main function to run the MeerKAT calibration pipeline.
    """
    parser = argparse.ArgumentParser(description="MeerKAT Calibration Pipeline")
    parser.add_argument("vis_file", help="Input visibility file (.ms)")
    parser.add_argument("--cal_table_dir", default="cal_tables", help="Directory for calibration tables")
    parser.add_argument("--output_dir", default="images", help="Directory for output images")
    args = parser.parse_args()

    # Check if the visibility file exists
    if not os.path.exists(args.vis_file):
        print(f"Error: Visibility file not found at {args.vis_file}")
        return

    # Create output directories if they don't exist
    os.makedirs(args.cal_table_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)

    bandpass_table = os.path.join(args.cal_table_dir, 'bandpass.B')
    gain_table = os.path.join(args.cal_table_dir, 'gain.G')
    output_image = os.path.join(args.output_dir, 'J1939-6342_UHF')
    good_channels = '0:401~2949;3151~3799'

    print("--- Starting MeerKAT Calibration Pipeline ---")

    flag_bad_data(args.vis_file)
    perform_bandpass_calibration(args.vis_file, bandpass_table, good_channels)
    perform_gain_calibration(args.vis_file, gain_table, bandpass_table, good_channels)
    apply_calibration_solutions(args.vis_file, bandpass_table, gain_table)
    image_calibrated_data(args.vis_file, output_image)

    print("--- Pipeline Finished ---")

if __name__ == "__main__":
    main()