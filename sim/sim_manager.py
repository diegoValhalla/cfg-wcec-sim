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

        # all tasks are called at time 0 initialy
        self._ready_queue = {}
        self._ready_queue[call_time] = []
        for task_prio in self._tasks_sims:
            task = self._tasks_sims[task_prio][0]
            if call_time not in self._ready_queue:
                self._ready_queue[call_time] = []
            self._ready_queue[call_time].append(task.get_priority())

        # set stop constraint to be equal to the period of less priority
        task_prio = max(self._tasks_sims) # less priority task
        task = self._tasks_sims[task_prio]
        stop_time = task[0].get_deadline()

        while True:
            # get task from ready queue by priority
            call_time = min(self._ready_queue.keys()) # earliest time
            task_prio = min(self._ready_queue[call_time])
            task = self._tasks_sims[task_prio][0]
            self._ready_queue[call_time].remove(task_prio)

            # at this point, there is no task running, that's why sim time is
            # updated to the closer time that has a task.
            if self._sim_time < call_time:
                # note: update sim time only if it is less than the current
                # task call time
                self._sim_time = call_time
            if self._sim_time >= stop_time:
                break

            # remove call time from ready queue if there are no more tasks to
            # execute in the list of this time
            if self._ready_queue[call_time] == []:
                del self._ready_queue[call_time]

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
            if next_call_time not in self._ready_queue:
                self._ready_queue[next_call_time] = []
            self._ready_queue[next_call_time].append(task.get_priority())

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
        if self._ready_queue.keys() == []: return ()

        # check if next task call time in ready queue preempts current one and
        # check if next task priority is less than current one
        call_time = min(self._ready_queue.keys()) # earliest time
        next_task_prio = min(self._ready_queue[call_time])
        next_task = self._tasks_sims[next_task_prio][0]
        if call_time + next_task.get_jitter() >= (self._sim_time + time_past +
                time_to_execute) or next_task_prio > curpriority:
            return None # no preemption

        # get preemption exact moment, so call time + jitter is always greater
        # or equal to sim time at this point. Moreover, get how much time
        # current task still runned before it was been preempted
        self._sim_time += time_past
        time_still_running = 0
        time_still_running = (call_time + next_task.get_jitter() -
                self._sim_time)

        # set new simulation time and when current task was stopped
        self._sim_time = call_time + next_task.get_jitter()
        stop_time_for_preemp = self._sim_time

        # preemption
        while True:
            # set preemption time
            call_time = min(self._ready_queue.keys()) # earliest time
            task_prio = min(self._ready_queue[call_time])
            if not result_file:
                print '\n  -- %d preemped by %d at %.2f --' % (curpriority,
                        task_prio, self._sim_time)

            # get task from ready queue by priority
            task_prio = min(self._ready_queue[call_time])
            task = self._tasks_sims[task_prio][0]
            self._ready_queue[call_time].remove(task_prio)

            # remove call time from ready queue if there are no more tasks to
            # execute in the list of this time
            if self._ready_queue[call_time] == []:
                del self._ready_queue[call_time]

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
            if next_call_time not in self._ready_queue:
                self._ready_queue[next_call_time] = []
            self._ready_queue[next_call_time].append(task.get_priority())

            # check if there is a new preemption
            call_time = min(self._ready_queue.keys()) # earliest time
            next_task_prio = min(self._ready_queue[call_time])
            next_task = self._tasks_sims[next_task_prio][0]
            if (call_time + next_task.get_jitter() >= self._sim_time or
                    next_task_prio > curpriority):
                break

        # how much time task was waiting to return execution
        wait_preemp_time = self._sim_time - stop_time_for_preemp
        return (time_still_running, wait_preemp_time)
