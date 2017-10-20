class State(object):

    def __init__(self, name, transitions=None, eps=None, is_end=False):
        self.name = name
        self.transitions = transitions or {}
        self.eps = eps or []
        self.is_end = is_end

    def follow_char(self, s):
        if s in self.transitions:
            return self.transitions[s]
        else:
            return []

    def add_transition(self, s, state):
        if s in self.transitions:
            self.transitions[s].append(state.name)
        else:
            self.transitions[s] = [state.name]

    def add_epsilon_transition(self, state):
        self.eps.append(state.name)


def build_subauto(s, qid=None):
    start = State('s_'+str(qid))
    end = State('end_'+str(qid))
    start.add_epsilon_transition(end)
    end.add_epsilon_transition(start)

    states = [start]
    count = 0
    state = start
    for char in s:
        next_state = State('{}_{}'.format(qid, count))
        state.add_transition(char, next_state)
        state = next_state
        states.append(state)
        count += 1
    state.add_epsilon_transition(start)
    state.add_epsilon_transition(end)
    states.append(end)
    return states


class Automata(object):

    def __init__(self, params):
        s1_states = build_subauto(''.join(params[:3]), qid='1')
        s2_states = build_subauto(''.join(params[3:]), qid='2')

        self.start = State('start')
        end = State('End')
        self.true_end = State('The True End', is_end=True)

        # add epsilons
        self.start.add_epsilon_transition(s1_states[0])
        self.start.add_epsilon_transition(s2_states[0])
        self.start.add_epsilon_transition(end)

        s1_states[-1].add_epsilon_transition(s2_states[0])
        s1_states[-1].add_epsilon_transition(end)
        s1_states[-1].add_epsilon_transition(self.start)
        s2_states[-1].add_epsilon_transition(end)
        s2_states[-1].add_epsilon_transition(self.start)

        end.add_epsilon_transition(self.start)
        end.add_epsilon_transition(self.true_end)

        states = [self.start, end, self.true_end] + s1_states + s2_states
        # for state in states:
        #     print state.name, state.transitions, state.eps
        self.state_map = {s.name: s for s in states}

    def test_string(self, s):
        current_states = self._run_eps_step({self.start.name})

        # now run each step
        for char in s:
            new_states = set()
            for state_name in current_states:
                state = self.state_map[state_name]
                new_states = new_states.union(state.follow_char(char))
            current_states = self._run_eps_step(new_states)
            if len(current_states) == 0:
                return False

        return self.true_end.name in current_states

    def _run_eps_step(self, current_states):
        found_more = True
        while found_more:
            found_more = False
            found = []
            for state in current_states:
                more = self.state_map[state].eps
                if len(set(more).difference(current_states)) > 0:
                    found += more
                    found_more = True
            current_states = current_states.union(found)

        return current_states


if __name__ == '__main__':
    from generator import *
    params = generate_params()
    print params
    a = Automata(params)

    for i in xrange(100):
        ex = generate_positive_example(params)
        if not a.test_string(ex):
            print ex



