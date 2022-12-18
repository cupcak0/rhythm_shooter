class Vector:
    def __init__(self, size=0, values=None):
        if values is None:
            self.vec = [0.0 for _ in range(size)]
        else:
            self.vec = values
            size = len(values)
        self.size = size
        self.type = Vector

    def __getitem__(self, key):
        return self.vec[key]

    def __setitem__(self, key, value):
        self.vec[key] = value

    def __getx__(self):
        return self.vec

    def __setx__(self, value):
        if len(value) != self.size:
            raise AttributeError(f'Size error {len(value)} != {self.size}')
        self.vec = value

    def __len__(self):
        return self.size

    def __add__(self, other):
        if len(self) == len(other):
            return self.type(values=[self[i] + other[i] for i in range(len(self))])
        elif len(self) > len(other):
            return self.type(values=[self[i] + other[i] if i < len(other) else self[i] for i in range(len(self))])
        else:
            return other.type(values=[self[i] + other[i] if i < len(self) else other[i] for i in range(len(other))])

    def __sub__(self, other):
        if len(self) == len(other):
            return self.type(values=[self[i] - other[i] for i in range(len(self))])
        elif len(self) > len(other):
            return self.type(values=[self[i] - other[i] if i < len(other) else self[i] for i in range(len(self))])
        else:
            return other.type(values=[self[i] - other[i] if i < len(self) else other[i] for i in range(len(other))])

    def __mul__(self, other):
        return self.type(values=[self[i] * float(other) for i in range(len(self))])

    def __truediv__(self, other):
        return self.type(values=[self[i] / float(other) for i in range(len(self))])

    def __floordiv__(self, other):
        return self.type(values=[self[i] // float(other) for i in range(len(self))])

    def __str__(self):
        return '(' + ', '.join(map(str, self)) + ')'

    def __repr__(self):
        return f'Vector({self.size})(' + ', '.join(map(str, self)) + ')'

    def length(self):
        a = self[0]
        for i in range(1, len(self)):
            b = self[i]
            a = (a*a+b*b)**0.5
        return a

    def normalized(self):
        mx = max(self)
        return self.type(values=[self[i] / mx for i in range(len(self))])

    def normalize(self):
        self = self.normalized()


class Vector3(Vector):
    def __init__(self, values=None):
        super().__init__(size=3, values=values)
        self.type = Vector3

    def __repr__(self):
        return 'Vector3(' + ', '.join(map(str, self)) + ')'


class Vector2(Vector):
    def __init__(self, values=None):
        super().__init__(size=2, values=values)
        self.type = Vector2

    def __repr__(self):
        return 'Vector2(' + ', '.join(map(str, self)) + ')'


class Vector4(Vector):
    def __init__(self, values=None):
        super().__init__(size=4, values=values)
        self.type = Vector4

    def __repr__(self):
        return 'Vector4(' + ', '.join(map(str, self)) + ')'
