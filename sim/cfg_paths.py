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
            _all_paths (dic): holds all paths of a graph. The key is a path
                RWCEC, whereas the value is a CFGPath object.
    """
    def __init__(self):
        self._all_paths = {}
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

    def find_approximate_best_path(self, graph, per_cent):
        """ From the list of all paths between worst and best, return the one
            whose number of cycles is the greatest one less or equal to the
            given per cent of the WCEC.

            Args:
                graph (CFG): control flow graph
                per_cent (float): how much per cent from WCEC should be the
                    approximate best path.

            Returns:
                (CFGPath) object if there is a valid path whose RWCEC is in the
                range of lower and upper rates. Return None if there is not any
                path.
        """
        wcep = self.find_worst_path(graph)
        if wcep is None: return None
        all_paths = self._find_all_paths(graph)
        paths_rwcec = sorted(all_paths.keys())
        wcec = wcep.get_path_rwcec()

        approx_path = None
        for rwcec in paths_rwcec:
            if rwcec > math.ceil(wcec * per_cent):
                break
            approx_path = self._all_paths[rwcec]
        return approx_path

    def find_middle_path(self, graph):
        """ From the list of all paths between worst and best RWCEC, return the
            middle path of this list. If the list length if even, then the path
            with the greatest RWCEC is returned.

            Returns:
                CFGPath object if there is a valid middle path in the list of
                paths whose RWCEC are less than the worst and greater than the
                best one. Return None if there is not any path.
        """
        all_paths = self._find_all_paths(graph)
        paths_rwcec = sorted(all_paths.keys())
        mid_rwcec_idx = len(paths_rwcec) / 2

        if mid_rwcec_idx < len(paths_rwcec):
            return all_paths[paths_rwcec[mid_rwcec_idx]]
        return None

    def _find_all_paths(self, graph):
        """ Explore graph to find all paths.

            Args:
                graph (CFG): control flow graph

            Returns:
                (dic) Returns a dic where the key is the path RWCEC and the
                    value is the path itself.
        """
        if not isinstance(graph, CFG): return

        if self._all_paths == {}:
            for entry in graph.get_entry_nodes():
                start_node = entry.get_func_first_node()
                path = [(start_node, start_node.get_wcec())]
                self._find_all_paths_visit(start_node, path,
                        start_node.get_wcec(), 0)

        return self._all_paths

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

    def _find_all_paths_visit(self, n, path, newrwcec, bestrwcec):
        """ Find all possible paths from a CFG is explore and compute their
            RWCEC computed. By the end, when CFG's last node is reached, check
            if the RWCEC of this new path is better from the previous one. If
            so, keep track of its contents and continue to explore the other
            paths until there is no other path better than the one saved.

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
                tmp_path = self._find_all_paths_visit(child, path,
                        newrwcec + child.get_wcec(), bestrwcec)
                path.remove(data)
            else:
                tmp_path = self._find_all_paths_loops(child, path, newrwcec,
                            bestrwcec)

            # set the greatest cfg path
            if (tmp_path is not None
                    and (cfg_path is None or tmp_path.get_path_rwcec() >
                        cfg_path.get_path_rwcec())):
                cfg_path = tmp_path
                bestrwcec = cfg_path.get_path_rwcec()

        # get a new cfg path whose RWCEC is valid
        if n.get_children() == []:
            # keep the found path in cache
            self._all_paths[newrwcec] = CFGPath(newrwcec, path)
            if newrwcec > bestrwcec:
                cfg_path = CFGPath(newrwcec, path)

        return cfg_path

    def _find_all_paths_loops(self, child, path, newrwcec, bestrwcec):
        tmp_path = cfg_path = None

        if child.get_start_line() in self._visited_loops:
            paths_visited = self._visited_loops[child.get_start_line()]
            for rwcec in list(self._all_paths):
                if paths_visited == 0:
                    break
                found_path = self._all_paths[rwcec].get_path()
                index = -1
                for i in range(0, len(found_path)):
                    node = found_path[i][0]
                    if node == child:
                        index = i
                        break
                if index > -1:
                    new_path = path + list(found_path[index:])
                    newrwcec = 0
                    for node, wcec in new_path:
                        newrwcec += wcec
                    tmp_path = CFGPath(newrwcec, new_path)
                    if newrwcec not in self._all_paths:
                        paths_visited -= 1
                    self._all_paths[newrwcec] = tmp_path
                    if newrwcec > bestrwcec:
                        bestrwcec = tmp_path.get_path_rwcec()
                        if (cfg_path is None or tmp_path.get_path_rwcec() >
                                    cfg_path.get_path_rwcec()):
                            cfg_path = tmp_path
                            bestrwcec = cfg_path.get_path_rwcec()
            return cfg_path

        prev_all_paths_length = len(self._all_paths)
        for i in range(0, child.get_loop_iters() + 1):
            loop_wcec = child.get_refnode_rwcec() - child.get_wcec()
            loop_wcec = float(loop_wcec) / child.get_loop_iters()
            loop_wcec = child.get_wcec() + (loop_wcec * i)
            loop_wcec = int(math.ceil(loop_wcec))

            if (self._all_paths == {}
                    or child.get_start_line() not in self._visited_loops):
                data = (child, loop_wcec)
                path.append(data)
                tmp_path = self._find_all_paths_visit(child, path,
                        newrwcec + loop_wcec, bestrwcec)
                path.remove(data)
                self._visited_loops[child.get_start_line()] = 1
            else:
                prev_loop_wcec = child.get_refnode_rwcec() - child.get_wcec()
                prev_loop_wcec = float(prev_loop_wcec) / child.get_loop_iters()
                prev_loop_wcec = child.get_wcec() + (prev_loop_wcec * (i - 1))
                prev_loop_wcec = int(math.ceil(prev_loop_wcec))
                data = (child, prev_loop_wcec)
                for rwcec in list(self._all_paths):
                    if data in self._all_paths[rwcec].get_path():
                        new_path = list(self._all_paths[rwcec].get_path())
                        index = new_path.index(data)
                        new_data = (child, loop_wcec)
                        new_path[index] = new_data
                        newrwcec = rwcec - prev_loop_wcec + loop_wcec
                        # keep the found path in cache
                        self._all_paths[newrwcec] = CFGPath(newrwcec,
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

        found_paths_num = len(self._all_paths) - prev_all_paths_length
        self._visited_loops[child.get_start_line()] = found_paths_num
        return cfg_path
