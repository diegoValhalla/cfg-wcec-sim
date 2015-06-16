import sys, os
import unittest

sys.path.insert(0, '../src')

from cfg import cfg, cfg2graphml
from sim import cfg_paths, sim


class TestSimpleCase(unittest.TestCase):
    """ Simulate a simple test case to validate implementation.

        Attributes:
            _graph (CFG): control flow graph
            _init_freq (float): initial frequency to start path execution
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

    def test_worst_case_mine(self):
        test_name = self.test_worst_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        self._check_result(wpath, False, False, result_check, result_ok)

    def test_worst_case_valentin(self):
        test_name = self.test_worst_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        self._check_result(wpath, True, False, result_check, result_ok)

    def test_worst_case_koreans(self):
        test_name = self.test_worst_case_koreans.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        self._check_result(wpath, False, True, result_check, result_ok)

    def test_best_case_mine(self):
        test_name = self.test_best_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        bpath = self._cfgpaths.find_best_path(self._graph)
        self._check_result(bpath, False, False, result_check, result_ok)

    def test_best_case_valentin(self):
        test_name = self.test_best_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        bpath = self._cfgpaths.find_best_path(self._graph)
        self._check_result(bpath, True, False, result_check, result_ok)

    def test_best_case_koreans(self):
        test_name = self.test_best_case_koreans.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        bpath = self._cfgpaths.find_best_path(self._graph)
        self._check_result(bpath, False, True, result_check, result_ok)

    def test_middle_case_mine(self):
        test_name = self.test_middle_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        bpath = self._cfgpaths.find_best_path(self._graph)
        mpath = self._cfgpaths.find_mid_path(self._graph,
                    wpath.get_path_rwcec(), bpath.get_path_rwcec())
        self._check_result(mpath, False, False, result_check, result_ok)

    def test_middle_case_valentin(self):
        test_name = self.test_middle_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        bpath = self._cfgpaths.find_best_path(self._graph)
        mpath = self._cfgpaths.find_mid_path(self._graph,
                    wpath.get_path_rwcec(), bpath.get_path_rwcec())
        self._check_result(bpath, True, False, result_check, result_ok)

    def test_middle_case_koreans(self):
        test_name = self.test_middle_case_koreans.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        wpath = self._cfgpaths.find_worst_path(self._graph)
        bpath = self._cfgpaths.find_best_path(self._graph)
        mpath = self._cfgpaths.find_mid_path(self._graph,
                    wpath.get_path_rwcec(), bpath.get_path_rwcec())
        self._check_result(bpath, False, True, result_check, result_ok)

    def _read_config_file(self):
        """ Get task and environment information of a configuration file.

            Args:
                config_file_name (string): configuration file name

            Returns:
                (float) task's deadline
                (float) initial frequency to be used
                (dic) freqs_volt: dictionary where key is the frequency and
                    supply voltage to use the given frequency is the value
        """
        deadline = 0
        freqs_volt = {}
        freqs = []
        volts = []
        config_file_name = self._find_file('sim.config')
        with open(config_file_name, 'rU') as f:
            lines = f.readlines()
            try:
                deadline = float(lines[0].split()[0])

                for freq in lines[1].split():
                    freqs.append(float(freq))
                init_freq = max(freqs)

                for volt in lines[2].split():
                    volts.append(float(volt))

                for i in range(0, len(freqs)):
                    freqs_volt[freqs[i]] = volts[i]
            except ValueError, IndexError:
                print 'Invalid data in config file'
                sys.exit(1)

        return deadline, init_freq, freqs_volt

    def _init_data(self):
        """ Initialize simulation data such as: graph, task's information, path
            finding and simulation objects.
        """
        # create CFG
        cfile = self._find_file('test_simple_case.c')
        self._graph = cfg.CFG(cfile)
        self._graph.make_cfg()

        # get and initialize data for simulation
        deadline, init_freq, freqs_volt = self._read_config_file()
        self._init_freq = init_freq
        self._cfgpaths = cfg_paths.CFGPaths()
        self._simulate = sim.SimDVFS(deadline, freqs_volt)

    def _check_result(self, path, valentin, koreans, result_check, result_ok):
        """ Simulate path execution and check if the result matches.

            Note: it should be used with worst and best paths.

            Args:
                path (list): each element is a tuple(CFGNode, WCEC)
                valentin (boolean): if Valentin's idea should be used
                koreans (boolean): if Koreans' idea should be used
                result_check (string): file name to write test result
                result_ok (string): file name that should be used to check
                    result.
        """
        result_list = self._simulate.start_sim(path, self._init_freq,
                valentin, koreans)

        with open(result_check, 'w') as f:
            for elem in result_list:
                f.write(str(elem) + '\n')

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
