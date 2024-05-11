import numpy as np
import matplotlib.pyplot as plt

# Function to remove dominated points
def remove_dominated_points(points):
    marker_for_removal = []
    for i in range(len(points)):
        for j in range(len(points)):
            if (points[i][0] < points[j][0] and points[i][1] <= points[j][1]) or (
                    points[i][0] <= points[j][0] and points[i][1] < points[j][1]):
                marker_for_removal.append(j)
    # Create new list of points that are not marked for removal
    points = [points[i] for i in range(len(points)) if i not in marker_for_removal]
    return points


# Function to calculate the 2-D Hypervolume Indicator
def hypervolume_indicator(points, reference_point):
    points = remove_dominated_points(points)
    points = np.array(points)
    reference_point = np.array(reference_point)
    dominated_points = [point for point in points if all(point <= reference_point)]
    dominated_points.sort(key=lambda x: x[0])
    hypervolume = 0.0
    last_point = reference_point
    for point in dominated_points:
        if last_point is not None:
            height = last_point[1] - point[1]
            width = reference_point[0] - point[0]
            hypervolume += height * width
        last_point = point
    return hypervolume

def hypervolume_increase(points, new_point, reference_point):
    # Calculate original hypervolume
    original_hv = hypervolume_indicator(points, reference_point)

    # Calculate hypervolume with the new point added
    new_points = points + [new_point]
    new_hv = hypervolume_indicator(new_points, reference_point)

    # The increase is the difference
    return new_hv - original_hv


def plot_hypervolume_with_contour(points, reference_point, delta, relevant_cells=[]):
    # Calculate hypervolume
    result_hypervolume = hypervolume_indicator(points, reference_point)
    print("Remaining non-dominated points:", remove_dominated_points(points))
    print("Hypervolume Indicator:", result_hypervolume)

    # Create a plot
    fig, ax = plt.subplots()

    # Plot each point and the reference point for context
    for point in points:
        ax.plot(*point, 'ro')  # Red 'o' for points
    ax.plot(*reference_point, 'bo')  # Blue 'o' for the reference point

    # Draw rectangles as shaded areas
    for point in points:
        x, y = point
        ref_x, ref_y = reference_point
        rectangle = [[x, x, ref_x, ref_x], [y, ref_y, ref_y, y]]
        ax.fill(*rectangle, alpha=0.6, color='gray')

    # Set up a grid for hypervolume increase calculations
    x_values = np.linspace(0, reference_point[0], 50)
    y_values = np.linspace(0, reference_point[1], 50)
    X, Y = np.meshgrid(x_values, y_values)
    Z = np.zeros(X.shape)

    for i in range(len(X)):
        for j in range(len(Y)):
            new_point = (X[i, j], Y[i, j])
            Z[i, j] = hypervolume_increase(points, new_point, reference_point)

    # Plot the contour where hypervolume increase exceeds delta
    CS = ax.contour(X, Y, Z, levels=[delta], colors='green', linestyles='dashed')
    ax.clabel(CS, inline=True, fontsize=10, fmt='%1.1f', colors='green')

    # Mark regions with transparent orange
    for lower_corner, upper_corner in relevant_cells:
        ax.add_patch(plt.Rectangle(lower_corner, upper_corner[0] - lower_corner[0], upper_corner[1] - lower_corner[1], color='orange', alpha=0.5))

    # Manually add gridlines at the coordinate levels of the given points
    all_points = points + [reference_point]
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    for p in all_points:
        ax.plot([p[0], p[0]], [y_min, y_max], 'grey', linestyle='--', linewidth=0.5)  # Vertical lines
        ax.plot([x_min, x_max], [p[1], p[1]], 'grey', linestyle='--', linewidth=0.5)  # Horizontal lines

    # Labels and title
    ax.set_xlabel('Objective 1')
    ax.set_ylabel('Objective 2')
    ax.set_title('Hypervolume Representation with Increase Contour')

    # Show the plot
    plt.show()
def find_cells_intersecting_level_curve(points, reference_point, delta):
    """ Identify grid cells based on sorted points and compute detailed hypervolume increases,
        prioritizing y from highest to lowest and then x from smallest to largest. """
    # Sort points by x (smallest to largest) and y (highest to lowest)
    sorted_x = sorted(points, key=lambda x: x[0])
    sorted_y = sorted(points, key=lambda x: x[1], reverse=True)

    relevant_cells = []

    # Iterate over y from highest to lowest
    for j in range(len(sorted_y) - 1):
        # Iterate over x from smallest to largest
        for i in range(len(sorted_x) - 1):
            # Define lower-left and upper-right corners of the cell
            lower_left = (sorted_x[i][0], sorted_y[j + 1][1])
            upper_right = (sorted_x[i + 1][0], sorted_y[j][1])

            # Calculate hypervolume increases at cell corners
            increase_ll = hypervolume_increase(points, lower_left, reference_point)
            increase_ur = hypervolume_increase(points, upper_right, reference_point)

            # Check conditions for including the cell

            if increase_ll > delta and increase_ur < delta:
                relevant_cells.append({
                    "lower_left": lower_left,
                    "upper_right": upper_right,
                    "hv_increase_ll": increase_ll,
                    "hv_increase_ur": increase_ur
                })

    return relevant_cells



# Main section to test the functions
if __name__ == "__main__":
    # Existing functions: remove_dominated_points, hypervolume_indicator, and hypervolume_increase
    # Define points and reference point
    points = [(0,5), (1, 4), (2, 2), (3, 1), (5, 0)]
    reference_point = (5, 5)
    delta = 1  # Set your delta here




    relevant_cells = find_cells_intersecting_level_curve(points, reference_point, delta)

    for cell in relevant_cells:
        print(f"Cell LL: {cell['lower_left']}, UR: {cell['upper_right']}, HV Increase LL: {cell['hv_increase_ll']:.2f}, HV Increase UR: {cell['hv_increase_ur']:.2f}")

    # unpack lower_left and upper_right corners from relevant_cells
    relevant_cells = [(cell['lower_left'], cell['upper_right']) for cell in relevant_cells]


    # Plot the hypervolume with contours showing where increase exceeds delta
    plot_hypervolume_with_contour(points, reference_point, delta, relevant_cells=relevant_cells)
