import sys
import itertools
from collections import defaultdict
from enum import Enum
from sortedcontainers import SortedList
from typing import Optional

def insert_ival(ivals: SortedList, ival: tuple[int,int]):
    idx = ivals.bisect_left(ival)

    if idx == len(ivals):
        ivals.add(ival)
        return
    
    to_remove = []
    merged_ival = ival
    if idx > 0 and ivals[idx-1][1] >= ival[0]:
        to_remove.append(idx-1)
        merged_ival = (ivals[idx-1][0], max(ivals[idx-1][1],ival[1]))

    while idx < len(ivals) and ivals[idx][0] <= merged_ival[1]:
        merged_ival = (merged_ival[0], max(ivals[idx][1], merged_ival[1]))
        to_remove.append(idx)
        idx += 1

    for i in to_remove[::-1]:
        del ivals[i]

    ivals.add(merged_ival)

class IvalLoc(Enum):
    INT = 0
    UPPER = 1
    LOWER = -1
    OUT = None

def is_contained(ivals: SortedList, val: int) -> IvalLoc:
    idx = ivals.bisect_left((val,-1))
    
    if (idx < len(ivals) and ivals[idx][0] == val):
        return IvalLoc.LOWER
    
    if (idx > 0 and ivals[idx-1][1] > val):
        return IvalLoc.INT
    
    if (idx > 0 and ivals[idx-1][1] == val):
        return IvalLoc.UPPER
    
    return IvalLoc.OUT

class Floor:
    def __init__(self, red_tiles: list[tuple[int,int]]):
        # vertical and horizontal edges keyed by x,y location, respectively
        # what about overlapping edges?
        self.verts = defaultdict(lambda: SortedList(key=lambda x:x[0]))
        self.hors = defaultdict(lambda: SortedList(key=lambda x:x[0]))
        for i in range(len(red_tiles)):
            if red_tiles[i][0] == red_tiles[i-1][0]:
                insert_ival(self.verts[red_tiles[i][0]], (min(red_tiles[i][1], red_tiles[i-1][1]), max(red_tiles[i][1], red_tiles[i-1][1])))
            else:
                insert_ival(self.hors[red_tiles[i][1]], (min(red_tiles[i][0], red_tiles[i-1][0]), max(red_tiles[i][0], red_tiles[i-1][0])))

        self.int_cache: dict[tuple[int,int],bool] = {}
        self.vedge_cache: dict[tuple[int,int], bool] = {}
        self.hedge_cache: dict[tuple[int,int], bool] = {}

    def on_hedge(self, pt: tuple[int,int]) -> bool:
        if pt in self.hedge_cache:
            return self.hedge_cache[pt]
        
        self.hedge_cache[pt] = is_contained(self.hors[pt[1]], pt[0]) != IvalLoc.OUT

        return self.hedge_cache[pt]
    
    def on_vedge(self, pt: tuple[int,int]) -> bool:
        if pt in self.vedge_cache:
            return self.vedge_cache[pt]
        
        self.vedge_cache[pt] = is_contained(self.verts[pt[0]], pt[1]) != IvalLoc.OUT

        return self.vedge_cache[pt]
    
    # send out horizontal rays at height y, count vertical edge crossings between xmin and xmax
    def hray_cast(self, y: int, xmin: int, xmax: Optional[int] = None) -> int:
        counts: int = 0
        broken_edge: IvalLoc = IvalLoc.OUT
        for x,ival in self.verts.items():
            if x <= xmin:
                continue

            if xmax is not None and x >= xmax:
                continue
            
            c = is_contained(ival, y)

            if c == IvalLoc.OUT:
                continue

            if c == IvalLoc.INT:
                counts += 1
                continue

            # deal with 'broken' vertical intersections:
            #
            #          |                |   |
            # - - - --- - - - - -- - - - --- - - ->
            #      |

            if broken_edge == IvalLoc.OUT:
                broken_edge = c
                continue

            counts += int(c.value == -broken_edge.value)
            broken_edge = IvalLoc.OUT

        return counts
    
    # as hray_cast, but for vertical rays
    def vray_cast(self, x: int, ymin: int, ymax: Optional[int] = None) -> int:
        counts: int = 0
        broken_edge: IvalLoc = IvalLoc.OUT
        for y,ival in self.hors.items():
            if y <= ymin:
                continue

            if ymax is not None and y >= ymax:
                continue
            
            c = is_contained(ival, x)

            if c == IvalLoc.OUT:
                continue

            if c == IvalLoc.INT:
                counts += 1
                continue

            if broken_edge == IvalLoc.OUT:
                broken_edge = c
                continue

            counts += int(c.value == -broken_edge.value)
            broken_edge = IvalLoc.OUT

        return counts


    def is_interior(self, pt: tuple[int,int]):
        if pt in self.int_cache:
            return self.int_cache[pt]
        
        self.int_cache[pt] = True
        if not (self.on_hedge(pt) or self.on_vedge(pt)):
            # not on an edge, use ray-casting to check if it's in the interior
            counts = self.hray_cast(pt[1], pt[0])

            if counts % 2 == 0:
                self.int_cache[pt] = False

        return self.int_cache[pt]
    
    def is_valid(self, c1: tuple[int,int], c2: tuple[int,int]) -> bool:
        max_x = max(c1[0],c2[0])
        min_x = min(c1[0],c2[0])
        max_y = max(c1[1],c2[1])
        min_y = min(c1[1],c2[1])

        # if the horizontal rectangle edge crosses a vertical boundary, part of it must be outside
        if self.hray_cast(max_y, min_x, max_x) > 0:
            return False
        
        if self.hray_cast(min_y, min_x, max_x) > 0:
            return False
        
        # if the vertical rectangle edge crosses a horizontal boundary, part of it must be outside
        if self.vray_cast(max_x, min_y, max_y) > 0:
            return False
        
        if self.vray_cast(min_x, min_y, max_y) > 0:
            return False
            
        # c1 and c2 are, by definition, on the edges, so check whether the catacorners are either on edges or inside
        k1 = (c1[0],c2[1])
        k2 = (c2[0],c1[1])

        return self.is_interior(k1) and self.is_interior(k2)
    

