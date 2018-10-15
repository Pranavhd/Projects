import operator

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def findroot(arr):
    if len(arr) == 0:
        return None
    index, value = max(enumerate(arr), key=operator.itemgetter(1))
    root = TreeNode(value)
    root.left = findroot(arr[:index])
    root.right = findroot(arr[index + 1:])
    return root

nums = [3,2,1,6,0,5]
print((findroot(nums)).val)