# plot_bandpass.py
# A robust script to visualize the bandpass table by reading the data
# directly and plotting with matplotlib.

# 1. ===== IMPORT THE NECESSARY TOOLS AND LIBRARIES =====
from casatools import table
import numpy as np
import matplotlib.pyplot as plt

# 2. ===== CREATE AN INSTANCE OF THE TABLE TOOL =====
# This is the correct way to access any CASA table.
tb = table()

# 3. ===== DEFINE INPUTS AND OUTPUTS =====
bandpass_table = 'cal_tables/bandpass.B'
output_plot_file = 'images/bandpass_amplitude_vs_frequency.png'

# 4. ===== READ DATA PROGRAMMATICALLY =====
print(f"--> Opening calibration table: {bandpass_table}")
try:
    # Open the bandpass table
    tb.open(bandpass_table)

    # Get the complex gain data. The shape is (n_pol, n_channels, n_antennas)
    gains = tb.getcol('CPARAM')
    
    # Get the flags associated with the data
    flags = tb.getcol('FLAG')

finally:
    # It is crucial to close the table tool
    tb.close()

print("--> Successfully read gain data and flags from the table.")

# 5. ===== PLOT THE DATA WITH MATPLOTLIB =====
print(f"--> Creating plot with matplotlib...")

# Get the dimensions from the data array's shape
num_chans = gains.shape[1]
num_ants = gains.shape[2]
channel_numbers = np.arange(num_chans)

# Create a figure and axes for the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Loop through each antenna to plot its solution
for i in range(num_ants):
    # Get the amplitude of the first polarization (XX) for this antenna
    amplitude = np.abs(gains[0, :, i])
    
    # Get the flags for this antenna's data
    antenna_flags = flags[0, :, i]
    
    # Use the flags to mask the bad data so it doesn't get plotted
    masked_amplitude = np.ma.masked_where(antenna_flags, amplitude)
    
    # Plot channel number vs. the masked amplitude
    ax.plot(channel_numbers, masked_amplitude, lw=1) # lw=1 for thin lines

# Set labels and title for the plot
ax.set_xlabel('Channel Number')
ax.set_ylabel('Amplitude')
ax.set_title('Bandpass Amplitude vs. Channel for All Antennas')
ax.grid(True)
ax.set_ylim(0, 2) # Set a reasonable y-axis limit

# 6. ===== SAVE THE PLOT =====
fig.savefig(output_plot_file)

print(f"--> Plot saved successfully to: {output_plot_file}")