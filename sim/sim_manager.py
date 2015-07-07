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

    def run_sim(self, path_name='w', valentin=False, show_result=False):
        self._sim_time = 0
        call_time = 0

        # all tasks are called at time 0 initialy
        self._ready_queue = {}
        self._ready_queue[call_time] = []
        for task_prio in self._tasks_sims:
            task = self._tasks_sims[task_prio]
            self._ready_queue[call_time].append(task[0].get_priority())

        # set stop constraint to be equal to the period of less priority
        task_prio = max(self._tasks_sims) # less priority task
        task = self._tasks_sims[task_prio]
        stop_time = task[0].get_deadline()

        while True:
            call_time = min(self._ready_queue.keys()) # earliest time
            if call_time > self._sim_time: # jump in time to call time
                self._sim_time = call_time
            if self._sim_time >= stop_time:
                break

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
                    self, call_time, self._sim_time, path, valentin)
            if self._sim_time - call_time == 0: # task was not preempted
                self._sim_time += task.get_response_time()
            else: # sim time should always be greater than call time
                pass

            # set next execution time of the current task
            next_call_time = call_time + task.get_period()
            if next_call_time not in self._ready_queue:
                self._ready_queue[next_call_time] = []
            self._ready_queue[next_call_time].append(task.get_priority())

            # show task simulation results
            if isinstance(result, list) and show_result:
                task.print_to_csv(
                        path_name, path.get_path_rwcec(), result, valentin)

    def check_preemp(self, curpriority, time_to_execute):
        pass
