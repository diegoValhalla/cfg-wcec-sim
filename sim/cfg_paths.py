import sys

sys.path.insert(0, '../../src')

from cfg.cfg import CFG
from cfg.cfg_nodes import CFGNodeType, CFGEntryNode, CFGNode


class CFGPaths(object):
    """ Find the worst. best and middle paths in a CFG, assuming that each
        given CFG is made by only one function. In other words, all C code must
        be inside 'main()'
    """
    def find_worst_path(self, graph):
        """ Explore all graph to find the worst path based on RWCEC.

            Returns:
                tuple(<int(WORST WCEC)>, <list of CFGNodes that make this path>)
        """
        if not isinstance(graph, CFG): return

        rwcec = 0
        path = []
        for entry in graph.get_entry_nodes():
            start_node = entry.get_func_first_node()
            rwcec = self._find_worst_path(start_node, path)
        return (rwcec, path)

    def find_best_path(self, graph):
        """ Explore all graph to find the best path based on RWCEC.

            Returns:
                tuple(<int(BEST WCEC)>, <list of CFGNodes that make this path>)
        """
        if not isinstance(graph, CFG): return

        rwcec = 0
        path = []
        for entry in graph.get_entry_nodes():
            start_node = entry.get_func_first_node()
            rwcec = self._find_best_path(start_node, path)
        return (rwcec, path)

    def find_middle_path(self, graph, up_rwcec, down_rwcec):
        pass

    def _find_worst_path(self, n, path):
        """ Use RWCEC as base to know which child of current node guides the
            execution to the worst case. Since all nodes store the RWCEC,
            starting from them, it is easier to know the worst case from the
            root node in the CFG.

            Args:
                n (CFGNode): node of CFG
                path (list): a list to keep track of the worst path

            Returns:
                RWCEC of the worst path
        """
        if not isinstance(n, CFGNode): return 0

        path.append(n)
        next_node = None
        for child in n.get_children():
            if next_node == None or child.get_rwcec() > next_node.get_rwcec():
                next_node = child

        if next_node is None:
            return n.get_wcec()
        return n.get_wcec() + self._find_worst_path(next_node, path)

    def _find_best_path(self, n, path):
        """ Use RWCEC as base to know which child of current node guides the
            execution to the best case. Since all nodes store the RWCEC,
            starting from them, it is easier to know the best case from the
            root node in the CFG, because one node can have only two children,
            if one child leads to the worst RWCEC, so follows the other one.

            Note: the best path is the one which executes the minimum number of
            cycles in the CFG. So, if there is a loop in the path, the minimum
            number of cycles is to never enter in it. In other words, there is
            not any loop iteration, only the loop condition WCEC is used,
            because to not enter in the loop, its condition can not be true.

            Args:
                n (CFGNode): node of CFG
                path (list): a list to keep track of the best path

            Returns:
                RWCEC of the best path
        """
        if not isinstance(n, CFGNode): return 0

        path.append(n)
        next_node = None
        for child in n.get_children():
            if next_node == None or child.get_rwcec() < next_node.get_rwcec():
                next_node = child

        if next_node is None:
            return n.get_wcec()
        return n.get_wcec() + self._find_best_path(next_node, path)
