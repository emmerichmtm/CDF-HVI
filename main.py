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




def plot_hypervolume_with_contour(points, reference_point, delta):
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
        ax.fill(*rectangle, alpha=0.2, color='gray')

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

    # Enhance plot
    ax.set_xlabel('Objective 1')
    ax.set_ylabel('Objective 2')
    ax.set_title('Hypervolume Representation with Increase Contour')
    ax.grid(True)

    # Show the plot
    plt.show()


# Main section to test the functions
if __name__ == "__main__":

    # Existing functions: remove_dominated_points, hypervolume_indicator, and hypervolume_increase


    # Define points and reference point
    points = [(1, 4), (2, 2), (3, 1), (4, 0)]
    reference_point = (5, 5)
    delta = 1  # Set your delta here

    # Plot the hypervolume with contours showing where increase exceeds delta
    plot_hypervolume_with_contour(points, reference_point, delta)
