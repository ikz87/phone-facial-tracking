import math
from typing import Union
import numpy as np

class Vec2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]):
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: Union[int, float]):
        if scalar == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return Vec2(self.x / scalar, self.y / scalar)

    def __str__(self):
        return f"Vec2({self.x}, {self.y})"

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: Union[int, float]):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar: Union[int, float]):
        if scalar == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

def dot(a: Union[Vec3, Vec2], b: [Vec3, Vec2]):
    if hasattr(a, 'x') and hasattr(a, 'y') and hasattr(b, 'x') and hasattr(b, 'y'):
        if hasattr(a, 'z') and hasattr(b, 'z'):
            # Vec3 dot product
            return a.x * b.x + a.y * b.y + a.z * b.z
        else:
            # Vec2 dot product
            return a.x * b.x + a.y * b.y
    else:
        raise ValueError("Dot product only accepts Vec3 or Vec2 types.")

def cross(a: Vec3, b: Vec3):
    return Vec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

def normalize(v: Union[Vec3, Vec2]):
    length = math.sqrt(dot(v, v))
    if length == 0:
        return v
    else:
        return v / length

def length(v: Union[Vec3, Vec2]):
    return math.sqrt(dot(v, v))

def distance(a: Union[Vec3, Vec2], b: Union[Vec3, Vec2]):
    return math.sqrt(dot(a - b, a - b))

def angle(a: Union[Vec3, Vec2], b: Union[Vec3, Vec2]):
    return math.degrees(math.acos(dot(normalize(a), normalize(b))))

def rotate(a: Union[Vec3, Vec2], angle):
    angle = math.radians(angle)
    c = math.cos(angle)
    s = math.sin(angle)
    if isinstance(a, Vec3):
        return Vec3(c * a.x - s * a.y, s * a.x + c * a.y, a.z)
    elif isinstance(a, Vec2):
        return Vec2(c * a.x - s * a.y, s * a.x + c * a.y)
    else:
        raise ValueError("Rotation only accepts Vec3 or Vec2 types.")

def orthonormal_basis(a: Vec3):
    # This returns an orthonormal basis with a vector parallell to the xz plane
    # required to generate our camera plane after applying rotations
    a = normalize(a)

    # We want this vector to have zero y-component (parallel to xz-plane).
    # If `a` is not aligned with the z-axis, we can use a vector (a.z, 0, -a.x)
    if a.x != 0 or a.z != 0:
        u = normalize(Vec3(a.z, 0, -a.x))
    else:
        # If `a` is aligned with the z-axis (0, ±1, 0), use a different vector
        # For example, (1, 0, 0) if `a` is pointing along the z-axis
        u = normalize(Vec3(1, 0, 0))
    u *= -1 # Flip it cuz we need that

    # This will ensure `w` is perpendicular to both `a` and `u`.
    w = normalize(cross(a,u))

    return u, w

def rotate_by_azimuth_elevation(a: Vec3, azimuth: float, elevation: float) -> Vec3:
    azimuth = math.radians(azimuth)
    elevation = math.radians(elevation)

    # Elevation rotation around the x-axis (first)
    # x' = a.x
    # y' = cos(elevation) * a.y + sin(elevation) * a.z
    # z' = -sin(elevation) * a.y + cos(elevation) * a.z
    cos_elevation = math.cos(elevation)
    sin_elevation = math.sin(elevation)
    x_elevation = a.x
    y_elevation = cos_elevation * a.y + sin_elevation * a.z
    z_elevation = -sin_elevation * a.y + cos_elevation * a.z
    rotated_elevation = Vec3(x_elevation, y_elevation, z_elevation)

    # Azimuth rotation around the y-axis (second)
    # x'' = cos(azimuth) * rotated_elevation.x - sin(azimuth) * rotated_elevation.z
    # y'' = rotated_elevation.y
    # z'' = sin(azimuth) * rotated_elevation.x + cos(azimuth) * rotated_elevation.z
    cos_azimuth = math.cos(azimuth)
    sin_azimuth = math.sin(azimuth)
    x_final = cos_azimuth * rotated_elevation.x - sin_azimuth * rotated_elevation.z
    y_final = rotated_elevation.y
    z_final = sin_azimuth * rotated_elevation.x + cos_azimuth * rotated_elevation.z

    return Vec3(x_final, y_final, z_final)


def azimuth_elevation_between(v1: Vec3, v2: Vec3):
    # Project both vectors onto the xz-plane for the azimuth angle
    v1_xz = normalize(Vec3(v1.x, 0, v1.z))
    v2_xz = normalize(Vec3(v2.x, 0, v2.z))

    # Calculate the azimuth angle between the xz projections
    dot_xz = dot(v1_xz, v2_xz)
    dot_xz = max(min(dot_xz, 1.0), -1.0)
    azimuth = math.acos(dot_xz) * (180 / math.pi)  # Convert from radians to degrees

    # Determine the sign of the azimuth based on cross product (y-component)
    if v1_xz.x * v2_xz.z - v1_xz.z * v2_xz.x > 0:
        azimuth = -azimuth  # Make azimuth negative if v2 is to the left of v1 in xz-plane

    # Elevation angle is a bit different
    # We gotta take into account both x and z components
    v1_y = normalize(Vec2(length(Vec2(v1.x, v1.z)), v1.y))
    v2_y = normalize(Vec2(length(Vec2(v2.x, v2.z)), v2.y))

    # Calculate the elevation angle between the resulting vectors
    dot_y = dot(v1_y,v2_y)
    dot_y = max(min(dot_y, 1.0), -1.0)
    elevation = math.acos(dot_y) * (180 / math.pi)  # Convert from radians to degrees

    # Determine the sign of the elevation based on z-component
    if v2.y < v1.y:
        elevation = -elevation  # Make elevation negative if v2 is below v1 in yz-plane

    return Vec2(azimuth, elevation)
