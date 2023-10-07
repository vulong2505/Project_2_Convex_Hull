# Used Divide and Conquer strategy as planned by https://codecrucks.com/convex-hull-using-divide-and-conquer/

def convex_hull(points):
    """
    Uses Divide & Conquer technique to solve the convex hull problem givne a set of 2D points.

    Args:
        points (list): A list of tuples representing (x, y) coordinates. 

    Returns:
        list: A list of points of the solved convex hull. 
    """

    if len(points) < 3:
        return points

    # Sort the points by x-coordinate (and by y-coordinate as a tie-breaker)
    points.sort(key=lambda p: (p[0], p[1]))

    # Find the leftmost and rightmost points
    A = points[0]
    B = points[-1]

    # Partition points into two subsets based on the line formed by A and B
    S1 = [p for p in points if get_coordinate_side(A, B, p) == 'right']
    S2 = [p for p in points if get_coordinate_side(B, A, p) == 'right']

    # Initialize the hull with points A and B
    hull = [A]

    # Find the hull on the right side of line segment AB and BA
    find_hull(S1, A, B, hull)
    find_hull(S2, B, A, hull)
    hull.append(B)

    return hull


def get_coordinate_side(A, B, P):
    """
    Determines which side P lies on based on line AB.
    
    Args:
        A (tuples): (x, y) coordinates of A
        B (tuples): (x, y) coordinates of B
        P (tuples): (x, y) coordinates of P

    Returns:
        str: Direction of the side that P lies on based on line AB.
    """

    cross_product = (B[0] - A[0]) * (P[1] - A[1]) - (B[1] - A[1]) * (P[0] - A[0])
    if cross_product < 0: return 'right'
    elif cross_product > 0: return 'left'
    return 'on-the-line'


def find_hull(S, A, B, hull):
    """
    Recursion step to solve the hulls of the subset of points. 

    Args:
        S (list): Subset of points to solve
        A (tuple): (x, y) coordinates of A
        B (tuple): (x, y) coordinates of B
        hull (list): Current list of points that represents the final convex hull
    """

    if not S:
        return

    C = max(S, key=lambda p: distance_from_line(A, B, p))
    hull.append(C)

    # Subdivide the points based on their position relative to line segment AC and CB
    S1 = [p for p in S if get_coordinate_side(A, C, p) == 'right']
    S2 = [p for p in S if get_coordinate_side(C, B, p) == 'right']

    # Recursively find the hull for the two subdivisions
    find_hull(S1, A, C, hull)
    find_hull(S2, C, B, hull)


def distance_from_line(A, B, P):
    """
    Calculates the distance of point P from line AB.

    Args:
        A (tuples): (x, y) coordinates of A
        B (tuples): (x, y) coordinates of B
        P (tuples): (x, y) coordinates of P

    Returns:
        (float): Distance of point P from line AB.
    """

    return abs((B[0] - A[0]) * (P[1] - A[1]) - (B[1] - A[1]) * (P[0] - A[0]))

################### PLOT VISUALS

def order_clockwise(hull):
    import math
    # Compute centroid of the hull
    centroid = [sum(x[0] for x in hull) / len(hull), sum(x[1] for x in hull) / len(hull)]
    
    # Sort the points of the hull by polar angle with respect to the centroid
    hull.sort(key=lambda p: (math.atan2(p[1]-centroid[1], p[0]-centroid[0])))
    
    return hull

def plot_points_and_hull(points, hull):
    import matplotlib.pyplot as plt

    # Reorder hull coordinates
    hull = order_clockwise(hull)

    # Extracting x and y coordinates from points
    x_coords, y_coords = zip(*points)
    
    # Extracting x and y coordinates from hull for plotting
    hull_x, hull_y = zip(*hull)
    hull_x = list(hull_x) + [hull_x[0]]
    hull_y = list(hull_y) + [hull_y[0]]

    plt.figure(figsize=(10, 10))

    # Plotting the points
    plt.scatter(x_coords, y_coords, c='blue', label='Points')
    
    # Plotting the hull
    plt.plot(hull_x, hull_y, 'r-', label='Convex Hull')
    
    # Displaying the plot
    plt.title('Visual Test for Convex Hull')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True)
    plt.show()
