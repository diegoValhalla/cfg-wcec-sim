import sys, os
import unittest

sys.path.insert(0, '../src')

from cfg import cfg, cfg2graphml
from sim import cfg_paths, sim_manager


class TestNoPreempTasks(unittest.TestCase):
    """ Simulate multiple tasks execution without preemption to validate
        implementation.

        Attributes:
            _graph (CFG): control flow graph
            _cfgpaths (CFGPaths): object to find worst, best and middle paths
            _simulate (SimDVFS): object to simulate path execution and print
                results.
    """

    def test_nopreemp_worst_case_valentin(self):
        test_name = self.test_nopreemp_worst_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        self._run_test('w', True, result_check, result_ok)

    def test_nopreemp_worst_case_mine(self):
        test_name = self.test_nopreemp_worst_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        self._run_test('w', False, result_check, result_ok)

    def test_nopreemp_middle_case_valentin(self):
        test_name = self.test_nopreemp_middle_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        self._run_test('m', True, result_check, result_ok)

    def test_nopreemp_middle_case_mine(self):
        test_name = self.test_nopreemp_middle_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        self._run_test('m', False, result_check, result_ok)

    def test_nopreemp_approx_best_case_mine(self):
        test_name = self.test_nopreemp_approx_best_case_mine.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        self._run_test('a', False, result_check, result_ok)

    def test_nopreemp_approx_best_case_valentin(self):
        test_name = self.test_nopreemp_approx_best_case_valentin.__name__
        result_ok = self._find_file(test_name + '.result')
        result_check = self._find_file(test_name + '.check')

        self._init_data()
        self._run_test('a', True, result_check, result_ok)

    def _find_file(self, name, check_dir='c_files'):
        """ Find a c file by name, taking into account the current dir can be
            in a couple of typical places
        """
        testdir = os.path.dirname(__file__)
        name = os.path.join(testdir, check_dir, name)
        return name

    def _init_data(self):
        """ Initialize simulation data such as: graph, task's information, path
            finding and simulation objects.
        """
        self._simManager = sim_manager.SimManager()
        self._set_simulation_config(self._simManager)

    def _set_simulation_config(self, simManager):
        """ Get task and environment information of a configuration file.

            Args:
                simManager (SimManager): simulation manager object
                config_file_name (string): configuration file name

            Returns:
                (float) task's WCEC
                (float) task's deadline
                (float) initial frequency to be used
                (dic) freqs_volt: dictionary where key is the frequency and
                    supply voltage to use the given frequency is the value
        """
        freqs = []
        volts = []
        freqs_volt = {}
        config_file = self._find_file('sim_nopreemp.config')
        with open(config_file, 'rU') as f:
            lines = f.readlines()
            try:
                for freq in lines[0].split():
                    freqs.append(float(freq))

                for volt in lines[1].split():
                    volts.append(float(volt))

                for i in range(0, len(freqs)):
                    freqs_volt[freqs[i]] = volts[i]

                for task in lines[2:]:
                    data = task.split()
                    wcec = float(data[1])
                    deadline = float(data[2])
                    period = float(data[3])
                    jitter = float(data[4])
                    init_freq = float(data[5])

                    cfile = data[0]
                    cfile = self._find_file(cfile)
                    graph = cfg.CFG(cfile)
                    graph.make_cfg()
                    simManager.add_task_sim(
                            graph, wcec, deadline, period, jitter,
                            init_freq, freqs_volt, 0.15)
            except ValueError, IndexError:
                print 'Invalid data in config file'
                sys.exit(1)

    def _run_test(self, path_name, valentin, result_check, result_ok):
        """ Simulate path execution and check if the result matches.

            Note: it should be used with worst and best paths.

            Args:
                path (list): each element is a tuple(CFGNode, WCEC)
                valentin (boolean): if Valentin's idea should be used
                result_check (string): file name to write test result
                result_ok (string): file name that should be used to check
                    result.
        """
        self._simManager.run_sim(path_name, valentin, result_check)

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
