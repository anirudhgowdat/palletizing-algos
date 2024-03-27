def dominates(point1, point2):
    """
    Check if point1 dominates point2 in both dimensions.
    """
    return point1[0] <= point2[0] and point1[1] <= point2[1]

def incremental_skyline(points):
    """
    Compute the skyline points using the Incremental Skyline algorithm.
    """
    skyline_points = []
    
    for point in points:
        dominated = False
        to_remove = []
        
        for idx, skyline_point in enumerate(skyline_points):
            if dominates(skyline_point, point):
                dominated = True
                break
            if dominates(point, skyline_point):
                to_remove.append(idx)
                
        if not dominated:
            for idx in reversed(to_remove):
                skyline_points.pop(idx)
            skyline_points.append(point)
            
    return skyline_points

if __name__ == "__main__":
    points = [(1, 4), (3, 6), (2, 2), (5, 3), (7, 5), (4, 7)]
    
    print("Input Points:")
    for point in points:
        print(point)
        
    skyline_points = incremental_skyline(points)
    
    print("\nSkyline Points:")
    for point in skyline_points:
        print(point)
