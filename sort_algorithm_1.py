import numpy as np
import random


# %% Insertion sort
# =============================================================================
def insertion_sort(array):
    n = len(array)
    for i in range(1, n):
        for j in range(i, 0, -1):
            if array[j] < array[j - 1]:
                array[j], array[j - 1] = array[j - 1], array[j]
            else:
                break
    return array


# %% Bubble sort
# =============================================================================
def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
    return array


# %% merge sort
# =============================================================================
def merge(a, b):
    s1, s2 = 0, 0
    ans = []
    while s1 < len(a) and s2 < len(b):
        if a[s1] <= b[s2]:  # if <, the sorting is no longer stable
            ans.append(a[s1])
            s1 += 1
        else:
            ans.append(b[s2])
            s2 += 1
    if s1 == len(a):
        ans = ans + b[s2:]
    if s2 == len(b):
        ans = ans + a[s1:]
    return ans


# important: input must be a list; cannot be ndarray.
def merge_sort(array):
    if len(array) <= 1:
        return array
    mid = len(array) // 2
    left = array[:mid]
    right = array[mid:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


# %% quick sort
# =============================================================================
def quick_sort(array):
    less = []
    equal = []
    greater = []
    if len(array) > 1:
        pivot = random.choice(array)
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return quick_sort(less) + equal + quick_sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array


# check_sort_result(quicksort.quicksort, distances)


# %% heap sort
# =============================================================================
class Heap():
    def __init__(self, array):
        self.heap = array
        self.length = len(array)
        self.build_max_heap()

    def left(self, idx):
        pos = 2 * idx + 1
        return pos if pos < self.length else None

    def right(self, idx):
        pos = 2 * idx + 2
        return pos if pos < self.length else None

    def parent(self, idx):
        return (idx - 1) // 2 if idx > 0 else None

    def build_max_heap(self):
        last_to_heapify = self.parent(self.length - 1)
        # lower limit of loop is 0
        for i in range(last_to_heapify, -1, -1):
            self.max_heapify(i)

    def _greater_child(self, i):
        left, right = self.left(i), self.right(i)
        if left is None and right is None:
            return None
        elif left is None:
            return right
        elif right is None:
            return left
        else:
            return left if self.heap[left] > self.heap[right] else right

    def max_heapify(self, i):
        greater_child = self._greater_child(i)
        if greater_child is not None and self.heap[greater_child] > self.heap[i]:
            self.heap[i], self.heap[greater_child] = self.heap[greater_child], self.heap[i]
            self.max_heapify(greater_child)

    def sort(self):
        while self.length > 1:
            self.heap[0], self.heap[self.length - 1] = self.heap[self.length - 1], self.heap[0]
            self.length -= 1
            self.max_heapify(0)
        return self.heap


def heap_sort(array):
    my_heap = Heap(array)
    return my_heap.sort()


# %% BST_sort
# =============================================================================
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.parent = None
        self.data = data
        self.height = 0

    def left_height(self):
        return -1 if self.left is None else self.left.height

    def right_height(self):
        return -1 if self.right is None else self.right.height

    def update_height(self):
        self.height = max(self.left_height(), self.right_height()) + 1

    def balance(self):
        """-2, -1: left heavy, 1, 2: right heavy"""
        return self.right_height() - self.left_height()


class BinaryTree:

    def __init__(self):
        self.root = None

    def inorder(self, node = 0, result = None):
        if result is None:
            result = []
        if node == 0:
            node = self.root
        if node:
            self.inorder(node.left, result)
            result.append(node.data)
            self.inorder(node.right, result)
        return result

    def inorder_1(self, node=0, result=None):
        if node == 0:
            current = self.root
        else:
            current = node
        if result is None:
            result = []
        stack = []
        while True:
            if current:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                result.append(current.data)
                current = current.right
            else:
                return result


class BinarySearchTree(BinaryTree):
    def __init__(self, data_array=[]):
        self.root = None
        for data in data_array:
            self.insert_1(Node(data))

    def insert(self, new_node, node=0):
        if not self.root:
            self.root = new_node
            return new_node
        if node == 0:
            node = self.root
        if new_node.data < node.data:
            if node.left:
                self.insert(new_node, node.left)
            else:
                new_node.parent = node
                node.left = new_node
        else:
            if node.right:
                self.insert(new_node, node.right)
            else:
                new_node.parent = node
                node.right = new_node
        node.update_height()

    def insert_1(self, new_node, node=0):
        if not self.root:
            self.root = new_node
            return new_node
        if node == 0:
            node = self.root
        queue = [node]
        for cur in queue:
            if new_node.data < cur.data:
                if cur.left:
                    queue.append(cur.left)
                else:
                    new_node.parent = cur
                    cur.left = new_node
            else:
                if cur.right:
                    queue.append(cur.right)
                else:
                    new_node.parent = cur
                    cur.right = new_node
        node.update_height()

    def sort(self):
        return self.inorder_1()


def BST_sort(array):
    my_tree = BinarySearchTree(array)
    return my_tree.sort()


# %% AVL_sort
# =============================================================================
class AVLTree(BinarySearchTree):
    def insert(self, new_node, node=0):
        super().insert(new_node, node)
        self.check_fix_AVL(new_node.parent)
        return new_node

    def update_all_heights_upwards(self, node):
        node.update_height()
        if node is not self.root:
            self.update_all_heights_upwards(node.parent)

    def _left_rotate(self, x):
        # First define y and B:
        y = x.right
        B = y.left
        # Setup y:
        y.parent = x.parent
        y.left = x
        # Setup y's parent
        if y.parent is None:
            self.root = y
        elif y.parent.left is x:
            y.parent.left = y
        else:
            y.parent.right = y
        # Setup x:
        x.parent = y
        x.right = B
        # Setup B:
        if B is not None:
            B.parent = x
        self.update_all_heights_upwards(x)

    def _right_rotate(self, x):
        # First define y and B:
        y = x.left
        B = y.right
        # Setup y:
        y.parent = x.parent
        y.right = x
        # Setup y's parent
        if y.parent is None:
            self.root = y
        elif y.parent.right is x:
            y.parent.right = y
        else:
            y.parent.left = y
        # Setup x:
        x.parent = y
        x.left = B
        # Setup B:
        if B is not None:
            B.parent = x
        self.update_all_heights_upwards(x)

    def check_fix_AVL(self, node):
        if node is None:
            return
        if abs(node.balance()) < 2:
            self.check_fix_AVL(node.parent)
            return
        if node.balance() == 2:  # right too heavy
            if node.right.balance() >= 0:
                self._left_rotate(node)
            else:
                self._right_rotate(node.right)
                self._left_rotate(node)
        else:  # node.balance() == -2, left too heavy
            if node.left.balance() <= 0:
                self._right_rotate(node)
            else:
                self._left_rotate(node.left)
                self._right_rotate(node)
        self.check_fix_AVL(node.parent)


def AVL_sort(array):
    my_tree = AVLTree(array)
    return my_tree.sort()


# %% count sort
def count_sort(array):
    dict = {}
    for i in array:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1
    new_dict_keys = sorted(dict)
    res = []
    for j in new_dict_keys:
        res += [j] * dict[j]
    return res


if __name__ == '__main__':
    # t1 = np.random.randint(-10, 20, 20)
    t1 = [1,7,4,6,2,1,4]
    print(insertion_sort(t1))
    print(bubble_sort(t1))
    print(merge_sort(t1))
    print(quick_sort(t1))
    print(heap_sort(t1))
    print(BST_sort(t1))
    print(AVL_sort(t1))
    print(count_sort(t1))