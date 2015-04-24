import sys, math

sys.path.insert(0, '../../src')

from cfg_paths import CFGPath

from cfg.cfg import CFG
from cfg.cfg_nodes import CFGNodeType, CFGEntryNode, CFGNode


class SimDVFS(object):
    def __init__(self, deadline=0, freqs_volt={}):
        self._freqs_available = list(freqs_volt.keys())
        self._freqs_volt = freqs_volt
        self._deadline = deadline
        self._typeB_overhead = 0
        self._typeL_overhead = 0

    def _init_data(self):
        self._curfreq = 0
        self._cycles_consumed = 0
        self._freq_cycles_consumed = []

    def start_sim(self, cfg_path, init_freq=0, valentin=False, koreans=False):
        """ Explore all functions in the C code

            Args:
                graph (cfg.CFG): CFG of the given C file
        """
        if not isinstance(cfg_path, CFGPath): return

        self._init_data()

        if koreans:
            self._curfreq = cfg_path.get_path_rwcec() / self._deadline
        else:
            self._curfreq = init_freq

        path = cfg_path.get_path()
        for i in range(0, len(path)):
            n, wcec = path[i]
            self._cycles_consumed += wcec
            # check if n is not last node
            if valentin == False and i + 1 < len(path):
                child = path[i + 1][0]
                if (n.get_type() == CFGNodeType.IF
                        or n.get_type() == CFGNodeType.ELSE_IF):
                    self._check_typeB_edge(n, child, koreans)
                elif n.get_type() == CFGNodeType.PSEUDO:
                    self._check_typeL_edge(n, wcec, child, koreans)

        # store last information
        if self._cycles_consumed != 0:
            self._update_data(self._curfreq)

        return self._freq_cycles_consumed

    def _check_typeB_edge(self, n, child, koreans=False):
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
        if rwcec_bj < rwcec_succbi:
            ratio = self._compute_typeB_sur(rwcec_succbi, rwcec_bj)
            self._change_freq(ratio, koreans)

    def _compute_typeB_sur(self, rwcec_wsbi, rwcec_bj):
        if rwcec_wsbi - self._typeB_overhead <= 0:
            return 1
        return float(rwcec_bj) / (rwcec_wsbi - self._typeB_overhead)

    def _check_typeL_edge(self, n, loop_wcec, child, koreans=False):
        """ Get loop information from current node and child and add DVFS code

            Args:
                n (CFGNode): current node being visited
                child (CFGNode): child of n
        """
        loop_max_iter = n.get_loop_iters()
        loop_after_line = child.get_start_line()
        loop_after_rwcec = child.get_rwcec()
        if loop_max_iter != 0:
            loop_wcec_once = ((n.get_refnode_rwcec() - n.get_wcec()) /
                                loop_max_iter)
        else:
            loop_wcec_once = n.get_refnode_rwcec()
        runtime_iter = (loop_wcec - n.get_wcec()) / loop_wcec_once

        ratio = self._compute_typeL_sur(loop_wcec_once, loop_after_rwcec,
                loop_max_iter, runtime_iter)
        self._change_freq(ratio, koreans)

    def _compute_typeL_sur(self, loop_wcec_once, loop_after_rwcec,
                loop_max_iter, runtime_iter):
        saved = self._compute_typeL_cycles_saved(loop_wcec_once,
                loop_max_iter, runtime_iter)
        if loop_after_rwcec + saved - self._typeL_overhead <= 0:
            return 1
        return (float(loop_after_rwcec) /
                (loop_after_rwcec + saved - self._typeL_overhead))

    def _compute_typeL_cycles_saved(self, loop_wcec_once, loop_max_iter,
            runtime_iter):
        return loop_wcec_once * (loop_max_iter - runtime_iter)

    def _change_freq(self, ratio, koreans=False):
        if ratio >= 1: return
        newfreq = self._curfreq * ratio
        if koreans:
            if newfreq < self._curfreq:
                self._update_data(newfreq)
        else:
            newfreq = math.ceil(newfreq)
            if newfreq < self._curfreq:
                # check for an available frequency - ceil operation
                # check for the smallest value that is greater than or equal to
                # new frequency
                set_freq = 0
                for freq in self._freqs_available:
                    if freq >= newfreq and (set_freq == 0 or freq <= set_freq):
                        set_freq = freq
                # if the new frequency value mapped into frequency set is equal
                # to current frequency, it does not update data, because
                # frequency is the same as before
                if set_freq != 0 and set_freq != self._curfreq:
                    self._update_data(set_freq)

    def _update_data(self, newfreq):
        data = (self._curfreq, self._cycles_consumed)
        self._freq_cycles_consumed.append(data)
        self._curfreq = newfreq
        self._cycles_consumed = 0

    def print_results(self, path_rwcec, freq_cycles_consumed, valentin,
            koreans):
        result = '\n****** Result details ******\n'

        if valentin:
            result += '(valentin)'
        elif koreans:
            result += '(koreans)'
        else:
            result += '(mine)'
        result += '\n\n'

        total_time = 0
        total_energy = 0
        for freq, cycles in freq_cycles_consumed:
            time_spent = float(cycles) / freq
            energy_consumed = float(cycles) * self._freqs_volt[freq]
            result += '  F: %.2f MHz\n' % freq
            result += '    Cycles: %.2f\n' % cycles
            result += '    Time: %.2fs\n' % time_spent
            result += '    Energy: %.2fJ\n\n' % energy_consumed
            total_time += time_spent
            total_energy += energy_consumed

        result += '  *** Summary ***\n'
        result += '    RWCEC: %.2f\n' % path_rwcec
        result += '    Deadline: %.2fs\n' % self._deadline
        result += '    Time Spent: %.2fs\n' % total_time
        result += '    Total Energy: %.2fJ' % total_energy
        print result

    def compare_result_to_worst_freq(self, path_rwcec, freq_cycles_consumed,
            valentin, koreans):
        result = '\n**** Energy Reduction (based on greatest frequency) ****\n'

        if valentin:
            result += '(valentin)'
        elif koreans:
            result += '(koreans)'
        else:
            result += '(mine)'
        result += '\n\n'

        worst_freq = max(self._freqs_available)
        worst_energy = float(path_rwcec) * self._freqs_volt[worst_freq]

        time_spent = 0
        energy_consumed = 0
        for freq, cycles in freq_cycles_consumed:
            time_spent += float(cycles) / freq
            energy_consumed += float(cycles) * self._freqs_volt[freq]

        result += '  RWCEC: %.2f\n' % path_rwcec
        result += '  Deadline: %.2fs\n' % self._deadline
        result += '  Time Spent: %.2fs\n' % time_spent
        result += '  Max frequency: %.2f MHz\n' % worst_freq
        result += '  Max energy: %.2fJ\n' % worst_energy
        result += '  Energy spent: %.2fJ\n' % energy_consumed
        result += ('  Energy reduction: %.2f%%\n' %
                    (100 - (energy_consumed * 100) / worst_energy))
        print result
