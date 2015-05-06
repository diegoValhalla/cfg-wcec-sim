import sys, math

sys.path.insert(0, '../../src')

from cfg.cfg import CFG
from cfg.cfg_nodes import CFGNodeType, CFGEntryNode, CFGNode


class CFGPath(object):
    """ Hold path RWCEC and all nodes that made it

        Args:
            rwcec (int): RWCEC of the given path
            path (list): list whose elements are tuple(node, node-wcec)
    """
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

        Attributes:
            _mid_paths (dic): holds all middle paths that their RWCECs are in
                the range of the given lower and upper RWCEC bounds. The key is
                path RWCEC, whereas the value is a CFGPath object.
    """
    def __init__(self):
        self._mid_paths = {}
        self._visited_loops = {}

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

        if self._mid_paths == {}:
            for entry in graph.get_entry_nodes():
                start_node = entry.get_func_first_node()
                path = [(start_node, start_node.get_wcec())]
                cfg_path = self._find_mid_path(start_node, path,
                        start_node.get_wcec(), upper_rwcec, lower_rwcec, 0)

        return self._check_mid_path_cached(lower_rwcec, upper_rwcec)

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

        path.append((n, n.get_wcec()))
        next_node = None
        for child in n.get_children():
            if next_node == None or child.get_rwcec() > next_node.get_rwcec():
                next_node = child

        if next_node is None:
            return n.get_wcec()
        elif n.get_type() == CFGNodeType.PSEUDO:
            path.remove((n, n.get_wcec()))
            path.append((n, n.get_refnode_rwcec()))
            return (n.get_refnode_rwcec() +
                    self._find_worst_path(next_node, path))

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

        path.append((n, n.get_wcec()))
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

            Note I: only the most external loop is handled. So, loops nested are
            not supported.

            Note II: for each path found, even if it is not the best one, keep
            it in cached to be reused.

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

        tmp_path = cfg_path = None
        for child in n.get_children():
            if child.get_type() != CFGNodeType.PSEUDO:
                data = (child, child.get_wcec())
                path.append(data)
                tmp_path = self._find_mid_path(child, path,
                        newrwcec + child.get_wcec(), urwcec, lrwcec, bestrwcec)
                path.remove(data)
            else:
                tmp_path = self._check_mid_path_loops(child, path,
                        newrwcec, urwcec, lrwcec, bestrwcec)

            # set the greatest cfg path
            if (tmp_path is not None
                    and (cfg_path is None or tmp_path.get_path_rwcec() >
                        cfg_path.get_path_rwcec())):
                cfg_path = tmp_path
                bestrwcec = cfg_path.get_path_rwcec()

        # get a new cfg path whose RWCEC is valid
        if n.get_children() == []:
            # keep the found path in cache
            self._mid_paths[newrwcec] = CFGPath(newrwcec, path)
            if newrwcec > bestrwcec:
                cfg_path = CFGPath(newrwcec, path)

        return cfg_path

    def _check_mid_path_cached(self, lrwcec, urwcec):
        """ Check if, for the given bounds, there is a middle path in cache
            whose RWCEC is in the range.

            Args:
                lrwcec (int): lower bound
                urwcec (int): upper bound

            Returns:
                CFGPath object if there is a valid RWCEC in the given range or
                None if there is not any path.
        """
        mid_rwcec = 0
        for rwcec in self._mid_paths:
            if rwcec > mid_rwcec and lrwcec < rwcec and rwcec < urwcec:
                mid_rwcec = rwcec

        if mid_rwcec > 0:
            return self._mid_paths[mid_rwcec]
        return None

    def _check_mid_path_loops(self, child, path, newrwcec, urwcec, lrwcec,
            bestrwcec):
        tmp_path = cfg_path = None

        if child.get_start_line() in self._visited_loops:
            paths_visited = self._visited_loops[child.get_start_line()]
            for rwcec in list(self._mid_paths):
                if paths_visited == 0:
                    break
                mid_path = self._mid_paths[rwcec].get_path()
                index = -1
                for i in range(0, len(mid_path)):
                    node = mid_path[i][0]
                    if node == child:
                        index = i
                        break
                if index > -1:
                    new_path = path + list(mid_path[index:])
                    newrwcec = 0
                    for node, wcec in new_path:
                        newrwcec += wcec
                    tmp_path = CFGPath(newrwcec, new_path)
                    if newrwcec not in self._mid_paths:
                        paths_visited -= 1
                    self._mid_paths[newrwcec] = tmp_path
                    if newrwcec > bestrwcec:
                        bestrwcec = tmp_path.get_path_rwcec()
                        if (cfg_path is None or tmp_path.get_path_rwcec() >
                                    cfg_path.get_path_rwcec()):
                            cfg_path = tmp_path
                            bestrwcec = cfg_path.get_path_rwcec()
            return cfg_path

        num_of_mid_paths = len(self._mid_paths)
        for i in range(0, child.get_loop_iters() + 1):
            loop_wcec = child.get_refnode_rwcec() - child.get_wcec()
            loop_wcec = float(loop_wcec) / child.get_loop_iters()
            loop_wcec = child.get_wcec() + (loop_wcec * i)
            loop_wcec = int(math.ceil(loop_wcec))

            if (self._mid_paths == {}
                    or child.get_start_line() not in self._visited_loops):
                data = (child, loop_wcec)
                path.append(data)
                tmp_path = self._find_mid_path(child, path,
                        newrwcec + loop_wcec, urwcec, lrwcec, bestrwcec)
                path.remove(data)
                self._visited_loops[child.get_start_line()] = 1
            else:
                prev_loop_wcec = child.get_refnode_rwcec() - child.get_wcec()
                prev_loop_wcec = float(prev_loop_wcec) / child.get_loop_iters()
                prev_loop_wcec = child.get_wcec() + (prev_loop_wcec * (i - 1))
                prev_loop_wcec = int(math.ceil(prev_loop_wcec))
                data = (child, prev_loop_wcec)
                for rwcec in list(self._mid_paths):
                    if data in self._mid_paths[rwcec].get_path():
                        new_path = list(self._mid_paths[rwcec].get_path())
                        index = new_path.index(data)
                        new_data = (child, loop_wcec)
                        new_path[index] = new_data
                        newrwcec = rwcec - prev_loop_wcec + loop_wcec
                        # keep the found path in cache
                        self._mid_paths[newrwcec] = CFGPath(newrwcec,
                                new_path)
                        if newrwcec > bestrwcec:
                            tmp_path = CFGPath(newrwcec, new_path)
                            bestrwcec = tmp_path.get_path_rwcec()

            # set the greatest cfg path by exploring each loop iteration
            if (tmp_path is not None
                    and (cfg_path is None or tmp_path.get_path_rwcec() >
                        cfg_path.get_path_rwcec())):
                cfg_path = tmp_path
                bestrwcec = cfg_path.get_path_rwcec()

        found_mid_paths = len(self._mid_paths) - num_of_mid_paths
        self._visited_loops[child.get_start_line()] = found_mid_paths
        return cfg_path
