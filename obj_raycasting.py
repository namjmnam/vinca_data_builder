import pandas as pd
import numpy as np
import pywavefront
from datetime import datetime
import logging
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import os

def load_obj(filename):
    scene = pywavefront.Wavefront(filename, collect_faces=True)
    vertices = []
    for mesh in scene.mesh_list:
        for face in mesh.faces:
            vertices.append([scene.vertices[index] for index in face])
    return np.array(vertices)

def ray_intersect_triangle(ray_origin, ray_direction, triangle, tolerance=1e-6):
    v0, v1, v2 = triangle
    edge1 = v1 - v0
    edge2 = v2 - v0
    h = np.cross(ray_direction, edge2)
    a = np.dot(edge1, h)

    if abs(a) < tolerance:
        return None

    f = 1.0 / a
    s = ray_origin - v0
    u = f * np.dot(s, h)

    if u < 0.0 or u > 1.0:
        return None

    q = np.cross(s, edge1)
    v = f * np.dot(ray_direction, q)

    if v < 0.0 or u + v > 1.0:
        return None

    t = f * np.dot(edge2, q)

    if t > tolerance:
        intersection = ray_origin + ray_direction * t
        return intersection
    return None

def classify_ray_hit(ray_origin, ray_direction, obj_file):
    triangles = load_obj(obj_file)
    hit_classification = []

    for triangle in triangles:
        result = ray_intersect_triangle(ray_origin, ray_direction, triangle)
        if result is not None:
            intersection = result
            hit_classification.append(intersection)
    return hit_classification

def raycasting():
    # Set logging level for pywavefront to ERROR to suppress warnings
    logging.getLogger('pywavefront').setLevel(logging.ERROR)

    # obj 파일 입력받기
    root = tk.Tk()
    root.withdraw()  # Tk 창을 숨깁니다

    # Get the script directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    obj_file = filedialog.askopenfilename(filetypes=[("OBJ files", "*.obj")], initialdir=script_directory)
    if not obj_file:
        raise ValueError("No file selected")

    # 사용자로부터 coord_range와 scale 입력 받기
    root = tk.Tk()
    root.withdraw()  # Tk 창을 숨깁니다
    coord_range = simpledialog.askinteger("Input", "Enter the coordinate range plus minus:", minvalue=1, maxvalue=100, initialvalue=30)
    scale = simpledialog.askfloat("Input", "Number of points in 1 unit:", minvalue=0.01, maxvalue=10.0, initialvalue=5)
    if coord_range is None or scale is None:
        raise ValueError("You must enter both coord_range and scale")

    # Record start time
    start_time = datetime.now()
    print("Start time:", start_time.strftime("%Y-%m-%d %H:%M:%S"))

    vertices = load_obj(obj_file)
    x_coords, y_coords, z_coords = zip(*vertices)

    # Plot all the checking points
    hit_points = []
    # coord_range = 15
    # scale = 1/10
    for x in range(-coord_range, coord_range+1):
        print('Progress: ', x+coord_range, ' / ', 2*coord_range)
        for y in range(-coord_range, coord_range+1):
            # Shoot from above
            origin = [x/scale, y/scale, 5]
            intersections = classify_ray_hit(origin, np.array([0, 0, -1]), obj_file)
            l = len(intersections)
            if l!=0:
                for point in intersections:
                    point[2] = round(point[2]*scale)/scale
                # print(intersections)
                highest_z_point = max(intersections, key=lambda x: x[2])
                lowest_z_point = min(intersections, key=lambda x: x[2])
                # print(highest_z_point, lowest_z_point)

                height = highest_z_point[2] - lowest_z_point[2]
                hit_points.append(highest_z_point)
                if height > 0:
                    hit_points.append(lowest_z_point)

                # Fill between top and bottom
                counter = 0
                while counter < height:
                    counter += 1/scale
                    filling_point = [x/scale, y/scale, lowest_z_point[2]+counter]
                    filling_point[2] = round(filling_point[2]*scale)/scale
                    hit_points.append(filling_point)

    # Record end time
    end_time = datetime.now()
    print("End time:", end_time.strftime("%Y-%m-%d %H:%M:%S"))

    # Calculate the difference
    time_difference = end_time - start_time
    print("Time taken:", time_difference)

    # 데이터프레임화
    data = pd.DataFrame(hit_points, columns=["X", "Y", "Z"])
    data = data.drop_duplicates(keep="first")
    return data, scale