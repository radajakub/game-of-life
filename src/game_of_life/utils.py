import numpy as np


def crop_box(box: np.ndarray) -> np.ndarray:
    """
    Crop the box to the smallest rectangle that contains all the non-zero elements.
    """
    ys, xs = np.where(box != 0)
    return box[ys.min(): ys.max() + 1, xs.min(): xs.max() + 1]
