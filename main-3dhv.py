import plotly.graph_objects as go

def non_dominated_points(points):
    """ Filters non-dominated points assuming all objectives are to be maximized """
    dominated = set()
    for i, p1 in enumerate(points):
        if i in dominated:
            continue
        for j, p2 in enumerate(points):
            if all(p1[k] >= p2[k] for k in range(len(p1))) and any(p1[k] > p2[k] for k in range(len(p1))):
                dominated.add(j)
    return [points[i] for i in range(len(points)) if i not in dominated]

def draw_box(x, y, z, dx, dy, dz, base_color):
    """Draw a 3D box with each face having a different shade of the base color."""
    # Define the coordinates for each vertex of the box
    v0, v1, v2, v3, v4, v5, v6, v7 = [
        [x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z],
        [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]
    ]

    # Define the vertices for each face
    faces = [
        [v0, v1, v5, v4],  # Front face
        [v1, v2, v6, v5],  # Right face
        [v2, v3, v7, v6],  # Back face
        [v3, v0, v4, v7],  # Left face
        [v0, v3, v2, v1],  # Bottom face
        [v4, v5, v6, v7]   # Top face
    ]

    # Create a list of Plotly Mesh3d objects, one for each face
    box_faces = []
    for i, face in enumerate(faces):
        # Adjust the shade of the base color for each face
        shade = 0.6 + 0.1 * i
        face_color = f'rgba({int(base_color[0] * shade)}, {int(base_color[1] * shade)}, {int(base_color[2] * shade)}, 1)'
        x_coords, y_coords, z_coords = zip(*face)
        box_faces.append(go.Mesh3d(
            x=x_coords, y=y_coords, z=z_coords,
            i=[0, 1, 2, 3], j=[1, 2, 3, 0], k=[2, 3, 0, 1],
            color=face_color,
            opacity=1  # Opaque faces
        ))

    return box_faces

# Define a function to plot a 3-D box with shaded faces given upper and lower bounds
def draw_interval_box(lbx,lby,lbz,ubx,uby,ubz,base_color):
    """Draw a 3D box with each face having a different shade of the base color."""
    # Use function draw_box to draw the box
    # Define dx, dy, dz
    dx = ubx - lbx
    dy = uby - lby
    dz = ubz - lbz
    # assert that dx, dy, dz are positive
    assert dx >= 0 and dy >= 0 and dz >= 0

    # Call draw_box
    return draw_box(lbx, lby, lbz, dx, dy, dz, base_color)

def draw_point(x, y, z, color):
    """ Draw a small ball (point) at a coordinate. """
    return go.Scatter3d(
        x=[x], y=[y], z=[z], mode='markers', marker=dict(color=color, size=5)
    )

def test_draw_anchored_boxes():
    # Example set of points Y
    Y = [[3, 2, 4], [1, 6, 3], [6, 5, 1], [5, 5, 2], [5,3,3], [2, 3, 5],[3,2,5], [1, 1, 6], [2, 5, 2]]
    yplus = [4, 4, 4]
    # Compute non-dominated points
    non_dominated = non_dominated_points(Y)
    # Anchor point
    anchor = [0, 0, 0]
    # Base color for boxes
    base_color = (255, 165, 0)
    plus_color = (0, 255, 0)
    # Point color
    point_color = 'blue'

    # Create a figure and add the boxes for each non-dominated point
    fig = go.Figure()
    for point in non_dominated:
        ubx, uby, ubz = point
        for face in draw_box(0, 0, 0, ubx, uby, ubz, base_color):
            fig.add_trace(face)
        # Draw a point at the upper corner
        fig.add_trace(draw_point(ubx, uby, ubz, point_color))
        ubx_yplus, uby_yplus, ubz_yplus = yplus
        for face_yplus in draw_box(0,0,0,ubx_yplus,uby_yplus,ubz_yplus,plus_color):
            fig.add_trace(face_yplus)
        # draw yplus point
        fig.add_trace(draw_point(ubx_yplus, uby_yplus, ubz_yplus, point_color))

    # Set the layout for the 3D plot
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='f1', nticks=10),
            yaxis=dict(title='f2', nticks=10),
            zaxis=dict(title='f3', nticks=10)
        ),
        margin=dict(r=10, l=10, b=10, t=10)
    )


    # Show the plot
    fig.show()

test_draw_anchored_boxes()

# compute the hypervolume of the non-dominated points
