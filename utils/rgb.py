def normalize_rgb(r, g, b):

    # Compress dynamic range
    r = int(r ** 0.5)
    g = int(g ** 0.5)
    b = int(b ** 0.5)

    # Manual balancing
    r = r * 1.0
    g = g * 4.0
    b = b * 1.5

    max_val = max(r, g, b)

    if max_val == 0:
        return 0, 0, 0

    r8 = int((r / max_val) * 255)
    g8 = int((g / max_val) * 255)
    b8 = int((b / max_val) * 255)

    return r8, g8, b8