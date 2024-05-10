# Hypervolume Indicator Visualization

## Overview
This project includes Python scripts designed to visualize the hypervolume indicator in a two-dimensional objective space. The hypervolume indicator is a useful metric in multi-objective optimization, helping to quantify the space covered by a set of points relative to a reference point. The scripts allow for the calculation of hypervolume increases and visualize these increases through shaded areas and contour lines in plots.

### Scripts Description
- `main.py`: Visualizes the hypervolume covered by a set of points and the areas where the hypervolume increases significantly when new points are added.
- `main_level_curve_with_correlated_gaussian.py`: Extends the basic visualization by overlaying a contour plot of a correlated Gaussian distribution, offering insights into probabilistic modeling aspects on top of the optimization landscape.

## Features
- **Calculate Hypervolume**: Compute the hypervolume covered by a set of points.
- **Visualize Increases**: Display areas where adding a new point exceeds a specified increase in hypervolume.
- **Interactive Contours**: Plot contour lines to show critical thresholds where the hypervolume increase is significant.
- **Overlay Gaussian Contour**: Integrate a correlated Gaussian distribution to provide a statistical perspective on the objective space.

## Prerequisites
Before you can run these scripts, make sure you have the following installed:
- Python 3.6 or newer
- NumPy
- Matplotlib
- SciPy

You can install the necessary Python packages using pip:
```bash
pip install numpy matplotlib scipy
