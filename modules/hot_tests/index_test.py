

indexes = {"Top": 1,
           "Right": 2,
           "Left": 3,
           "Bottom": 5}

def y_mod(indexes: list[int]) -> bool: return sum(indexes) > 6
def x_mod(indexes: list[int]) -> bool: return sum(indexes) % 2

corners_list = [["Top", "Right"], ["Top", "Left"], ["Bottom", "Right"], ["Bottom", "Left"]]
data = [f"Corner {corner[0]}-{corner[1]} has Y Mod of {y_mod([indexes[corner[0]], indexes[corner[1]]])} and X mod of {x_mod([indexes[corner[0]], indexes[corner[1]]])}" for corner in corners_list]
print("\n".join(data))
