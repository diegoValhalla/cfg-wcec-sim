import sys, math

sys.path.insert(0, '../../src')

from cfg.cfg import CFG
from cfg.cfg_nodes import CFGNodeType, CFGEntryNode, CFGNode


class SimDVFS(object):
    def __init__(self, deadline=0, freqs_available=[]):
        self._deadline = deadline
        self._curfreq = 0
        self._freqs_available = freqs_available
        self._cycles_consumed = 0
        self._freq_cycles_consumed = []
        self._typeB_overhead = 0
        self._typeL_overhead = 0

    def start_sim(self, path, init_freq=0):
        """ Explore all functions in the C code

            Args:
                graph (cfg.CFG): CFG of the given C file
        """
        self._curfreq = init_freq
        for i in range(0, len(path)):
            n = path[i]
            self._cycles_consumed += n.get_wcec()
            if i + 1 < len(path): # check if n is not last node
                child = path[i + 1]
                if (n.get_type() == CFGNodeType.IF
                        or n.get_type() == CFGNodeType.ELSE_IF):
                    self._check_typeB_edge(n, child)
                elif n.get_type() == CFGNodeType.PSEUDO:
                    self._check_typeL_edge(n, child)

    def _check_typeB_edge(self, n, child):
        """ Check if current child has a RWCEC less than the greatest RWCEC of
            a successor of current node. If it is, so this is a type-B edge.

            Note: if child is an ELSE_IF node, the DVFS check must happen in
            its first child (then-statement), because there is no way to change
            frequency before a else-if condition.

            Args:
                clines (list): list of tuples (clines, text) from C code
                n (CFGNode): current node being visited
                child (CFGNode): child of n
        """
        rwcec_succbi = n.get_rwcec() - n.get_wcec()
        rwcec_bj = child.get_rwcec()
        bjline = child.get_start_line()
        if _rwcec_bj < rwcec_succbi:
            ratio = self._compute_typeB_sur(rwcec_succbi, rwcec_bj)
            self._change_freq(ratio)

    def _compute_typeB_sur(self, rwcec_wsbi, rwcec_bj):
        if rwcec_wsbi - overhead <= 0:
            return 1
        return rwcec_bj / (rwcec_wsbi - self._typeB_overhead)

    def _change_freq(self, ratio):
        if ratio >= 1: return
        newfreq = self._curfreq * ratio
        newfreq = math.ceil(newfreq)
        if newfreq < self._curfreq: # check if it is possible to change freq
            set_freq = 0
            for freq in self._freqs_available: # check for an available freq
                if freq >= newfreq and (set_freq == 0 or freq <= set_freq):
                    set_freq = freq
            if set_freq != 0: # if freq is available
                self._update_data(set_freq)

    def _update_data(self, newfreq):
        data = (self._curfreq, self._cycles_consumed)
        self._freq_cycles_consumed.append(data)
        self._curfreq = newfreq
        self._cycles_consumed = 0

    def _check_typeL_edge(self, n, child):
        """ Get loop information from current node and child and add DVFS code

            Args:
                n (CFGNode): current node being visited
                child (CFGNode): child of n
        """
        if n.get_loop_iters() != 0:
            loop_wcec_once = n.get_refnode_rwcec() / n.get_loop_iters()
        else:
            loop_wcec_once = n.get_refnode_rwcec()
        loop_cond_line = n.get_start_line()
        loop_max_iter = n.get_loop_iters()
        loop_after_line = child.get_start_line()
        loop_after_rwcec = child.get_rwcec()
        self._insert_typeL_info(loop_cond_line, loop_wcec_once,
                loop_max_iter, loop_after_line, loop_after_rwcec)

    def _insert_typeL_info(self, loop_cond_line, loop_wcec_once,
            loop_max_iter, loop_after_line, loop_after_rwcec):
        """ Gather all information from a type-L edge and simulate DVFS code
            execution.

            Args:
                bjline (int): start line of bj
                rwcec_bi (int): RWCEC of bi
                rwcec_bj (int): RWCEC of bj
        """
        pass

