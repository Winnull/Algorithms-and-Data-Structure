from BinarySearchTree import *

BLACK = 0
RED = 1


class NodeRBT(object):
    def __init__(self, key=None, value=None, color=BLACK):
        self.key = key
        self.value = value
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.color = color
        self.size_tree = 0

    def __str__(self):
        return "<class NodeRBT ({}, {}, {}, {})>".format(self.key, self.value, self.get_color(), self.size_tree)
    __repr__ = __str__

    def get_color(self):
        if self.color:
            return "RED"
        else:
            return "BLACK"

    def show_info(self):
        if not self.parent:
            print("######### ROOT #########")
        print("------------------------")
        print("key: %s" % self.key)
        print("value: %s" % self.value)
        print("color: %s" % self.get_color())
        print("left_child: %s" % self.left_child.key)
        print("right_child: %s" % self.right_child.key)
        print("parent: %s" % self.parent.key if self.parent else "parent: None")
        print("size_tree: %s" % self.size_tree)
        print("------------------------")

    def get_info_in_tuple(self):
        return self.key, self.value, self.get_color()

    def reset(self):
        self.key = None
        self.value = None
        self.parent = None
        self.left_child = None
        self.right_child = None
        self.color = BLACK
        self.size_tree = 0


class RedBlackTree(object):
    def __init__(self):
        self.root = NodeRBT(None, None, BLACK)

    def __str__(self):
        return "<class RedBlackTree of size {}>".format(self.root.size_tree)
    __repr__ = __str__

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        self.pointer += 1
        if self.pointer > self.root.size_tree:
            raise StopIteration

        return self.select(self.pointer)

    def __getitem__(self, item):
        return self.select(item)

    def __compare(self, key=None, method='compare', source=None, print_path=False):
        compare_node = source if source else self.root
        parent_node = None

        while compare_node.key:
            parent_node = compare_node

            if method == 'search':
                if parent_node.key == key:
                    # when the method is search, compare_node is the result
                    parent_node = parent_node.parent
                    break

            if method == 'compare' or method == 'search':
                compare_node = parent_node.left_child if key <= parent_node.key else parent_node.right_child

            if method == 'min':
                compare_node = parent_node.left_child

            if method == 'max':
                compare_node = parent_node.right_child

            if print_path:
                try:
                    root_string = "(root)" if not parent_node.parent else ""
                    print(root_string + "({}, {}, {}) -> ({}, {}, {})".format(
                        parent_node.key, parent_node.value, parent_node.get_color(),
                        compare_node.key, compare_node.value, compare_node.get_color()))
                except AttributeError:
                    pass

        return parent_node, compare_node

    def __rotation(self, node, right_rotation=False):
        """
        Rotate around a certain node.
        Args:
            node: the node to be rotated, class NodeRBT
            right_rotation: True for right rotation, False for left rotation

        """
        # left rotation
        if not right_rotation:
            # update parent
            parent = node.parent
            neighbor = node.right_child
            if node.key <= parent.key:
                parent.left_child = neighbor
            else:
                parent.right_child = node.right_child

            # update node
            node.parent = neighbor
            node.right_child = neighbor.left_child

            # update neighbor
            neighbor.parent = parent
            neighbor.left_child = node

            # print("--> before left rotation:")
            # print("size tree of node {}: {}".format(node.key, node.size_tree))
            # print("size tree of node {}: {}".format(neighbor.key, neighbor.size_tree))

            # update size of tree
            node.size_tree -= neighbor.size_tree
            node.size_tree += node.right_child.size_tree
            neighbor.size_tree -= node.right_child.size_tree
            neighbor.size_tree += node.size_tree

            # print("--> after left rotation:")
            # print("size tree of node {}: {}".format(node.key, node.size_tree))
            # print("size tree of node {}: {}".format(neighbor.key, neighbor.size_tree))

        # right rotation
        else:
            # update parent
            parent = node.parent
            neighbor = node.left_child
            if node.key <= parent.key:
                parent.left_child = neighbor
            else:
                parent.right_child = node.right_child

            # update node
            node.parent = neighbor
            node.left_child = neighbor.right_child

            # update neighbor
            neighbor.parent = parent
            neighbor.right_child = node

            # print("--> before right rotation:")
            # print("size tree of node {}: {}".format(node.key, node.size_tree))
            # print("size tree of node {}: {}".format(neighbor.key, neighbor.size_tree))

            # update size of tree
            node.size_tree -= neighbor.size_tree
            node.size_tree += node.left_child.size_tree
            neighbor.size_tree -= node.left_child.size_tree
            neighbor.size_tree += node.size_tree

            # print("--> after right rotation:")
            # print("size tree of node {}: {}".format(node.key, node.size_tree))
            # print("size tree of node {}: {}".format(neighbor.key, neighbor.size_tree))

    def __fix_double_reds(self, node):
        grand_parent_node = node.parent.parent
        parent_node = node.parent

        if grand_parent_node.left_child.color == grand_parent_node.right_child.color:
            uncle_node_red = True
        else:
            uncle_node_red = False

        # Case 3.1: uncle node is RED
        if uncle_node_red:
            grand_parent_node.left_child.color = BLACK
            grand_parent_node.right_child.color = BLACK
            grand_parent_node.color = RED

            # if the grand parent node is the root, change color to BLACK
            if not grand_parent_node.parent:
                grand_parent_node.color = BLACK

            else:
                # detect whether the new two-red problem comes up
                if grand_parent_node.parent.color == RED:
                    self.__fix_double_reds(grand_parent_node)

        # Case 3.2: uncle node is BLACK
        else:
            # Case 3.2.1: need first a local rotation
            if (node.key <= parent_node.key) != (parent_node.key <= grand_parent_node.key):
                self.__rotation(parent_node, right_rotation=(node.key <= parent_node.key))
                node = parent_node
                parent_node = parent_node.parent

            # Case 3.2.2: no need for a local rotation
            self.__rotation(grand_parent_node, right_rotation=(parent_node.key <= grand_parent_node.key))
            parent_node.color = BLACK
            grand_parent_node.color = RED

    def check_balance(self):
        size_tree = self.root.size_tree
        num_black_nodes_ref = 0

        # calculate the number of black nodes on the path to the node with the smallest key
        pointer = self.root
        while pointer.left_child.key:
            if pointer.color == BLACK:
                num_black_nodes_ref += 1
            pointer = pointer.left_child

        for i in range(1, size_tree + 1):
            node = self.select(i)
            # check every end node whether the numbers of black nodes are same
            if node.size_tree == 1:
                num_black_nodes = 0
                pointer = node
                while pointer.parent:
                    if pointer.color == BLACK:
                        num_black_nodes += 1
                    pointer = pointer.parent

                # add one because of root
                num_black_nodes += 1
                if num_black_nodes != num_black_nodes_ref:
                    raise ValueError("The tree is not balance!")

        print("Balance test success!")

    def check_color(self):
        size_tree = self.root.size_tree
        for i in range(1, size_tree + 1):
            node = self.select(i)
            # check from every end node
            if node.size_tree == 1:
                pointer = node
                while pointer.parent:
                    if pointer.color == RED and pointer.parent.color == RED:
                        raise ValueError("The tree has double red!")
                    pointer = pointer.parent

                if pointer.color != BLACK:
                    raise ValueError("The root is not black!")

        print("Color test success!")

    def check_all(self):
        self.check_balance()
        self.check_color()

    def get_node(self, key, print_path=False):
        """
        Get the node with the given key.
        Args:
            key: the key of the node
            print_path: True for printing the searching path, and vice versa

        Returns:
            search_node: class NodeBST

        """
        parent_node, search_node = self.__compare(key, method='search', print_path=print_path)

        return search_node

    def search(self, key, print_path=False):
        """
        Search for a certain key. Print the information of the node.
        Args:
            key: the key of the node to be searched
            print_path: True for printing the searching path, and vice versa

        """
        search_node = self.get_node(key, print_path)
        print("ID: {}\nValue: {}\nColor: {}".format(search_node.key, search_node.value, search_node.get_color()))

    def select(self, index, source=None):
        """
        Select a certain index of node in an ascending order, i.e. return the node with the ith smallest key.
        Args:
            index: ith smallest key

        """
        if index > self.root.size_tree or index <= 0:
            raise IndexError("The index is out of range!")

        check_node = self.root if not source else source

        while True:
            size_left_tree = check_node.left_child.size_tree
            if size_left_tree == index - 1:
                break
            elif size_left_tree >= index:
                check_node = check_node.left_child
            else:
                check_node = self.select(index - size_left_tree - 1, source=check_node.right_child)
                break

        return check_node

    def insert(self, key, value):
        insert_node = NodeRBT(key, value, color=RED)

        parent_node, _ = self.__compare(key)

        # Case 1: root node
        # if no parent_node, means the insert node is the root
        if not parent_node:
            self.root = insert_node
            self.root.color = BLACK
            self.root.left_child = NodeRBT(None, None)
            self.root.right_child = NodeRBT(None, None)

            # update the size of tree
            insert_node.size_tree += 1

        else:
            insert_node.parent = parent_node
            insert_node.left_child = NodeRBT(None, None, color=BLACK)
            insert_node.right_child = NodeRBT(None, None, color=BLACK)
            if key <= parent_node.key:
                parent_node.left_child = insert_node
            else:
                parent_node.right_child = insert_node

            # Case 2: parent node is BLACK, do nothing
            if parent_node.color == BLACK:
                pass
            # Case 3: parent node is RED, solve the two-red problem
            else:
                self.__fix_double_reds(insert_node)

            # update the size of tree
            parent_node = insert_node.parent
            insert_node.size_tree += 1
            parent_node.size_tree += 1
            while parent_node.parent:
                parent_node = parent_node.parent
                parent_node.size_tree += 1

    def show_single_path(self, node, path_str=""):
        while node.parent:
            path_str = self.show_single_path(node.parent, path_str)
            break

        path_str += " -> "
        path_str += str(node.get_info_in_tuple())

        return path_str

    def show_paths(self):
        print("------------------------")
        print("######### ALL PATHS #########")
        for i in range(1, self.root.size_tree + 1):
            node = self.select(i)
            if node.size_tree == 1:
                print("|" + self.show_single_path(node))
        print("------------------------")


treeRBT = RedBlackTree()

# test for insert case 1 & 2 & 3.1
treeRBT.insert(2000, 100)
treeRBT.insert(1500, 100)
treeRBT.insert(2500, 100)
treeRBT.insert(1300, 100)
treeRBT.insert(1700, 100)
treeRBT.insert(1600, 100)
# treeRBT.search(1600, print_path=True)

# test for insert case 3.2.1
# treeRBT.insert(1200, 100)
# treeRBT.insert(1100, 100)
# treeRBT.search(1300, print_path=True)
# for i in treeRBT:
#     i.show_info()

# test for insert case 3.2.2
treeRBT.insert(1200, 100)
treeRBT.insert(1250, 100)
# for i in treeRBT:
#     i.show_info()


# # test for select & iteration & list
# print(treeRBT.select(3))
# for i in treeRBT:
#     print(i)
# print(treeRBT[3])

treeRBT.check_all()

treeRBT.show_paths()
