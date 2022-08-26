import random

from shapely.geometry import Polygon

from random import triangular

from constants import GRAVITY, AIR_DENSITY
from util.functions import *
from util.vectors import Vector2
from util.vertex import Vertex


# units are all meters and kilograms
class Buoy:
    buoy_count = 1

    def __init__(self,
                 x: float,
                 y: float,
                 width: int,
                 height: int,
                 mass: int,
                 color: tuple = (0, 0, 0)
                 ):
        self.id = Buoy.buoy_count

        self.mass = mass
        self.position = Vector2((x, y))

        self.speed = Vector2()
        self.accel = Vector2()

        self.ang_speed = 0
        self.ang_accel = 0

        self.angle = triangular(-35, 35, 0)  # starts at a random angle, just to make things interesting

        self.submerged_height = 0.0  # for horizontal drag and wind area
        self.submerged_area = 0.0

        self.width = width
        self.height = height
        self.depth = (width + height) // 10

        self.normalised_vertices = [
                                    (0, 0),  # top left
                                    (1, 0),  # top right
                                    (1, 1),  # bottom right
                                    (0, 1),  # bottom left
                                    ]

        # triangle, physics almost work for this as they are (CoB is still a little wrong), but they are not drawn on screen properly
        # rename it normalised_vertices in order to use the triangle
        self.triangle = [
                            (0.5, 1),  # bottom
                            (1, 0),  # top right
                            (0, 0),  # top left
                        ]

        self.vertices = []  # position of vertices in world updated every frame
        for i, vertex in enumerate(self.normalised_vertices):
            origin = Vector2((self.width / 2, self.height / 2)) + self.position
            point = Vector2(vertex) * Vector2((self.width, self.height)) + self.position
            x, y = rotate_around(origin, point, -self.angle)
            next_index = i + 1 if i < len(self.normalised_vertices) - 1 else 0
            vertex = Vertex(i, next_index, (x, y))
            self.vertices.append(vertex)

        self.com = Vector2((self.width / 2, self.height / 2))  # center of mass
        self.cob = Vector2()  # center of buoyancy

        self.drag_coefficient = 1

        self.intersections = []  # intersections of buoy's sides with waterline
        self.vertices_in_order = []  # vertices of the polygon that represents submerged area

        if color != (0, 0, 0):
            self.color = color
        else:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        Buoy.buoy_count += 1

    # return geometrical center, rectangles only
    def get_centroid(self):
        return Vector2(self.width / 2, self.height / 2)

    # place center of mass in geometrical center, for rectangles only
    def get_com(self):
        self.com = Vector2((self.width / 2, self.height / 2))

    # update position of vertices after taking rotation into account
    def update_vertices(self):
        for i, vertex in enumerate(self.normalised_vertices):  # use zip() here
            origin = Vector2((self.width / 2, self.height / 2)) + self.position
            point = Vector2(vertex) * Vector2((self.width, self.height)) + self.position
            x, y = rotate_around(origin, point, -self.angle)
            self.vertices[i].coord = Vector2(x, y)
            self.vertices[i].submerged = False

    # main physics function
    def get_submerged_vertices(self, water_level: float):
        self.intersections = []
        self.update_vertices()

        # find which vertices are underwater
        submerged_vertices = []
        for vertex in self.vertices:
            if vertex.coord.y > water_level:
                vertex.submerged = True
                submerged_vertices.append(vertex)
        submerged_indices = [x.index for x in submerged_vertices]

        # if totally out of the water
        if len(submerged_vertices) <= 0:
            self.submerged_area = 0.0
            self.cob = Vector2()

        # if partially submerged, with more than 1 but fewer than all vertices submerged
        elif 0 < len(submerged_vertices) < len(self.vertices):
            vertex_order = []  # store order to draw polygon correctly

            # find edges that intersect water line
            for index in range(len(self.vertices)):
                right = index + 1
                if right > len(self.normalised_vertices) - 1:
                    right = 0

                # get points of intersection with water
                if (index in submerged_indices and right not in submerged_indices) or (index not in submerged_indices and right in submerged_indices):

                    current_vertex = self.vertices[index].coord
                    right_vertex = self.vertices[right].coord

                    # calculate slope while avoiding DivZero if dx == 0
                    dx = (current_vertex.x - right_vertex.x)
                    if dx != 0:
                        dy = (current_vertex.y - right_vertex.y)
                        m = dy / dx
                        x = current_vertex.x + (water_level - current_vertex.y) / m
                    else:
                        x = current_vertex.x

                    intersection = Vector2(x, water_level)
                    self.intersections.append(intersection)

                    if index in submerged_indices and index not in vertex_order:  # "index not in vertex_order" check just to avoid adding same vertex twice
                        vertex_order.append(index)
                    elif right in submerged_indices and right not in vertex_order:
                        vertex_order.append(right)

            # reorder intersections (left must be the first element in list)
            if self.intersections[1].x < self.intersections[0].x:
                self.intersections.sort(key=lambda x: x.x, reverse=False)

            # calculate submerged height for drag calculation
            lowest_vertex_y = min([x.coord.y for x in self.vertices if x.submerged])
            self.submerged_height = abs(self.intersections[0].y - lowest_vertex_y)

            vertex_order = [x.index for x in submerged_vertices]  # create list of just indices (maybe remove those extra lists...?)
            vertex_order.sort(reverse=True)  # sometimes 3 must come before 0, so this function does not work 100% of the time, added quick fix below

            # quick fix to keep vertices in the right order
            if vertex_order == [3, 1, 0]:
                vertex_order = [1, 0, 3]
            elif vertex_order == [3, 0]:
                vertex_order = [0, 3]
            elif vertex_order == [3, 2, 0]:
                vertex_order = [0, 3, 2]
            elif vertex_order == [1, 2]:
                vertex_order = [2, 1]

            ordered_vertex_positions = [self.vertices[x].coord for x in vertex_order]
            self.vertices_in_order = [self.intersections[0].components()] + unpack_vector_list(ordered_vertex_positions) + [self.intersections[1].components()]

            # get area and centroid with Shapely
            polygon = Polygon(self.vertices_in_order)
            self.submerged_area = polygon.area
            self.cob.x, self.cob.y = polygon.centroid.x, polygon.centroid.y
            self.cob = self.cob - self.position  # always relative to top-left corner

        # if all vertices are submerged
        elif len(submerged_vertices) == len(self.vertices):
            self.cob = Vector2(self.width / 2, self.height / 2)
            self.submerged_area = self.width * self.height

            lowest_vertex_y = min([x.coord.y for x in self.vertices])
            highest_vertex_y = max([x.coord.y for x in self.vertices])
            self.submerged_height = abs(highest_vertex_y - lowest_vertex_y)

            self.vertices_in_order = unpack_vector_list([x.coord for x in submerged_vertices])

    def translation(self, water, wind_strength, time_delta: float):
        summation = Vector2()

        weight = self.mass * GRAVITY

        drag = Vector2()
        if self.submerged_area > 0:
            buoyancy = water.density * GRAVITY * self.submerged_area * self.depth
            drag.x = 0.5 * water.density * pow(self.speed.x, 2) * self.drag_coefficient * self.submerged_height * self.depth
            drag.y = 0.5 * water.density * pow(self.speed.y, 2) * self.drag_coefficient * self.width * self.depth
        else:
            buoyancy = 0.0
            drag.x = 0.5 * AIR_DENSITY * pow(self.speed.x, 2) * self.drag_coefficient * self.height * self.depth
            drag.y = 0.5 * AIR_DENSITY * pow(self.speed.y, 2) * self.drag_coefficient * self.width * self.depth
        drag.x *= -1 if self.speed.x > 0 else 1
        drag.y *= -1 if self.speed.y > 0 else 1

        # horizontal
        def completely_submerged(vertices):
            for vertex in vertices:
                if not vertex.submerged:
                    return False
            return True
        if not completely_submerged(self.vertices):
            lowest_vertex_y = max([x.coord.y for x in self.vertices])
            highest_vertex_y = min([x.coord.y for x in self.vertices if x.submerged is False])
            wind_height = (lowest_vertex_y - highest_vertex_y) - self.submerged_height  # only area above waterline is affected by wind
        else:
            wind_height = 0
        wind_force = wind_strength * self.depth * wind_height
        summation.x = wind_force + drag.x
        self.accel.x = summation.x / self.mass
        self.speed.x += self.accel.x * time_delta
        self.position.x += (self.speed.x * time_delta + (self.accel.x * pow(time_delta, 2)) / 2)

        # vertical
        summation.y = weight - buoyancy + drag.y
        self.accel.y = summation.y / self.mass
        self.speed.y += self.accel.y * time_delta
        self.position.y += (self.speed.y * time_delta + (self.accel.y * pow(time_delta, 2)) / 2)

    def rotation(self, water, time_delta: float):
        # calculate torque and drag
        multiplier = 1000  # looks better with exaggerated drag
        if self.submerged_area > 0:
            rotated_com = rotate_around(self.get_centroid() + self.position, self.com + self.position, -self.angle)
            leverage = self.cob.x + self.position.x - rotated_com[0]  # rotated_com is absolute so cob needs position in order to follow same coordinates system
            torque = leverage * self.mass
            ang_drag = 0.5 * water.density * pow(self.ang_speed, 2) * self.drag_coefficient * self.width * self.depth * multiplier  # insignificant without a multiplier
        else:
            torque = 0
            ang_drag = 0.5 * AIR_DENSITY * pow(self.ang_speed, 2) * self.drag_coefficient * self.width * self.depth * multiplier
        ang_drag *= -1 if self.ang_speed > 0 else 1

        summation = torque + ang_drag

        # calculate new angle
        inertial_moment = 20000000000  # moment of inertia is always the same
        self.ang_accel = summation / inertial_moment
        self.ang_speed += self.ang_accel * time_delta
        delta_angle = self.ang_speed * time_delta + self.ang_accel * pow(time_delta, 2) / 2
        self.angle += delta_angle

        # calculate new, rotated position of top-left corner
        geometrical_center = Vector2(self.width / 2, self.height / 2)
        rotated_center = Vector2(rotate_around(self.cob + self.position, geometrical_center + self.position, -delta_angle))  # must use the delta, not self.angle
        self.position = Vector2(rotate_around(rotated_center, self.position, -delta_angle))

    def __str__(self):
        return f'id{self.id}  position: {self.position}\nspeed: {self.speed}\naccel: {self.accel}\n' + '—' * 10
