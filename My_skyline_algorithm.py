class Box:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

class SkylineBin3D:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.skyline = [(0, 0, length)]
        self.placed_boxes = []

    def insert(self, box):
        best_score = float("inf")
        best_node = None

        for node in self.skyline:
            for rotation in self.generate_rotations(box):
                score, placement = self.score_by_sizes(node, rotation)
                if score < best_score:
                    best_score = score
                    best_node = node
                    best_rotation = rotation
                    best_placement = placement

        if best_node:
            self.split_node(best_node, best_rotation, best_placement)
            return True
        else:
            return False
        
    def split_node(self, node, box, placement):
            x, y, remaining_length = node
            _,_,box_length = box
            self.placed_boxes.append((x, y, remaining_length, placement))

            # Update skyline.
            next_y = y + placement[1]
            next_remaining_length = remaining_length - placement[0]
            self.skyline.remove(node)
            if next_remaining_length > 0:
                self.skyline.append((x, next_y, next_remaining_length))

            # Add remaining space after placing the box
            remaining_space = [(x + placement[0], y, box_length)]
            self.skyline.extend(remaining_space)
            self.skyline = [(x, y, length) for x, y, length in self.skyline if length > 0] 

    def generate_rotations(self, box):
        length, width, height = box
        return [
        (length, width, height),
        (length, height, width),
        (width, length, height),
        (width, height, length),
        (height, length, width),
        (height, width, length),
        ]

    def score_by_sizes(self, node, box):
        x, y, remaining_length = node
        length, width, height = box
        best_fit = float("inf")
        best_placement = None

        for i in range(len(self.skyline)):
            nx, ny, remaining = self.skyline[i]
            if remaining < width:
                continue
            if ny + height > self.height:
                continue
            if remaining == width:
                placement = (remaining, width)
            else:
                placement = (width, min(remaining - width, width))
            if placement[0] * placement[1] < best_fit:
                best_fit = placement[0] * placement[1]
                best_placement = placement
        return best_fit, best_placement

def skylineCut3D(boxes, palletLength, palletwidth, palletHeight):
    bin = SkylineBin3D(palletLength, palletwidth, palletHeight)
    placed_boxes = 0
    for box in boxes:
        if bin.insert((box.length, box.width, box.height)):
            placed_boxes += 1
    for box in bin.placed_boxes:
        x, y, z, _ = box
        print(f"({x}, {y}, {z})")
    return placed_boxes

    #Example usage:

if __name__ == "__main__":
    boxes = [Box(265, 180, 140), Box(325, 245, 150), Box(390, 290, 310), Box(390, 290, 215),
                Box(560, 235, 200), Box(580, 255, 100), Box(505, 205, 315), Box(300, 300, 310)]
    pallet_length = 1200
    pallet_width = 800
    pallet_height = 1500
    num_boxes_placed = skylineCut3D(boxes, pallet_length, pallet_width, pallet_height)
    print(f"Number of boxes placed on the pallet: {num_boxes_placed}")