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
          self.used_boxes.append(Box(box[0], remainingWidth, usedBox.depth))

      if remainingHeight > 0:
          self.used_boxes.append(Box(usedBox.length, usedBox.width, remainingHeight))

def scoreBySizes(self, usedBox, box):
    return max(usedBox.length + box[0], usedBox.width + box[1], usedBox.depth + box[2])

def guillotineCut3D(boxes, palletLength, palletWidth, palletHeight):
    bin = GuillotineBin3D(palletLength, palletWidth, palletHeight)

    placedBoxes = 0
    for box in boxes:
        if bin.insert(box):
            placedBoxes += 1

    return placedBoxes  # else:               print(F"Could not place box {box}")

if __name__ == "__main__":

    boxes = [Box(265, 180, 140), Box(325, 245, 150), Box(390, 290, 310), Box(390, 290, 215),
             Box(560, 235, 200), Box(580, 255, 300), Box(585, 295, 315), Box(390, 390, 310)]

    palletLength = 1200
    palletWidth = 300
    palletHeight = 1500

    num_boxes_placed = guillotineCut3D(boxes, palletLength, palletWidth, palletHeight)

    if num_boxes_placed is not None:
        print("Number of boxes placed on the pallet:", num_boxes_placed)
