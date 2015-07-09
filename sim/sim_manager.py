import sys, math

sys.path.insert(0, '../../src')

from cfg_paths import CFGPaths
from sim import SimDVFS


class SimManager(object):

    def __init__(self):
        self._tasks_sims = {}
        self._running_stack = []
        self._ready_queue = {}
        self._priority_count = 0
        self._sim_time = 0

    def get_sim_time(self):
        return self._sim_time

    def add_task_sim(
            self, graph, wcec, deadline, period, jitter, init_freq,
            freqs_volt, approx_percent):

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

            # update sim time only if it is less than the current task call
            # time
            # at this point, there is no task running, that's why sim time is
            # updated
            if self._sim_time < call_time:
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

            # run simulation
            result = task.start_sim(
                    self, call_time, self._sim_time, path_name, path,
                    valentin, show_result)
            self._sim_time += task.get_time_executed()

            # set next execution time of the current task
            next_call_time = call_time + task.get_period()
            if next_call_time not in self._ready_queue:
                self._ready_queue[next_call_time] = []
            self._ready_queue[next_call_time].append(task.get_priority())

    def check_preemp(self, path_name, curpriority, time_past, time_to_execute,
            valentin, result_file):
        """
            Args:
                time_past (float): time that was already executed by current
                    task, but it was not added yet to sim time
                time_to_execute (float): time that could leads to preemption
                    during its execution
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
        # or equal to sim time at this point
        # get how much time current task still runned before it was been
        # preempted
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
            print '  %d preemped by %d at %.2f' % (curpriority, task_prio,
                    self._sim_time)

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
            self._sim_time += task.get_time_executed()

            # set next execution time of the current task
            next_call_time = call_time + task.get_period()
            if next_call_time not in self._ready_queue:
                self._ready_queue[next_call_time] = []
            self._ready_queue[next_call_time].append(task.get_priority())

            # check if a preemption will happen again
            call_time = min(self._ready_queue.keys()) # earliest time
            next_task_prio = min(self._ready_queue[call_time])
            next_task = self._tasks_sims[next_task_prio][0]
            if (call_time + next_task.get_jitter() >= self._sim_time or
                    next_task_prio > curpriority):
                break

        # how much time task was waiting to return execution
        wait_preemp_time = self._sim_time - stop_time_for_preemp
        return (time_still_running, wait_preemp_time)