def generate_svg_polygon(coordinates, svg_width=100, svg_height=100, scale=1):
    """
    Generates a complete SVG string with a single black <polygon> element.

    Args:
        coordinates (list): A list of (x, y) tuples, e.g., [(10, 10), (50, 50), (10, 50)].
        svg_width (int): The width of the SVG canvas.
        svg_height (int): The height of the SVG canvas.

    Returns:
        str: The complete SVG XML string.
    """

    # 1. Format the coordinate list into the required "x1,y1 x2,y2 ..." string.
    # We use a list comprehension and the str.join method for efficiency.
    point_strings = [f"{x*scale},{y*scale}" for x, y in coordinates]
    points_attribute = " ".join(point_strings)

    # 2. Define the styling for the polygon
    # fill:black makes the inside of the shape black
    # stroke:black adds a border (usually redundant here, but good practice)
    # stroke-width:1 ensures the line has some thickness
    style_attributes = "fill:black;stroke:black;stroke-width:1"

    # 3. Construct the full SVG string
    svg_code = f"""
<svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
  <polygon points="{points_attribute}"
           fill="none"
           stroke="black"
           stroke-width="1" />
</svg>
"""
    return svg_code.strip()
    

if __name__ == "__main__":
    filename = sys.argv[1]
    locs = []
    with open(filename, "r") as f:
        lines = f.read().splitlines()
        locs = [tuple(map(int, line.split(","))) for line in lines]

    pairs = sorted(
        itertools.combinations(range(len(locs)), 2),
        key=lambda p: -(abs(locs[p[0]][0] - locs[p[1]][0]) + 1)
        * (abs(locs[p[0]][1] - locs[p[1]][1]) + 1),
    )

    corners = pairs[0]
    print(
        (abs(locs[corners[0]][0] - locs[corners[1]][0]) + 1)
        * (abs(locs[corners[0]][1] - locs[corners[1]][1]) + 1)
    )

    floor = Floor(locs)

    for i,pair in enumerate(pairs):
        if floor.is_valid(locs[pair[0]], locs[pair[1]]):
            break

    print(
        (abs(locs[pair[0]][0] - locs[pair[1]][0]) + 1)
        * (abs(locs[pair[0]][1] - locs[pair[1]][1]) + 1)
    )

    # print(generate_svg_polygon(locs, svg_height=1000, svg_width=1000, scale=0.01))