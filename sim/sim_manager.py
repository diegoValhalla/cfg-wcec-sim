import os, sys, math

sys.path.insert(0, '../../src')

from cfg_paths import CFGPaths
from sim import SimDVFS


class SimManager(object):
    """ Manages the execution of all tasks and handle preemption according to
        their priority, period and jitter.

        Args:
            tasks_sims (dic): keeps all tasks that will be simulated. The key
                is task's priority and the value is a list where the first
                element is SimDVFS object that will simulate task execution,
                the second and the following elements are: WCEP, MCEP and ABCEP
            ready_queue (dic): keeps the time that each task will be invoked.
                The key is the time while value is the same as task_sims object
            priority_count (int): counter to set priority of each task while
                they are added to simulation manager. Note: less value means
                high priority
            sim_time (float): simulation time
    """
    def __init__(self):
        self._tasks_sims = {}
        self._ready_queue = {}
        self._priority_count = 0
        self._sim_time = 0

    def get_sim_time(self):
        """ Returns (float) current simulation time
        """
        return self._sim_time

    def add_sim_time(self, time):
        self._sim_time += time

    def add_task_sim(
            self, graph, wcec, deadline, period, jitter, init_freq,
            freqs_volt, approx_percent):
        """ Simulate all tasks execution by checking their priority and
            periods. It also is responsible to schedule when current task will
            be simulate again based on its period and jitter.

            Args:
                graph (CFG): control flow graph
                wcec (float): task's WCEC
                deadline (float): task's new deadline equals to response time
                period (float): task's period
                jitter (float): task's jitter
                init_freq (float): task's initial frequency
                freqs_volt (dic): dictionary where key is the frequency and
                    supply voltage to use the given frequency is the value
                per_cent (float): how much per cent from WCEC should be
                    approximate best path.
        """
        self._priority_count += 1
        simulate = SimDVFS(
                wcec, self._priority_count, deadline, period,
                jitter, init_freq, freqs_volt)

        cfg_paths = CFGPaths()
        wpath = cfg_paths.find_worst_path(graph)
        mpath = cfg_paths.find_middle_path(graph)
        abpath = cfg_paths.find_approximate_best_path(graph, approx_percent)
        if abpath is None:
            print 'approximate best path is not available'
            sys.exit(1)

        self._tasks_sims[self._priority_count] = (
                simulate, wpath, mpath, abpath)

    def _gcd(self, x, y):
        return self._gcd(y, x % y) if (y > 0) else x

    def _lcm(self, nums):
        if len(nums) == 0:
            return -1

        z = nums[0]
        for y in nums[1:]:
            x, y = max(z, y), min(z, y)
            z = (x * y) / self._gcd(x, y)

        return z

    def run_sim(self, path_name='w', valentin=False, show_result=''):
        """ Simulate all tasks execution by checking their priority and
            periods. It also is responsible to schedule when current task will
            be simulate again based on its period and jitter.

            Args:
                path_name (string): current path name 'w' (worst), 'm' (middle)
                    or 'a' (approximated best path)
                valentin (boolean): if Valentin's idea should be used
                show_result (string): file name to write simulation results. If
                    anyone is given, there is not any writing
        """
        # check if the current file exist, if so, remove it
        try:
            with open(show_result, 'rU') as f:
                pass
            os.remove(show_result)
        except IOError as e:
            pass # file does not exist

        self._sim_time = 0
        call_time = 0
        deadlines = []

        # all tasks are called at time 0 initialy
        self._ready_queue = {}
        for task_prio in self._tasks_sims:
            task = self._tasks_sims[task_prio][0]
            self._ready_queue[task_prio] = call_time
            deadlines.append(task.get_period())

        # set stop constraint to be equal to the period of less priority
        task_prio = max(self._tasks_sims) # less priority task
        task = self._tasks_sims[task_prio]
        stop_time = task[0].get_deadline()
        #stop_time = self._lcm(deadlines)

        while True:
            # at this point, there is no preemption. Then, get task from ready
            # queue whose call time is the smallest one
            task_prio = -1
            call_time = -1
            for next_task_prio in self._ready_queue:
                next_call_time = self._ready_queue[next_task_prio]
                if call_time == -1 or next_call_time < call_time:
                    task_prio = next_task_prio
                    call_time = next_call_time
            task = self._tasks_sims[task_prio][0]
            del self._ready_queue[task.get_priority()]

            # at this point, there is no task running, that's why sim time is
            # updated to the closer time that has a task.
            if self._sim_time < call_time:
                # note: update sim time only if it is less than the current
                # task call time
                self._sim_time = call_time
            if self._sim_time >= stop_time:
                break

            # get task path to execute
            if path_name == 'w':
                path = self._tasks_sims[task_prio][1]
            elif path_name == 'm':
                path = mpath = self._tasks_sims[task_prio][2]
            elif path_name == 'a':
                path = self._tasks_sims[task_prio][3]

            # check if jitter has already passed. If condition is false, jitter
            # has passed, if it is true, sum to sim time how much time must be
            # passed to jitter be fully done
            if call_time + task.get_jitter() > self._sim_time:
                self._sim_time += call_time + task.get_jitter() - self._sim_time

            # run simulation
            result = task.start_sim(
                    self, call_time, self._sim_time, path_name,
                    path, valentin, show_result)

            # set next execution time of the current task
            next_call_time = call_time + task.get_period()
            self._ready_queue[task.get_priority()] = next_call_time

    def check_preemp(self, path_name, curpriority, time_past, time_to_execute,
            valentin, result_file):
        """ Check if any preemption should happen during the execution of the
            new node. If during 'time_to_execute' there is a preemption, then
            check how much time was passed before preemption, and also check
            how much time the current task waits until be resumed.

            Args:
                path_name (string): current path name 'w' (worst), 'm' (middle)
                    or 'a' (approximated best path)
                time_past (float): time that was already executed by current
                    task, but it was not added yet to sim time
                time_to_execute (float): time that could leads to preemption
                    during its execution
                valentin (boolean): if Valentin's idea should be used
                show_result (string): file name to write simulation results. If
                    anyone is given, there is not any writing

            Returns:
                (tuple) None if there was not any preemption or a 2-elements
                    tuple where the first one is how much time task still
                    consumed before be preempted. Then, the second element
                    means how long the preempted task wait until its execution
                    could be resumed
        """
        # check if a preemption will happen
        next_task_info = self._get_next_task_info(
                            curpriority,
                            self._sim_time + time_past + time_to_execute)
        if next_task_info is None:
            return None

        # get preemption exact moment, so call time + jitter is always greater
        # or equal to sim time at this point. Moreover, get how much time
        # current task still runned before it was been preempted
        next_call_time = next_task_info[0]
        next_task = next_task_info[2]
        self._sim_time += time_past
        time_still_running = 0
        time_still_running = (next_task_info[0] +
                next_task_info[2].get_jitter() - self._sim_time)

        # set new simulation time and when current task was stopped
        self._sim_time = next_call_time + next_task.get_jitter()
        stop_time_for_preemp = self._sim_time

        # preemption
        while True:
            call_time = next_task_info[0]
            task_prio = next_task_info[1]
            task = next_task_info[2]
            if not result_file:
                print '\n -- %d preempt by %d at %.2f' % (curpriority, task_prio,
                        self._sim_time)

            # get task path to execute
            if path_name == 'w':
                path = self._tasks_sims[task_prio][1]
            elif path_name == 'm':
                path = mpath = self._tasks_sims[task_prio][2]
            elif path_name == 'a':
                path = self._tasks_sims[task_prio][3]

            # run simulation
            result = task.start_sim(
                    self, call_time, self._sim_time, path_name, path,
                    valentin, result_file)

            # set next execution time of the current task
            next_call_time = call_time + task.get_period()
            self._ready_queue[task.get_priority()] = next_call_time

            # check if a preemption will happen
            next_task_info = self._get_next_task_info(
                                curpriority,
                                self._sim_time)
            if next_task_info is None:
                break

        # how much time task was waiting to return execution
        wait_preemp_time = self._sim_time - stop_time_for_preemp
        return (time_still_running, wait_preemp_time)

    def _get_next_task_info(self, curpriority, sim_updated_time):
        """ Check if a preemption may happen by searching all tasks whose
            priority is greater than current one. After that, check if its
            its call time is less than current sim time.

            Args:
                curpriority (int): priority of the current path
                sim_updated_time (float): simulation time updated if current
                    task node is executed

            Returns:
                (tuple) None if there was not any preemption or a 3-elements
                    tuple where the first one is the call time of next task.
                    Then, the second element means next task priority while the
                    last element is the task (SimDVFS object) itself.
        """
        if self._ready_queue.keys() == []: return None
        next_task_prio = -1
        next_call_time = -1
        for prio in self._ready_queue:
            prio_call_time = self._ready_queue[prio]
            prio_task = self._tasks_sims[prio][0]
            if ((next_task_prio == -1 or prio < next_task_prio) and
                    prio < curpriority and prio_call_time +
                    prio_task.get_jitter() < sim_updated_time):
                next_task_prio = prio
                next_call_time = prio_call_time

        if next_task_prio == -1:
            return None
        return (next_call_time,
                next_task_prio,
                self._tasks_sims[next_task_prio][0])
