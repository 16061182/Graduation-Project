import cv2

def plot_hand_2d(coords_hw, image, linewidth=2):
    """ Plots a hand stick figure into a matplotlib figure. """
    colors = [(0, 0, 127),
              (0, 0, 187),
              (0, 0, 246),
              (0, 32, 255),
              (0, 85, 255),
              (0, 140, 255),
              (0, 192, 255),
              (15, 248, 231),
              (57, 255, 190),
              (102, 255, 144),
              (144, 255, 102),
              (190, 255, 57),
              (231, 255, 15),
              (255, 211, 0),
              (255, 163, 0),
              (255, 111, 0),
              (255, 63, 0),
              (246, 11, 0),
              (187, 0, 0),
              (127, 0, 0)]

    # define connections and colors of the bones
    bones = [((0, 4), colors[0]),
             ((4, 3), colors[1]),
             ((3, 2), colors[2]),
             ((2, 1), colors[3]),

             ((0, 8), colors[4]),
             ((8, 7), colors[5]),
             ((7, 6), colors[6]),
             ((6, 5), colors[7]),

             ((0, 12), colors[8]),
             ((12, 11), colors[9]),
             ((11, 10), colors[10]),
             ((10, 9), colors[11]),

             ((0, 16), colors[12]),
             ((16, 15), colors[13]),
             ((15, 14), colors[14]),
             ((14, 13), colors[15]),

             ((0, 20), colors[16]),
             ((20, 19), colors[17]),
             ((19, 18), colors[18]),
             ((18, 17), colors[19])]

    for connection, color in bones:
        coord1 = coords_hw[connection[0], :]
        coord2 = coords_hw[connection[1], :]

        coord1_t = (int(coord1[1]), int(coord1[0]))
        coord2_t = (int(coord2[1]), int(coord2[0]))

        cv2.line(image, coord2_t, coord1_t, color, linewidth)