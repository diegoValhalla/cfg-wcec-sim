import sys, math

sys.path.insert(0, '../../src')

from cfg_paths import CFGPath

from cfg.cfg import CFG
from cfg.cfg_nodes import CFGNodeType, CFGEntryNode, CFGNode


class SimDVFS(object):
    """ Simulates path execution and holds each frequency changing information,
        such as the number of cycles executed with the same frequency before
        changing it. It also prints the results.

        Args:
            wcec (float): task's WCEC
            priority (int): task's priority
            deadline (float): task's new deadline equals to response time
            period (float): task's period
            jitter (float): task's jitter
            init_freq (float): task's initial frequency
            freqs_volt (dic): dictionary where key is the frequency and supply
                voltage to use the given frequency is the value
            overheadB (float): cycles overhead of changing frequency in type-B
                edges
            overheadL (float): cycles overhead of changing frequency in type-L
                edges

        Attributes:
            _freqs_available (list): list of the supported frequencies
            _freqs_volt (dic): key is the frequency and voltage is the value
            _deadline (float): task's deadline
            _typeB_overhead (float): cycles overhead of typeB edges operations
            _typeL_overhead (float): cycles overhead of typeL edges operations
            _curfreq (float): current frequency being used in path execution
            _cpc_consumed (float): current path cycles consumed so far in path
                execution with the same frequency
            _wcec_consumed (float): cycles consumed from WCEP. Saved execution
                cycles are taking into account here
            _sec (float): saved execution cycles which means, how many cycles
                were not executed because of a type-B or type-L edge
            _total_spent_time (float): total time spent by a task in one
                execution
            _start_time (float): when task simulation starts
            _call_time (float): when task simulation was called to start. It
                does not mean that task simulation start at the sime time
            _freq_cycles_consumed (list): list to store path execution history
                where each element is a tuple(frequency used, cycles consumed
                by the given frequency)
    """
    def __init__(
            self, wcec, priority=0, deadline=0, period=0, jitter=0,
            init_freq=0, freqs_volt={}, overheadB=100, overheadL=100):
        self._wcec = wcec
        self._priority = priority
        self._deadline = deadline
        self._period = period
        self._jitter = jitter
        self._init_freq = init_freq
        self._freqs_volt = freqs_volt
        self._freqs_available = sorted(list(freqs_volt.keys()))
        self._typeB_overhead = float(overheadB)
        self._typeL_overhead = float(overheadL)
        self._total_spent_time = self._jitter

    def _init_data(self):
        """ Initializes main data to keep track.
        """
        self._curfreq = 0
        self._cpc_consumed = 0
        self._wcec_consumed = 0
        self._sec = 0
        self._start_time = 0
        self._call_time = 0
        self._freq_cycles_consumed = []

    def get_deadline(self):
        return self._deadline

    def get_priority(self):
        return self._priority

    def get_period(self):
        return self._period

    def get_response_time(self):
        return self._total_spent_time

    def get_volt_from_freq(self, freq):
        """ Returns the supply voltage that matches to the given frequency

            Args:
                freq (float): frequency

            Returns:
                (float) supply voltage
        """
        return self._freqs_volt[freq]

    def start_sim(self, simManager, call_time, start_time, cfg_path,
            valentin=False):
        """ Start path execution and check for each typeB and typeL edges.

            Note: if Valentin's and Koreans' idea are both false, so they are
            used together (this is the given propose).

            Args:
                cfg_path (CFGPath): object contains the path for execution
                valentin (boolean): if Valentin's idea should be used

            Returns:
                (list) List where each element is a tuple made by the frequency
                used and how many cycles where consumed using the same
                frequency. This list order is according to frequency
                appearance. In other words, one frequency can be presented in
                more than one tuple since it was used in different moments.
        """
        if not isinstance(cfg_path, CFGPath): return

        self._init_data()
        self._start_time = start_time
        self._call_time = call_time
        self._curfreq = self._init_freq
        if start_time - call_time >= self._jitter:
            self._total_spent_time -= self._jitter
        else:
            self._total_spent_time = self._jitter - (start_time - call_time)

        path = cfg_path.get_path()
        for i in range(0, len(path)):
            n, wcec = path[i]
            self._cpc_consumed += wcec
            self._wcec_consumed += wcec
            # check if n is not last node, because typeB and typeL edges are
            # always check with the pair (parent, child)
            if valentin == False and i + 1 < len(path):
                child = path[i + 1][0]
                if n.get_type() == CFGNodeType.IF:
                    self._check_typeB_edge(n, child)
                elif n.get_type() == CFGNodeType.PSEUDO:
                    self._check_typeL_edge(n, wcec, child)
                self._wcec_consumed += self._sec
                self._sec = 0

        # store last information
        if self._cpc_consumed != 0:
            self._update_data(self._curfreq)

        return self._freq_cycles_consumed

    def _check_typeB_edge(self, n, child):
        """ Check if current child has a RWCEC less than the greatest RWCEC of
            a successor of current node. If it is, so this is a type-B edge.
            Then, compute typeB speed update ratio and change frequency if it is
            possible.

            Args:
                n (CFGNode): current node being visited
                child (CFGNode): child of n
                koreans (boolean): if Koreans' idea should be used
        """
        rwcec_succbi = n.get_rwcec() - n.get_wcec()
        rwcec_bj = child.get_rwcec()
        bjline = child.get_start_line()
        if rwcec_bj < rwcec_succbi:
            ratio = self._compute_typeB_sur(rwcec_succbi, rwcec_bj)
            self._change_freq(ratio)
            self._sec = rwcec_succbi - rwcec_bj

    def _compute_typeB_sur(self, rwcec_wsbi, rwcec_bj):
        """ Compute speed update ratio from type-B edge
              r(bi, bj) = RWCEC(bj) / (RWCEC(WORST_SUCC(bi)) - typeB_overhead)

            Args:
                rwcec_wsbi (float): RWCEC of the worst successor of bi
                rwcec_bj (float): RWCEC of bj

            Returns:
                (float) speed update ratio from a type-B edge
        """
        if rwcec_wsbi - self._typeB_overhead <= 0:
            return float(1)
        return float(rwcec_bj) / (rwcec_wsbi - self._typeB_overhead)

    def _check_typeL_edge(self, n, loop_wcec, child):
        """ Compute typeL speed update ratio by using how many loop iterations
            were done in the given path and its WCEC of one execution. Then,
            change frequency if it is possible.

            Args:
                n (CFGNode): current node being visited
                loop_wcec (float): loop RWCEC using all its iterations
                child (CFGNode): child of n
                koreans (boolean): if Koreans' idea should be used
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
        self._change_freq(ratio)

    def _compute_typeL_sur(self, loop_wcec_once, loop_after_rwcec,
                loop_max_iter, runtime_iter):
        """ Compute speed update ratio from type-L edge
            r(bi,bout) = RWCEC(bout)/(RWCEC(bout) + SAVED(bi) - typeB_overhead)
            where bi is loop condition node.

            Args:
                loop_wcec_once (float): WCEC of one loop execution
                loop_after_rwcec (float): RWCEC of first node after loop
                    execution.
                loop_max_iter (float): maximum number of loop iterations
                runtime_iter (float): how many loop iterations were done at
                    runtime.

            Returns:
                (float) speed update ratio from a type-L edge
        """
        saved = self._compute_typeL_cycles_saved(loop_wcec_once,
                loop_max_iter, runtime_iter)
        self._sec = saved
        if loop_after_rwcec + saved - self._typeL_overhead <= 0:
            return float(1)
        return (float(loop_after_rwcec) /
                (loop_after_rwcec + saved - self._typeL_overhead))

    def _compute_typeL_cycles_saved(self, loop_wcec_once, loop_max_iter,
            runtime_iter):
        """ Compute how many cycles were not executed
            r(bi, bout) = RWCEC(bout)/(RWCEC(bout) + SAVED(bi) - typeB_overhead)
            where bi is loop condition node.

            Args:
                loop_wcec (float): WCEC of one loop execution
                loop_max_iter (float): maximum number of loop iterations
                runtime_iter (float): how many loop iterations were done at
                    runtime.

            Returns:
                (float) cycles that were not executed from a type-L edge
        """
        return loop_wcec_once * (loop_max_iter - runtime_iter)

    def _change_freq(self, ratio):
        """ Change frequency if it is possible by checking the given ratio
            value. If it is greater or equal than one, change it will not
            improve energy efficiency. Otherwise, map the new frequency to the
            list of available ones, apply it if it is not equal to the
            current frequency and save the history of updates.

            Args:
                ratio (float): the ratio of how less is the following path from
                    worst case.
                koreans (boolean): if Koreans' idea should be used
        """
        if ratio >= 1: return
        newfreq = self._curfreq * ratio
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
        """ Save the history of how many cycles where consumed using the
            current frequency and apply the new frequency.

            Args:
                newfreq (float): new frequency to be used in path execution
        """
        data = (self._curfreq, self._cpc_consumed)
        self._freq_cycles_consumed.append(data)
        self._total_spent_time += float(data[1]) / float(data[0])
        self._curfreq = newfreq
        self._cpc_consumed = 0

    def print_results(self, path_name, path_rwcec, freq_cycles_consumed,
            valentin, koreans):
        """ Print detailed information in standard output of a given result by
            checking which idea is being used.

            Note: This print function can't be used to middle path since it
            is made by the average result of all middle paths. So, there is no
            way to know the frequencies used in average.

            Args:
                path_name (string): if it is worst, best or average path
                path_rwcec (float): path RWCEC
                freq_cycles_consumed (list): result list of a path execution
                valentin (boolean): if Valentin's idea should be used
                koreans (boolean): if Koreans' idea should be used
        """
        result = '\n****** Result details ******\n'

        if valentin:
            result += '(valentin'
        elif koreans:
            result += '(koreans'
        else:
            result += '(mine'
        result += ' - ' + path_name + ')'
        result += '\n\n'

        ci = 0
        total_time = 0
        total_energy = 0
        for freq, cycles in freq_cycles_consumed:
            time_spent = float(cycles) / freq
            energy_consumed = float(cycles) * self._freqs_volt[freq]
            result += '  F: %.2f MHz\n' % freq
            result += '    Cycles: %.2f\n' % cycles
            result += '    Time: %.2fs\n' % time_spent
            result += '    Energy: %.2fJ\n\n' % energy_consumed
            ci += time_spent
            total_energy += energy_consumed

        result += '  *** Summary ***\n'
        result += '    RWCEC: %.2f\n' % path_rwcec
        result += '    Computing time: %.2f\n' % ci
        result += '    Response time: %.2fs\n' % self._total_spent_time
        result += '    Deadline: %.2fs\n' % self._deadline
        result += '    Total Energy: %.2fJ' % total_energy
        print result

    def compare_result_to_worst_freq(self, path_name, path_rwcec,
            freq_cycles_consumed, time_spent, energy_consumed, valentin,
            koreans):
        """ Print summary information in standard output of a given result by
            comparing it to the used of greatest frequency available in the
            same path execution.

            Note: This print function should be used with middle paths and the
            parameters: time_spent and energy_consumed, should not be zero and
            freq_cycles_consumed should be an empty list in order to print
            average results.

            Args:
                path_name (string): if it is worst, best or average path
                path_rwcec (float): path RWCEC. If it is middle path, this
                    value is the average of all middle paths.
                freq_cycles_consumed (list): result list of a path execution
                time_spent (float): time spent executing the given path. If it
                    is middle path, this value is the average of all middle
                    paths.
                energy_consumed (float): energy consumed in the given path
                    execution. If it is middle path, this value is the average
                    of all middle paths.
                valentin (boolean): if Valentin's idea should be used
                koreans (boolean): if Koreans' idea should be used
        """
        result = '\n**** Energy Reduction (based on greatest frequency) ****\n'

        if valentin:
            result += '(valentin'
        elif koreans:
            result += '(koreans'
        else:
            result += '(mine'
        result += ' - ' + path_name + ')'
        result += '\n\n'

        worst_freq = max(self._freqs_available)
        worst_energy = float(path_rwcec) * self._freqs_volt[worst_freq]

        if freq_cycles_consumed != []:
            ci = 0
            energy_consumed = 0
            for freq, cycles in freq_cycles_consumed:
                ci += float(cycles) / freq
                energy_consumed += float(cycles) * self._freqs_volt[freq]

        result += '  RWCEC: %.2f\n' % path_rwcec
        result += '  Computing time: %.2fs\n' % ci
        result += '  Response time: %.2fs\n' % self._total_spent_time
        result += '  Deadline: %.2fs\n' % self._deadline
        result += '  Max frequency: %.2f MHz\n' % worst_freq
        result += '  Max energy: %.2fJ\n' % worst_energy
        result += '  Energy spent: %.2fJ\n' % energy_consumed
        result += ('  Energy reduction: %.2f%%\n' %
                    (100 - (energy_consumed * 100) / worst_energy))
        print result

    def print_to_csv(self, path_name, path_rwcec, freq_cycles_consumed,
            valentin):
        csv = 'v,' if (valentin) else 'm,'
        csv += path_name
        csv += ',%(path_rwcec).0f,%(energy_reduction).2f%%'
        csv += ',%(time_spent).2f,%(deadline).2f'

        ci = 0
        freqCount = len(self._freqs_available) - 1
        total_time = 0
        total_energy = 0
        for freq, cycles in freq_cycles_consumed:
            time_spent = float(cycles) / freq
            energy_consumed = float(cycles) * self._freqs_volt[freq]
            ci += time_spent
            total_energy += energy_consumed
            # print not used frequencies
            while freq < self._freqs_available[freqCount]:
                csv += ',-,-,-'
                freqCount -= 1
            freqCount -= 1
            csv += ',%.0f' % freq
            csv += ',%.0f' % cycles
            csv += ',%.2f' % time_spent
        while freqCount >= 0:
            csv += ',-,-,-'
            freqCount -= 1

        # compare to use of higher frequency
        worst_freq = max(self._freqs_available)
        worst_energy = float(path_rwcec) * self._freqs_volt[worst_freq]
        energy_reduction = (100 - (total_energy * 100) / worst_energy)

        csv %= {
            'path_rwcec': path_rwcec, 'energy_reduction': energy_reduction,
            'time_spent': time_spent, 'deadline': self._deadline
        }
        csv += '\n'

        dataLog = open('data.csv', 'a')
        dataLog.write(csv)
        dataLog.close()
