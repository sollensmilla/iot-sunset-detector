def estimate_cct(r, g, b):

    # Avoid divide by zero
    if r == 0 and g == 0 and b == 0:
        return 0

    # Normalize
    total = r + g + b

    rn = r / total
    gn = g / total
    bn = b / total

    # Simple warm/cool estimation
    cct = int(
        1000 +
        (bn * 9000)
    )

    return cct