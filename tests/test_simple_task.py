import sys, os
import unittest

sys.path.insert(0, '../src')

from cfg import cfg, cfg2graphml
from sim import cfg_paths, sim


class TestSimpleTask(unittest.TestCase):
    """ Simulate a simple test case of one task execution to validate
        implementation.

        Attributes:
            _graph (CFG): control flow graph
            _cfgpaths (CFGPaths): object to find worst, best and middle paths
            _simulate (SimDVFS): object to simulate path execution and print
                results.
    """

    def _find_file(self, name, check_dir='c_files'):
        """ Find a c file by name, taking into account the current dir can be
            in a couple of typical places
        """
        testdir = os.path.dirname(__file__)
        name = os.path.join(testdir, check_dir, name)
        return name

    def test_simple_worst_case_mine(self):
        test_name = self.test_simple_worst_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        self._check_result(wpath, False, result_check, result_ok)

    def test_simple_worst_case_valentin(self):
        test_name = self.test_simple_worst_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        self._check_result(wpath, True, result_check, result_ok)

    def test_simple_best_case_mine(self):
        test_name = self.test_simple_best_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        bpath = self._cfgpaths.find_best_path(self._graph)
        self._check_result(bpath, False, result_check, result_ok)

    def test_simple_best_case_valentin(self):
        test_name = self.test_simple_best_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        bpath = self._cfgpaths.find_best_path(self._graph)
        self._check_result(bpath, True, result_check, result_ok)

    def test_simple_approx_best_case_mine(self):
        test_name = self.test_simple_approx_best_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        approxPath = self._cfgpaths.find_approximate_best_path(self._graph,
                0.2)
        self._check_result(approxPath, False, result_check, result_ok)

    def test_simple_approx_best_case_valentin(self):
        test_name = self.test_simple_approx_best_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        approxPath = self._cfgpaths.find_approximate_best_path(self._graph,
                0.2)
        self._check_result(approxPath, True, result_check, result_ok)

    def test_simple_middle_case_mine(self):
        test_name = self.test_simple_middle_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        mpath = self._cfgpaths.find_middle_path(self._graph)
        self._check_result(mpath, False, result_check, result_ok)

    def test_simple_middle_case_valentin(self):
        test_name = self.test_simple_middle_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        mpath = self._cfgpaths.find_middle_path(self._graph)
        self._check_result(mpath, True, result_check, result_ok)

    def _read_config_file(self):
        """ Get task and environment information of a configuration file.

            Args:
                config_file_name (string): configuration file name

            Returns:
                (float) task's WCEC
                (float) task's deadline
                (float) initial frequency to be used
                (dic) freqs_volt: dictionary where key is the frequency and
                    supply voltage to use the given frequency is the value
        """
        wcec = 0
        deadline = 0
        jitter = 0
        init_freq = 0
        freqs_volt = {}
        freqs = []
        volts = []
        config_file_name = self._find_file('sim_simple.config')
        with open(config_file_name, 'rU') as f:
            lines = f.readlines()
            try:
                for freq in lines[0].split():
                    freqs.append(float(freq))

                for volt in lines[1].split():
                    volts.append(float(volt))

                for i in range(0, len(freqs)):
                    freqs_volt[freqs[i]] = volts[i]

                data = lines[2].split()
                wcec = float(data[0])
                deadline = float(data[1])
                period = float(data[2])
                jitter = float(data[3])
                init_freq = float(data[4])
            except ValueError, IndexError:
                print 'Invalid data in config file'
                sys.exit(1)

        return wcec, deadline, period, jitter, init_freq, freqs_volt

    def _init_data(self):
        """ Initialize simulation data such as: graph, task's information, path
            finding and simulation objects.
        """
        # create CFG
        cfile = self._find_file('foo.c')
        self._graph = cfg.CFG(cfile)
        self._graph.make_cfg()

        # get and initialize data for simulation
        wcec, deadline, period, jit, init_freq, freqs_volt = \
                self._read_config_file()
        self._cfgpaths = cfg_paths.CFGPaths()
        self._simulate = sim.SimDVFS(
                wcec, 0, deadline, period, jit,
                init_freq, freqs_volt)

    def _check_result(self, path, valentin, result_check, result_ok):
        """ Simulate path execution and check if the result matches.

            Note: it should be used with worst and best paths.

            Args:
                path (list): each element is a tuple(CFGNode, WCEC)
                valentin (boolean): if Valentin's idea should be used
                result_check (string): file name to write test result
                result_ok (string): file name that should be used to check
                    result.
        """
        result_list = self._simulate.start_sim(None, 0, 0, '', path,
                valentin, '')

        with open(result_check, 'w') as f:
            for elem in result_list:
                freq = elem[0]
                wcec = elem[1]
                st = elem[2]
                et = elem[3]
                f.write('(%.0f, %0.f, %.2f, %.2f)\n' % (freq, wcec, st, et))

        test_assert = False
        with open(result_check, 'rU') as check_file,\
                open(result_ok, 'rU') as ok_file:
            check = check_file.read()
            ok = ok_file.read()
            test_assert = (check == ok)

        self.assertTrue(test_assert)
        os.remove(result_check)


if __name__ == '__main__':
    unittest.main()
