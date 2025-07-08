# test_pipeline.py
# A script to be run by CASA's Python interpreter.

# These import statements must have NO spaces or tabs before them.
from casatasks import listobs
import os
import sys

# This print statement is at the top level, so it also has no indentation.
print("--- Starting CASA Test Script ---")

# --- IMPORTANT ---
# Replace this with the real, full path to your data!
# Example: '/Users/thapelomasebe/Downloads/1740033067.ms'
vis_file = '/Users/thapelomasebe/Downloads/1740033067-sdp-l0_2025-07-03T00-22-40_t1w.ms'
# --- --- --- ---

# This 'if' statement is at the top level, so it has no indentation.
if not os.path.isdir(vis_file):
    # These print statements are INSIDE the 'if' block, so they MUST be indented.
    # The standard is 4 spaces.
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(f"!! ERROR: Cannot find the visibility file at:")
    print(f"!! {vis_file}")
    print("!! Please edit test_pipeline.py and fix the path.")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    sys.exit(1) # This is also inside the 'if' block.
else:
    # These print statements are INSIDE the 'else' block, so they MUST be indented.
    print(f"Found visibility file. Running listobs...")
    print("This may take a moment...")

    # This is also inside the 'else' block.
    output_log_file = 'listobs_summary.txt'

    # This function call is inside the 'else' block.
    listobs(vis=vis_file, listfile=output_log_file, overwrite=True)
    
    # This print statement is also inside the 'else' block.
    print(f"--- listobs complete. ---")

# These final print statements are back at the top level, so they have no indentation.
print(f"--- A summary has been saved to: {output_log_file} ---")
print("--- Script Finished Successfully ---")