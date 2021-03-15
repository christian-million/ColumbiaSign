# Resources
# https://towardsdatascience.com/how-to-loop-through-your-own-objects-in-python-1609c81e11ff
# https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
# https://docs.python.org/3/reference/datamodel.html#object.__contains__
import copy


class Node:
    '''A single element of a linear data structure
    Contains data to store and a reference to the subsequent Node (or None if the last Node)
    Arguments
    ---------
    data :
        The information to store. Can be anything.

    nxt : Node
        A reference to the subsequent Node, or None if the last.
    '''
    def __init__(self, data, nxt=None):
        # The actual content of the Node
        self.data = data

        # This should be a reference to the subsequent Node or None
        self.nxt = nxt

    def __str__(self):
        # Return the data string representation
        return str(self.data)


class LinkedListIter:
    '''An iterator for the LinkedList class that allows the LinkedList class to be iterated over
    Iteration happens on each Nodes data attribute
    '''
    def __init__(self, LinkedList):
        self.LinkedList = LinkedList

        # initialize the first node to be the head
        self.i_node = self.LinkedList.head

        self.len = len(self.LinkedList)
        self.count = 0

    def __next__(self):
        if self.i_node and self.count <= self.len:
            # capture the data before overriding the next node
            out = self.i_node.data

            # increment to the subsequent node
            self.i_node = self.i_node.nxt

            self.count += 1

            # return the data
            return out

        else:
            raise StopIteration


