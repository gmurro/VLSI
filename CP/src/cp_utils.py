def compute_l_max(x,y,w):
    l_max = sum(y)
    max_x = max(x)
    max_y = max(y)
    w_blocks = w // max_x
    l_max = -(l_max // -w_blocks)
    l_max = max_y if l_max < max_y else l_max
    return l_max