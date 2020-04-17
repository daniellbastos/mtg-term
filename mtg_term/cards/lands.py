from mtg_term.constants import BLACK, BLUE, GREEN, RED, WHITE


class Land:
    def __init__(self, cost=1):
        self.cost = cost

    def __str__(self):
        return self.color

    def __eq__(self, other_land):
        return self.color == other_land.color

    def __lt__(self, other_land):
        return self.color < other_land.color

    def __gt__(self, other_land):
        return self.color > other_land.color


class Forest(Land):
    color = GREEN

    def __repr__(self):
        return f'<Forest {self}>'


class Island(Land):
    color = BLUE

    def __repr__(self):
        return f'<Island {self}>'


class Plains(Land):
    color = WHITE

    def __repr__(self):
        return f'<Plains {self}>'


class Swamp(Land):
    color = BLACK

    def __repr__(self):
        return f'<Swamp {self}>'


class Mountain(Land):
    color = RED

    def __repr__(self):
        return f'<Mountain {self}>'
