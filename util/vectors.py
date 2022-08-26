from math import atan2


class Vector2:
    def __init__(self, *args
                 ):
        if len(args) == 0:
            self.x = 0.0
            self.y = 0.0
        elif len(args) == 1:
            if type(args[0]) is Vector2:
                self.x = args[0].x
                self.y = args[0].y
            else:  # if list of tuple
                self.x = args[0][0]
                self.y = args[0][1]
        elif len(args) == 2:  # if two ints or floats
            self.x = args[0]
            self.y = args[1]
        else:
            raise Exception(f'Vector2 needs two or fewer arguments but {len(args)} were passed!')

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def angle(self):
        return atan2(self.x, self.y)

    def components(self):
        return [self.x, self.y]

    def __add__(self, other):
        if type(other) == Vector2:
            x = self.x + other.x
            y = self.y + other.y
        elif type(other) == int or type(other) == float:
            x = self.x + other
            y = self.y + other
        else:
            raise Exception(f'Cannot add Vector2 to {type(other)}')
        return Vector2(x, y)

    def __sub__(self, other):
        if type(other) == Vector2:
            x = self.x - other.x
            y = self.y - other.y
        elif type(other) == int or type(other) == float:
            x = self.x - other
            y = self.y - other
        else:
            raise Exception(f'Cannot subtract Vector2 by {type(other)}')
        return Vector2(x, y)

    def __mul__(self, other):
        if type(other) == Vector2:
            x = self.x * other.x
            y = self.y * other.y
        elif type(other) == int or type(other) == float:
            x = self.x * other
            y = self.y * other
        else:
            raise Exception(f'Cannot multiply Vector2 by {type(other)}')
        return Vector2(x, y)

    def __truediv__(self, other):
        if type(other) == Vector2:
            x = self.x / other.x
            y = self.y / other.y
        elif type(other) == int or type(other) == float:
            x = self.x / other
            y = self.y / other
        else:
            raise Exception(f'Cannot divide Vector2 by {type(other)}')
        return Vector2(x, y)

    def __floordiv__(self, other):
        if type(other) == Vector2:
            x = self.x // other.x
            y = self.y // other.y
        elif type(other) == int or type(other) == float:
            x = self.x // other
            y = self.y // other
        else:
            raise Exception(f'Cannot floor divide Vector2 by {type(other)}')
        return Vector2(x, y)

    def __str__(self):
        return f'x{self.x:.2f}  y{self.y:.2f}'


class Vector3:
    def __init__(self, *args):
        if len(args) == 0:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
        elif len(args) == 1:
            if type(args[0]) is Vector3:
                self.x = args[0].x
                self.y = args[0].y
                self.z = args[0].z
            else:  # if list of tuple
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
        elif len(args) == 3:  # if two ints or floats
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]
        else:
            raise Exception(f'Vector3 needs zero, one or three arguments but {len(args)} were passed!')

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def angle(self):
        return atan2(self.x, self.y)

    def components(self):
        return self.x, self.y, self.z

    def __add__(self, other):
        if type(other) == Vector3:
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
        elif type(other) == int or type(other) == float:
            x = self.x + other
            y = self.y + other
            z = self.z + other
        else:
            raise Exception(f'Cannot add Vector3 to {type(other)}')
        return Vector3(x, y, z)

    def __sub__(self, other):
        if type(other) == Vector3:
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
        elif type(other) == int or type(other) == float:
            x = self.x - other
            y = self.y - other
            z = self.z - other
        else:
            raise Exception(f'Cannot subtract Vector3 by {type(other)}')
        return Vector3(x, y, z)

    def __mul__(self, other):
        if type(other) == Vector3:
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
        elif type(other) == int or type(other) == float:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        else:
            raise Exception(f'Cannot multiply Vector3 by {type(other)}')
        return Vector3(x, y, z)

    def __truediv__(self, other):
        if type(other) == Vector3:
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
        elif type(other) == int or type(other) == float:
            x = self.x / other
            y = self.y / other
            z = self.z / other
        else:
            raise Exception(f'Cannot divide Vector3 by {type(other)}')
        return Vector3(x, y, z)

    def __floordiv__(self, other):
        if type(other) == Vector3:
            x = self.x // other.x
            y = self.y // other.y
            z = self.z // other.z
        elif type(other) == int or type(other) == float:
            x = self.x // other
            y = self.y // other
            z = self.z // other
        else:
            raise Exception(f'Cannot floor divide Vector3 by {type(other)}')
        return Vector3(x, y, z)

    def __str__(self):
        return f'x{self.x:.2f}  y{self.y:.2f}  z{self.z:.2f}'