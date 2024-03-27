class Box:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

def maximalRectanglePacking(boxes, palletlength, palletwidth, palletHeight):
    dimension = sorted(boxes, key=lambda box: max(box.length, box.width, box.height), reverse=True)
    # Sort boxes by maximum dimension in descending order
    pallets = [(palletlength, palletwidth, palletHeight)]
    placed_boxes = 0

    for box in dimension:
        for i in range(len(pallets)):
            if (box.length < pallets[i][0] and box.width < pallets[i][1] and box.height < pallets[i][2]) or \
               (box.length < pallets[i][1] and box.width < pallets[i][2] and box.height < pallets[i][0]) or \
               (box.width < pallets[i][0] and box.length < pallets[i][2] and box.height < pallets[i][1]) or \
               (box.width < pallets[i][1] and box.length < pallets[i][0] and box.height < pallets[i][2]) or \
               (box.height < pallets[i][0] and box.length < pallets[i][1] and box.width < pallets[i][2]) or \
               (box.height < pallets[i][1] and box.width < pallets[i][0] and box.length < pallets[i][2]):
                placed_boxes += 1
                # Place the box and possibly split the pallet
                new_pallets = []
                for j in range(len(pallets)):
                    new_pallets.extend(splitPallet(pallets[j], box))
                else:
                    new_pallets.append(pallets[i])
                pallets = new_pallets
                break
    return placed_boxes

def splitPallet(pallet, box):
    remaining_pallets = []
    if box is not None:
        if box.length < pallet[0]:
            remaining_pallets.append((pallet[0] - box.length, pallet[1], pallet[2]))
        if box.width < pallet[1]:
            remaining_pallets.append((pallet[0], pallet[1] - box.width, pallet[2]))
        if box.height < pallet[2]:
            remaining_pallets.append((pallet[0], pallet[1], pallet[2] - box.height))
        return remaining_pallets

if __name__ == "__main__":
    boxes = [Box(265, 180, 140), Box(325, 245, 150), Box(390, 290, 310), Box(398, 290, 215), 
             Box(560, 235, 200), Box(580, 255, 300), Box(585, 295, 315), Box(390, 390, 310)]
    pallet_length = 1200
    pallet_width=800
    pallet_height = 1500
    num_boxes_placed = maximalRectanglePacking(boxes, pallet_length, pallet_width, pallet_height)
    print (f"Number of boxes placed on the pallet: {num_boxes_placed}")