class LinkedList:
    '''LinkedList is a sequence of nodes which reference subsequent nodes
    Arguments
    ---------
    *args :
        elements added to structure on initialization
    unpack : bool
        for single length *args of type list or tuple, use each element as node (defaults True)
    '''
    def __init__(self, *args, unpack=True):

        self.head = None

        # args is technically a tuple, so not using any lists :)
        if args:
            # Unpack each element of single list or tuple into individual nodes
            if len(args) == 1 and isinstance(args[0], (list, tuple)) and unpack:
                args = args[0]

            for arg in args:
                self.append(arg)

        # Set a default delimiter
        self.delimiter = ' -> '

    def append(self, data, right=True):
        '''Add a node to the end
        Arguments
        ---------
        data :
            the data to append. Could be anything.
        right : bool
            append to the right (default True)
        '''
        if self.head:
            if right:
                # Initialize a current_node to overwrite
                current_node = self.head

                # Swipe through each node until the last
                while current_node.nxt:
                    current_node = current_node.nxt

                # Add the new node to the end
                current_node.nxt = Node(data)

            # On left append, new node becomes the head
            else:
                self.head = Node(data, self.head)
        # On empty list, new node becomes the head
        else:
            self.head = Node(data)

    def pop(self, right=True):
        '''Removes and returns the the right/left element
        Arguments
        ---------
        right : bool
            pop the right side? (default True)
        '''
        if self.head:
            if right:
                # Initialize reference nodes to overwrite
                prev_node = self.head
                current_node = self.head

                # Until the last node has been reached
                while current_node:

                    # Skip to the next
                    if current_node.nxt:
                        prev_node = current_node
                        current_node = current_node.nxt

                    # On the last node...
                    else:
                        # ...Remove references to it
                        prev_node.nxt = None

                        # Return the data
                        return current_node.data

            # On left pop, the heads next becomes the head
            else:
                # capture the data before overwriting
                out = self.head.data

                # Replace the head before returning
                self.head = self.head.nxt

                # Return the popped data
                return out

    def contains(self, item):
        '''Check to see if the structure contains an element
        NOTE: This compares the item to the data, not against the Node itself.
        Arguments
        ---------
        item -- target item to identify

        Returns
        -------
        bool
            whether or not item exists in LinkedList
        '''
        if self.head:

            # Reference node to overwrite
            current_node = self.head

            # Run through each node
            while current_node:

                # Confirmed this works for None
                # Compares a Nodes data, not a Node
                if current_node.data == item:
                    return True

                # Skip to the next node
                else:
                    current_node = current_node.nxt

            # If while loop completed, then no match was found
            return False

        # If empty
        else:
            return False

    def has_cycle(self):
        '''Determines whether or not the LinkedList has a cycle or not

        Cycle - A (singly) linked list has a cycle if traversal of the
        list will result the in visiting the same node twice.

        Returns
        -------
        bool
            Whether the LinkedList has a cycle or not
        '''
        if self.head:

            # temporary traversal reference
            current_node = self.head

            # A list of nodes we've already traversed
            checked_nodes = LinkedList()
            while current_node:

                # Check each node against all other checked nodes
                for checked in checked_nodes:
                    if current_node.nxt is checked:
                        return True
                else:
                    # Add to list of checked nodes
                    checked_nodes.append(current_node)
                    current_node = current_node.nxt

            # If we made it out of the loop, then no cycle!
            return False

    def linked_list_type(self):
        '''Classifies the LinkedList into circle, lollipop, or terminating
        - A (singly) linked list has a cycle if traversal of the list will result the in visiting the same node twice.
        - A linked list is a circle it has a cycle containing the head.
        - A linked list is a lollipop if it has a cycle but is but is not a circle.

        Returns
        -------
        str
            One of "circle", "lollipop", or "terminating"
        '''
        if self.head:

            # temporary traversal reference
            current_node = self.head

            # A list of nodes we've already traversed
            checked_nodes = LinkedList()

            while current_node:

                # Check each node against all other checked nodes
                for checked in checked_nodes:
                    if current_node.nxt is checked:
                        # Do we reference the head next?
                        if current_node.nxt is self.head:
                            return "Circle"
                        else:
                            return "Lollipop"
                else:
                    # Add to list of checked nodes
                    checked_nodes.append(current_node)
                    current_node = current_node.nxt

            # If we made it out of the loop, then we've terminated!
            return "Terminating"

    def reverse(self):
        '''Reverses the order of the LinkedList'''
        if self.head:

            # Initialize some reference variables to overwrite
            previous_node = self.head
            next_node = self.head.nxt
            previous_node.nxt = None

            while next_node.nxt:
                # We need something to reference the unreversed
                tether = next_node.nxt

                # We can override this because we reference it above
                next_node.nxt = previous_node

                # Establish new previous node
                previous_node = next_node

                # Our original tether to the unreversed acts as our next node
                next_node = tether

            # replace the None pointer with the reversed
            next_node.nxt = previous_node

            # Make the last node the new head.
            self.head = next_node

    def __contains__(self, item):
        '''Allows for use with `in` operator'''
        return self.contains(item)

    def copy(self):
        '''Returns a deepcopy of itself'''
        return copy.deepcopy(self)

    def __add__(self, other):
        '''Overwrites plus sign to behave like python lists would when using "+"
        Nothing happens: LinkedList + LinkedList2
        New Object: LinkedList3 = LinkedList + LinkedList2
        Arguments
        ---------
        other -- the right hand side of an expression (self + other)
        '''
        og = copy.deepcopy(self)

        # Combines other LinkedList Nodes as Subsequent Nodes
        if isinstance(other, (LinkedList, Node)):

            # Create a copy of the right hand side
            other_copy = copy.deepcopy(other.head)

            # If this instance is empty, just fill it with the other
            if og.head is None:
                og.head = other_copy

            else:
                current_node = og.head

                # Skip along to the last node
                while current_node.nxt:
                    current_node = current_node.nxt

                # Make the last node reference the head of the other DataStructure
                current_node.nxt = other_copy

        # If it is not another LinkedList structure or Node, just append to right
        else:
            og.append(other)

        # return a new LinkedList instance
        return og

    def __iter__(self):
        '''Allows the structure to become an iterable.'''
        return LinkedListIter(self)

    def __len__(self):
        '''Counts the number of nodes in the structure
        Added bonus of considering empty structure as Falsey
        '''
        # Empty
        if self.head is None:
            return 0

        # Count until the next node doesn't exist.
        else:

            # temporary traversal reference
            i = 1
            current_node = self.head

            # A list of nodes we've already traversed
            checked_nodes = LinkedList()
            while current_node:

                # Check each node against all other checked nodes
                for checked in checked_nodes:
                    if current_node.nxt is checked:
                        return i
                else:
                    # Add to list of checked nodes
                    checked_nodes.append(current_node)
                    current_node = current_node.nxt
                    i += 1

            # If we made it out of the loop, then no cycle!
            return i

    def __eq__(self, other):
        '''Test equality between two LinkedLists
        Two LinkedLists are equal if the lengths are the same and the contents of
        each position are equal.
        '''
        if isinstance(other, LinkedList):
            if len(self) == len(other):
                for x, y in zip(self, other):
                    if x != y:
                        return False
                return True
        else:
            return False

    def __str__(self):
        # Show None
        if self.head is None:
            return "<None>"

        # Separate each nodes data using the delimiter
        else:
            # Initialize reference node to overwrite
            current_node = self.head

            # Initialize the string to return with first element
            out = str(self.head.data)

            while current_node.nxt:
                current_node = current_node.nxt

                # Add to the out string.
                out += f'{self.delimiter}{current_node.data}'

            return out

    def to_circle(self):
        '''Helper function to convert LinkedList into a circle. Sets the last Nodes `nxt` attribute to self.head'''
        if self.head:

            # This block just retrieves the last node
            next_node = self.head
            while next_node:
                current_node = next_node
                next_node = next_node.nxt

            # Set the head to the last nodes nxt
            current_node.nxt = self.head

    def to_lollipop(self, i=None):
        '''Helper function to convert LinkedList to Lollipop.
        Parameters
        ----------
        i : int
            the index of the node begins/ends the lollipop (defaults to half of LinkedList len)
        '''
        list_length = len(self)
        if list_length >= 2 and i < list_length:

            # Cast to approximately half if no index is provided
            if i is None:
                i = int(list_length/2)

            current_node = self.head

            # Indexing Counter
            j = 1
            while current_node:

                # If index of target node, reference it
                if j == i:
                    target_node = current_node

                # If we're at the end, then set the last nodes nxt to target node
                if j == len(self):
                    current_node.nxt = target_node
                    break

                # Iterate
                current_node = current_node.nxt
                j += 1

        else:
            raise AttributeError("Lollipops need at least 2 Nodes to work...")

    def __getitem__(self, key):
        if key < 0 or key >= len(self):
            raise IndexError

        count = 0
        node = self.head

        while key != count:
            node = node.nxt
            count += 1

        return node.data
