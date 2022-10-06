import math
import sys
import time
from collections import defaultdict
from typing import Dict, List

import numpy as np

from constants import *
from environment import *
from state import State

"""
solution.py

This file is a template you should use to implement your solution.

You should implement each section below which contains a TODO comment.

Last updated by njc 08/09/22
"""


class Solver:

    def __init__(self, environment: Environment):
        self.environment = environment
        #
        # TODO: Define any class instance variables you require (e.g. dictionary mapping state to VI value) here.
        #
        self.policy: Dict[State, int] = None
        self.new_policy = None
        self.state_value: Dict[State, float] = None
        self.new_state_value: Dict[State, float] = None
        self.state_transition_probability = None
        self.state_rewards = None
        self.possible_states = self.get_all_states()
        self.terminal_states = self.get_terminal_states()
        # exit()

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
        pass

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
        pass

    def vi_iteration(self):
        """
        Perform a single iteration of Value Iteration (i.e. loop over the state space once).
        """
        #
        # TODO: Implement code to perform a single iteration of Value Iteration here.
        #
        # In order to ensure compatibility with tester, you should avoid adding additional arguments to this function.
        #
        pass

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
        pass

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
        pass

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
        # probability = 1 / len(ROBOT_ACTIONS)
        # self.move_probability_map = defaultdict(lambda: {move: probability for move in ROBOT_ACTIONS})
        self.policy = defaultdict(lambda: FORWARD)
        self.new_policy = defaultdict(lambda: np.random.choice(ROBOT_ACTIONS))
        self.state_value = defaultdict(float)
        for state in self.terminal_states:
            self.state_value[state] = 10000
        self.new_state_value = defaultdict(lambda: math.inf)
        self.calculate_state_transition_probabilities()
        # self.possible_states.sort(key=lambda state: self.state_value[state], reverse=True)
        # for state in self.possible_states:
        #     self.environment.render(state)
        # exit(0)

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
        return self.new_policy == self.policy if len(self.policy) else False

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
        self.policy = self.new_policy
        self.pi_evaluate()
        self.pi_improvise()

    def pi_plan_offline(self):
        """
        Plan using Policy Iteration.
        """
        # !!! In order to ensure compatibility with tester, you should not modify this method !!!
        self.pi_initialise()
        iter = 0
        while not self.pi_is_converged():
            self.pi_iteration()
            iter += 1
        print(f'Iter: {iter}')

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
        # if state not in self.terminal_states:
        #     move_tuple = [(move, probability) for move, probability in self.state_transition_probability[state].items()]
        #     best_move, probability = max(move_tuple, key=lambda x: x[1])
        #     # max_value = -math.inf
        #     # best_move = None
        #     # for action in ROBOT_ACTIONS:
        #     #     reward, next_state = self.environment.apply_dynamics(state, action)
        #     #     value = reward + (self.environment.gamma * self.state_value[next_state])
        #     #     if value > max_value:
        #     #         max_value = value
        #     #         best_move = action
        #     return best_move
        # return None
        return self.policy[state]

    # === Helper Methods ===============================================================================================
    #
    #
    # TODO: Add any additional methods here
    #
    #
    def pi_compute_state_value(self, state: State):
        if state not in self.terminal_states:
            # values = list()
            value = 0.0
            for action in ROBOT_ACTIONS:
                for possible_next_state in self.state_transition_probability[state][action]:
                    # reward, next_state = self.environment.apply_dynamics(state, action)
                    value += self.state_rewards.get(possible_next_state, -1) + \
                             (self.environment.gamma *
                              self.state_value[possible_next_state] *
                              self.state_transition_probability[state][action][possible_next_state])

                # values.append(value)
            # return max(values)
            return value
        return self.state_value[state]

    def pi_evaluate(self, max_iter=1000):
        # for state in self.possible_states:
        #     self.state_value[state] = self.pi_compute_state_value(state)
        for _ in range(max_iter):
            for state in self.possible_states:
                self.new_state_value[state] = self.pi_compute_state_value(state)
            if self.pi_is_converged():
                break

    def pi_improvise(self):
        for state in self.possible_states:
            if state not in self.terminal_states:
                self.new_policy[state] = self.pi_select_best_move_from_state_values(state)

    def pi_select_best_move_from_state_values(self, state):
        formula = lambda s, action: max(self.state_transition_probability[s][action][next_state] *
                                        (self.state_rewards[next_state] +
                                         (self.environment.gamma * self.state_value[next_state]))
                                        for next_state in self.possible_states)
        return max(ROBOT_ACTIONS, key=lambda x: formula(state, x))

    def get_all_states(self) -> List[State]:
        """
        returns list of all possible states in the environment
        :return:
        """
        states = set()
        initial = self.environment.get_init_state()
        fringe = {initial}

        while fringe:

            current = fringe.pop()
            states.add(current)

            for action in ROBOT_ACTIONS:
                reward, next_state = self.environment.apply_dynamics(current, action)

                if next_state not in states:
                    states.add(next_state)
                    self.state_rewards[next_state] = reward
                    fringe.add(next_state)

        # for state in states:
        #     self.environment.render(state)
        return list(states)

    def get_terminal_states(self) -> List[State]:
        return [state for state in self.possible_states if self.environment.is_solved(state)]

    def calculate_state_transition_probabilities(self):
        for state in self.possible_states:
            self.state_transition_probability[state] = defaultdict(lambda: 0.0)
            for action in ROBOT_ACTIONS:
                total_probability = 1.0
                probability_double_move = self.environment.double_move_probs[action]
                probability_cw = self.environment.drift_cw_probs[action]
                probability_ccw = self.environment.drift_ccw_probs[action]
                probability_cw_and_double = probability_double_move * probability_cw
                probability_ccw_and_double = probability_double_move * probability_ccw
                probability_double_move -= (probability_ccw_and_double + probability_cw_and_double)
                probability_cw -= probability_cw_and_double
                probability_ccw -= probability_ccw_and_double
                probability_correct_move = total_probability - (probability_cw +
                                                                probability_ccw +
                                                                probability_cw_and_double +
                                                                probability_ccw_and_double +
                                                                probability_double_move)
                _, correct_state = self.environment.apply_dynamics(state, action)

                # first drift right then apply requested action
                _, drift_cw = self.environment.apply_dynamics(self.environment.apply_dynamics(state, SPIN_RIGHT)[1],
                                                              action)

                # first drift left then apply requested action
                _, drift_ccw = self.environment.apply_dynamics(self.environment.apply_dynamics(state, SPIN_LEFT)[1],
                                                               action)

                # apply action twice
                _, double_move = self.environment.apply_dynamics(self.environment.apply_dynamics(state, action)[1],
                                                                 action)

                # first drift cw and then apply action twice
                _, cw_and_double = self.environment.apply_dynamics(
                    self.environment.apply_dynamics(
                        self.environment.apply_dynamics(state, SPIN_RIGHT)[1], action)[1],
                    action)

                _, ccw_and_double = self.environment.apply_dynamics(
                    self.environment.apply_dynamics(
                        self.environment.apply_dynamics(state, SPIN_LEFT)[1], action)[1],
                    action)

                self.state_transition_probability[state][action][correct_state] = probability_correct_move
                self.state_transition_probability[state][action][drift_cw] = probability_cw
                self.state_transition_probability[state][action][drift_ccw] = probability_ccw
                self.state_transition_probability[state][action][double_move] = probability_double_move
                self.state_transition_probability[state][action][cw_and_double] = probability_cw_and_double
                self.state_transition_probability[state][action][ccw_and_double] = probability_ccw_and_double
