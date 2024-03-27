import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Box:
    def __init__(self, length, width, depth):
        self.length = length
        self.width = width
        self.depth = depth

    def get_orientations(self):
        return [
            (self.length, self.width, self.depth),
            (self.length, self.depth, self.width),
            (self.width, self.length, self.depth),
            (self.width, self.depth, self.length),
            (self.depth, self.length, self.width),
            (self.depth, self.width, self.length),
        ]

class GuillotineBin3D:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.used_boxes = [Box(0, 0, length)]

    def insert(self, box):
        if self.try_insert(box):
            return True
        return False

    def score_by_sizes(self, node, box):
        x, y, remaining_length = node.__dict__["length"], node.__dict__["width"], node.__dict__["depth"]
        length, width, height = box.__dict__["length"], box.__dict__["width"], box.__dict__["depth"]
        best_fit = float("inf")
        best_placement = None
        for i in range(len(self.used_boxes)):
            nx, ny, remaining = self.used_boxes[i].__dict__["length"], self.used_boxes[i].__dict__["width"], self.used_boxes[i].__dict__["depth"]
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

    def try_insert(self, box):
        best_score = float('inf')
        best_box = None
        for used_box in self.used_boxes:
            b1 = used_box.__dict__
            b2 = box.__dict__
            score, placement = self.score_by_sizes(used_box, box)
            if score < best_score:
                best_score = score
                best_box = used_box
        if best_box:
            # Insert the box into the best_box
            self.splitBox(best_box, box)
            return True
        return False

    def splitBox(self, usedBox, box):
        self.used_boxes.remove(usedBox)

        remainingLength = usedBox.__dict__["length"] - box.__dict__["length"]
        remainingWidth = usedBox.__dict__["width"] - box.__dict__["width"]
        remainingHeight = usedBox.__dict__["depth"] - box.__dict__["depth"]

        if remainingLength > 0:
            self.used_boxes.append(Box(remainingLength, usedBox.width, usedBox.depth))

        if remainingWidth > 6:
            self.used_boxes.append(Box(box.length, remainingWidth, usedBox.depth))

        if remainingHeight > 0:
            self.used_boxes.append(Box(usedBox.length, usedBox.width, remainingHeight))

def scoreBySizes(self, usedBox, box):
    return max(usedBox.length + box[0], usedBox.width + box[1], usedBox.depth + box[2])

def guillotineCut3D(boxes, palletLength, palletWidth, palletHeight):
    bin = GuillotineBin3D(palletLength, palletWidth, palletHeight)

    placedBoxes = []
    for box in boxes:
        if bin.insert(box):
            placedBoxes.append((box.length, box.width, box.depth))

    return placedBoxes

def visualize_boxes(boxes, palletLength, palletWidth, palletHeight, placedBoxes):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([0, palletLength])
    ax.set_ylim([0, palletWidth])
    ax.set_zlim([0, palletHeight])

    #for box in boxes:
    #   ax.bar3d(0, 0, 0, box.length, box.width, box.depth, color='r', alpha=0.1)
    colors = ['b', 'y', 'g', 'r']
    index = 0
    for box in placedBoxes:
        ax.bar3d(box[0], box[1], box[2], box[0], box[1], box[2], color=colors[index%4])
        index += 1

    plt.show()

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

if __name__ == "__main__":
    boxes = [Box(265, 180, 140), Box(325, 245, 150), Box(390, 290, 310), Box(390, 290, 215),
             Box(560, 235, 200), Box(580, 255, 300), Box(585, 295, 315), Box(390, 390, 310)]

    palletLength = 1200
    palletWidth = 800
    palletHeight = 1500

    placedBoxes = guillotineCut3D(boxes, palletLength, palletWidth, palletHeight)
    placedBoxes2 = skylineCut3D(boxes, palletLength, palletWidth, palletHeight)

    if placedBoxes:
        print("Number of boxes placed on the pallet:", len(placedBoxes))
        # print placed boxes
        for box in placedBoxes:
            print(box)
        visualize_boxes(boxes, palletLength, palletWidth, palletHeight, placedBoxes)
    else:
        print("Could not place any boxes on the pallet.")
