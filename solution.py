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
        self.state_value: Dict[State, float] = None
        self.new_state_value: Dict[State, float] = None
        self.possible_states = self.get_all_states()
        self.terminal_states = self.get_terminal_states()
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
        self.policy = defaultdict(lambda: FORWARD)
        self.state_value = defaultdict(float)
        self.new_state_value = defaultdict(lambda: math.inf)

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
        return max(self.new_state_value[s] - self.state_value[s] for s in self.new_state_value.keys()) <= 0.001

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
        self.pi_evaluate()
        self.pi_improvise()

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
        return self.policy[state]

    # === Helper Methods ===============================================================================================
    #
    #
    # TODO: Add any additional methods here
    #
    #
    def pi_compute_state_values(self):
        pass

    def pi_evaluate(self, max_iter=1000):
        pass

    def pi_improvise(self):
        pass

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
                    fringe.add(next_state)

        return list(states)

    def get_terminal_states(self) -> List[State]:
        return [state for state in self.possible_states if self.environment.is_solved(state)]
