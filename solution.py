import math
from collections import defaultdict, namedtuple
from typing import Dict, List

# from constants import *  # commented because constants is already imported in environment.py
from environment import *
from state import State

"""
solution.py

This file is a template you should use to implement your solution.

You should implement each section below which contains a TODO comment.

Last updated by njc 08/09/22
"""

ProbAndReward = namedtuple('ProbAndReward', ['prob', 'reward'])


class Solver:

    def __init__(self, environment: Environment):
        self.environment = environment
        #
        # TODO: Define any class instance variables you require (e.g. dictionary mapping state to VI value) here.
        #
        self.state_value: Dict[State, float] = None
        self.vi_delta = 0.0
        self.vi_delta_threshold = self.environment.epsilon * 0.2
        self.vi_policy: Dict[State, int] = defaultdict(lambda: 0)
        self.state_action: Dict[State, int] = defaultdict(None)
        self.possible_states: List[State] = None
        self.terminal_states: List[State] = None

        # probability = transitions[s][a][s_prime]
        self.transitions: Dict[State, Dict[int, Dict[State, ProbAndReward[float, float]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: (0, 0))))

        self.get_all_states_and_transition_probabilities()
        self.terminal_states = {state for state in self.possible_states if self.environment.is_solved(state)}

    # === Value Iteration ==============================================================================================

    def vi_initialise(self):
        """
        Initialise any variables required before the start of Value Iteration.
        """
        #
        # TODO: Implement any initialisation for Value Iteration (e.g. building a list of states) here. You should not
        #  perform value iteration in this method.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        self.state_value: Dict[State, float] = defaultdict(lambda: random.random())
        self.vi_delta = math.inf
        self.vi_delta_threshold = self.environment.epsilon * 0.2
        self.state_action: Dict[State, int] = defaultdict(None)
        self.transitions: Dict[State, Dict[int, Dict[State, float]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

        self.get_all_states_and_transition_probabilities()
        self.terminal_states = {state for state in self.possible_states if self.environment.is_solved(state)}

        # TODO: For some strange reason, keeping state-value of terminal states 50 helps converge faster.
        for state in self.terminal_states:
            self.state_value[state] = 100

        print(f'=============================================================================================')
        print(f'Total states: {len(self.possible_states)}, terminal states: {len(self.terminal_states)}')
        print(f'=============================================================================================')
        # for episode in range(10):
        #     self.vi_plan_offline()

    def vi_is_converged(self):
        """
        Check if Value Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        #
        # TODO: Implement code to check if Value Iteration has reached convergence here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        return self.vi_delta < self.vi_delta_threshold

    def vi_iteration(self):
        """
        Perform a single iteration of Value Iteration (i.e. loop over the state space once).
        """
        #
        # TODO: Implement code to perform a single iteration of Value Iteration here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        delta = 0
        for state in self.possible_states:

            if state in self.terminal_states:
                continue

            old_value = self.state_value[state]
            new_value = -math.inf

            optimal_action = None
            for action in ROBOT_ACTIONS:
                total = 0
                for s_prime in self.transitions[state][action].keys():
                    prob_and_reward = self.transitions[state][action][s_prime]
                    total += prob_and_reward.prob * (prob_and_reward.reward + (self.state_value[s_prime]))

                if total > new_value:
                    new_value = total
                    optimal_action = action

            if optimal_action is not None:
                self.vi_policy[state] = optimal_action

            self.state_value[state] = new_value

            delta = max(delta, abs(new_value - old_value))

        self.vi_delta = delta

    def vi_plan_offline(self):
        """
        Plan using Value Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.vi_initialise()
        while not self.vi_is_converged():
            self.vi_iteration()

    def vi_get_state_value(self, state: State):
        """
        Retrieve V(s) for the given state.
        :param state: the current state
        :return: V(s)
        """
        #
        # TODO: Implement code to return the value V(s) for the given state (based on your stored VI values) here. If a
        #  value for V(s) has not yet been computed, this function should return 0.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        return self.state_value[state]

    def vi_select_action(self, state: State):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of ROBOT_ACTIONS)
        """
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored VI values) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        return self.vi_policy[state]

    # === Policy Iteration =============================================================================================

    def pi_initialise(self):
        """
        Initialise any variables required before the start of Policy Iteration.
        """
        #
        # TODO: Implement any initialisation for Policy Iteration (e.g. building a list of states) here. You should not
        #  perform policy iteration in this method. You should assume an initial policy of always move FORWARDS.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def pi_is_converged(self):
        """
        Check if Policy Iteration has reached convergence.
        :return: True if converged, False otherwise
        """
        #
        # TODO: Implement code to check if Policy Iteration has reached convergence here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def pi_iteration(self):
        """
        Perform a single iteration of Policy Iteration (i.e. perform one step of policy evaluation and one step of
        policy improvement).
        """
        #
        # TODO: Implement code to perform a single iteration of Policy Iteration (evaluation + improvement) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    def pi_plan_offline(self):
        """
        Plan using Policy Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.pi_initialise()
        while not self.pi_is_converged():
            self.pi_iteration()

    def pi_select_action(self, state: State):
        """
        Retrieve the optimal action for the given state (based on values computed by Value Iteration).
        :param state: the current state
        :return: optimal action for the given state (element of ROBOT_ACTIONS)
        """
        #
        # TODO: Implement code to return the optimal action for the given state (based on your stored PI policy) here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

    # === Helper Methods ===============================================================================================
    #
    #
    # TODO: Add any additional methods here
    #
    #
    def get_all_states_and_transition_probabilities(self) -> List[State]:
        """
        Returns list of all possible states
        :return:
        """
        states = set()
        initial_state = self.environment.get_init_state()

        fringe = {initial_state}

        while fringe:

            current = fringe.pop()

            states.add(current)

            for action in ROBOT_ACTIONS:

                normal_reward, next_state = self.environment.apply_dynamics(current, action)

                _, cw_spin = self.environment.apply_dynamics(current, SPIN_RIGHT)

                _, ccw_spin = self.environment.apply_dynamics(current, SPIN_LEFT)

                double_move_reward, double_move = self.environment.apply_dynamics(next_state, action)

                cw_reward, move_after_cw_spin = self.environment.apply_dynamics(cw_spin, action)

                ccw_reward, move_after_ccw_spin = self.environment.apply_dynamics(ccw_spin, action)

                double_move_cw_reward, double_move_after_cw_spin = self.environment.apply_dynamics(move_after_cw_spin, action)

                double_move_ccw_reward, double_move_after_ccw_spin = self.environment.apply_dynamics(move_after_ccw_spin, action)

                DRIFT_CW_PROB = self.environment.drift_cw_probs[action]
                DRIFT_CCW_PROB = self.environment.drift_ccw_probs[action]
                DOUBLE_MOVE_PROB = self.environment.double_move_probs[action]
                DRIFT_CW_DOUBLE_MOVE_PROB = DRIFT_CW_PROB * DOUBLE_MOVE_PROB
                DRIFT_CCW_DOUBLE_MOVE_PROB = DRIFT_CCW_PROB * DOUBLE_MOVE_PROB
                NORMAL_MOVE_PROB = (1 - (DRIFT_CW_PROB + DRIFT_CCW_PROB)) * (1 - DOUBLE_MOVE_PROB)

                self.transitions[current][action][move_after_cw_spin] = ProbAndReward(DRIFT_CW_PROB, cw_reward)
                self.transitions[current][action][move_after_ccw_spin] = ProbAndReward(DRIFT_CCW_PROB, ccw_reward)
                self.transitions[current][action][double_move] = ProbAndReward(DOUBLE_MOVE_PROB, double_move_reward)
                self.transitions[current][action][double_move_after_cw_spin] = ProbAndReward(DRIFT_CW_DOUBLE_MOVE_PROB, double_move_cw_reward)
                self.transitions[current][action][double_move_after_ccw_spin] = ProbAndReward(DRIFT_CCW_DOUBLE_MOVE_PROB, double_move_ccw_reward)
                self.transitions[current][action][next_state] = ProbAndReward(NORMAL_MOVE_PROB, normal_reward)

                if next_state not in states:
                    fringe.add(next_state)
                if move_after_cw_spin not in states:
                    fringe.add(move_after_cw_spin)
                if move_after_ccw_spin not in states:
                    fringe.add(move_after_ccw_spin)
                if double_move not in states:
                    fringe.add(double_move)
                if double_move_after_cw_spin not in states:
                    fringe.add(double_move_after_cw_spin)
                if double_move_after_ccw_spin not in states:
                    fringe.add(double_move_after_ccw_spin)

        self.possible_states = list(states)

        return self.possible_states
