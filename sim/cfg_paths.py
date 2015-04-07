import sys, math

sys.path.insert(0, '../../src')

from cfg.cfg import CFG
from cfg.cfg_nodes import CFGNodeType, CFGEntryNode, CFGNode


class CFGPath(object):
    def __init__(self, rwcec, path):
        self._rwcec = rwcec
        self._path = list(path)

    def get_path_rwcec(self):
        return self._rwcec

    def get_path(self):
        return self._path


class CFGPaths(object):
    """ Find the worst. best and middle paths in a CFG, assuming that each
        given CFG is made by only one function. In other words, all C code must
        be inside 'main()'
    """
    def find_worst_path(self, graph):
        """ Explore all graph to find the worst path based on RWCEC.

            Args:
                graph (CFG): control flow graph

            Returns:
                CFGPath object
        """
        if not isinstance(graph, CFG): return

        cfg_path = None
        for entry in graph.get_entry_nodes():
            path = []
            start_node = entry.get_func_first_node()
            rwcec = self._find_worst_path(start_node, path)
            cfg_path = CFGPath(rwcec, path)
        return cfg_path

    def find_best_path(self, graph):
        """ Explore all graph to find the best path based on RWCEC.

            Args:
                graph (CFG): control flow graph

            Returns:
                CFGPath object
        """
        if not isinstance(graph, CFG): return

        cfg_path = None
        for entry in graph.get_entry_nodes():
            path = []
            start_node = entry.get_func_first_node()
            rwcec = self._find_best_path(start_node, path)
            cfg_path = CFGPath(rwcec, path)
        return cfg_path

    def find_mid_path(self, graph, upper_rwcec, lower_rwcec):
        """ Explore all graph to find one path whose RWCEC is the greatest one
            smaller than the upper bound. However, it should not be the less
            than lower bound.

            Args:
                graph (CFG): control flow graph
                upper_rwcec (int): RWCEC upper bound
                lower_rwcec (int): RWCEC lower bound

            Returns:
                CFGPath object
        """
        if not isinstance(graph, CFG): return

        cfg_path = None
        for entry in graph.get_entry_nodes():
            start_node = entry.get_func_first_node()
            cfg_path = None
            path = []
            cfg_path = self._find_mid_path(start_node, path,
                    start_node.get_wcec(), upper_rwcec, lower_rwcec, 0)
        return cfg_path

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
        elif n.get_type() == CFGNodeType.PSEUDO:
            return n.get_refnode_rwcec() + self._find_worst_path(next_node, path)

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

    def _find_mid_path(self, n, path, newrwcec, urwcec, lrwcec, bestrwcec):
        """ Find a path whose RWCEC is the greatest value less than the upper
            bound and greater than lower bound.

            All possible paths from a CFG is explored and their RWCEC is
            computed. By the end, when CFG's last node is reached, check if the
            RWCEC of this new path is better from the previous one. If so, keep
            track of its contents and continue to explore the other paths until
            there is no other path better than the one saved.

            If there is a loop in CFG, it must be checked the RWCEC of all
            possible paths by changing the number of iterations. In other
            words, check the best path doing the loop once, twice, three times
            until its maximum iteration number.

            Note: only the most external loop is handled. So, loops nested are
            not supported.

            Args:
                n (CFGNode): current node
                path (list): keep tracking of current path nodes
                newrwcec (int): RWCEC of the new path explored
                urwcec (int): RWCEC upper bound
                lrwcec (int): RWCEC lower bound
                bestrwcec (int): best RWCEC reached until now

            Returns:
                CFGPath object
        """
        if not isinstance(n, CFGNode): return

        tmp_path = None
        cfg_path = None
        path.append(n) # make path
        for child in n.get_children():
            if child.get_type() != CFGNodeType.PSEUDO:
                tmp_path = self._find_mid_path(child, path,
                        newrwcec + child.get_wcec(), urwcec, lrwcec, bestrwcec)
            else:
                for i in range(1, child.get_loop_iters() + 1):
                    if i <= child.get_loop_iters():
                        loop_wcec = child.get_refnode_rwcec() - child.get_wcec()
                        loop_wcec = float(loop_wcec)
                        loop_wcec = child.get_wcec() + (loop_wcec / i)
                        loop_wcec = int(math.ceil(loop_wcec))
                    else: # there is no loop iteration
                        loop_wcec = child.get_wcec()
                    tmp_path = self._find_mid_path(child, path,
                            newrwcec + loop_wcec, urwcec, lrwcec, bestrwcec)

                    # set the greatest cfg path by exploring each loop iteration
                    if (tmp_path is not None
                            and (cfg_path is None or tmp_path.get_path_rwcec() >
                                cfg_path.get_path_rwcec())):
                        cfg_path = tmp_path

                    if cfg_path is not None:
                        bestrwcec = cfg_path.get_path_rwcec()

            # set the greatest cfg path
            if (tmp_path is not None
                    and (cfg_path is None or tmp_path.get_path_rwcec() >
                        cfg_path.get_path_rwcec())):
                cfg_path = tmp_path

            if cfg_path is not None:
                bestrwcec = cfg_path.get_path_rwcec()

        # get a new cfg path whose RWCEC is valid
        if n.get_children() == []:
            if newrwcec > bestrwcec and lrwcec < newrwcec and newrwcec < urwcec:
                cfg_path = CFGPath(newrwcec, path)

        path.remove(n)
        return cfg_path
