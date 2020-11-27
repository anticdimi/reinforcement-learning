import util, random
import numpy as np
from copy import deepcopy

class Agent:

  def getAction(self, state):
    """
    For the given state, get the agent's chosen
    action.  The agent knows the legal actions
    """
    abstract

  def getValue(self, state):
    """
    Get the value of the state.
    """
    abstract

  def getQValue(self, state, action):
    """
    Get the q-value of the state action pair.
    """
    abstract

  def getPolicy(self, state):
    """
    Get the policy recommendation for the state.

    May or may not be the same as "getAction".
    """
    abstract

  def update(self, state, action, nextState, reward):
    """
    Update the internal state of a learning agent
    according to the (state, action, nextState)
    transistion and the given reward.
    """
    abstract


class RandomAgent(Agent):
  """
  Clueless random agent, used only for testing.
  """

  def __init__(self, actionFunction):
    self.actionFunction = actionFunction

  def getAction(self, state):
    return random.choice(self.actionFunction(state))

  def getValue(self, state):
    return 0.0

  def getQValue(self, state, action):
    return 0.0

  def getPolicy(self, state):
    return 'random'

  def update(self, state, action, nextState, reward):
    pass


################################################################################
# Exercise 7

class ValueIterationAgent(Agent):

  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
    Your value iteration agent should take an mdp on
    construction, run the indicated number of iterations
    and then act according to the resulting policy.
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations

    # TODO: init randomly
    states = self.mdp.getStates()
    self.values = {s: 0.0 for s in states}
    self.new_values = {s: 0.0 for s in states}

    flag = True

    for i in range(self.iterations):
        if self.values[self.mdp.getStartState()] > 0 and flag:
            print('First iter in which value of start state is != 0: ', i)
            flag = False

        for s in states:
            if self.mdp.isTerminal(s):
                continue

            possible_actions = self.mdp.getPossibleActions(s)
            results_to_maximize_over = []
            for a in possible_actions:
                rew = self.mdp.getReward(s, a, None)
                transition_states_probs = self.mdp.getTransitionStatesAndProbs(s, a)

                total_sum = rew
                for next_state, prob in transition_states_probs:
                    total_sum += prob * self.values[next_state]
                total_sum *= discount

                results_to_maximize_over.append(total_sum)

            self.new_values[s] = np.max(results_to_maximize_over)

        self.values = deepcopy(self.new_values)


    self.q = {(s, a): 0 for s in states for a in self.mdp.getPossibleActions(s)}

    for s, a in self.q:
        rew = self.mdp.getReward(s, a, None)
        transition_states_probs = self.mdp.getTransitionStatesAndProbs(s, a)

        total_sum = rew
        for next_state, prob in transition_states_probs:
            total_sum += prob * self.values[next_state]
        total_sum *= discount

        self.q[(s, a)] = total_sum

  def getValue(self, state):
    """
    Look up the value of the state (after the indicated
    number of value iteration passes).
    """
    return self.values[state]



  def getQValue(self, state, action):
    """
    Look up the q-value of the state action pair
    (after the indicated number of value iteration
    passes).
    """

    return self.q[(state, action)]



  def getPolicy(self, state):
    """
    Look up the policy's recommendation for the state
    (after the indicated number of value iteration passes).
    """
    if self.mdp.isTerminal(state):
        return None

    actions = self.mdp.getPossibleActions(state)
    values_to_maximize_over = [self.q[(state, a)] for a in actions]
    return actions[np.argmax(values_to_maximize_over)]



  def getAction(self, state):
    """
    Return the action recommended by the policy.
    """
    return self.getPolicy(state)


  def update(self, state, action, nextState, reward):
    """
    Not used for value iteration agents!
    """
    pass


################################################################################

class QLearningAgent(Agent):

  def __init__(self, actionFunction, discount = 0.9, learningRate = 0.1, epsilon = 0.2):
    """
    A Q-Learning agent gets nothing about the mdp on
    construction other than a function mapping states to actions.
    The other parameters govern its exploration
    strategy and learning rate.
    """
    self.setLearningRate(learningRate)
    self.setEpsilon(epsilon)
    self.setDiscount(discount)
    self.actionFunction = actionFunction

    raise "Your code here."

  # THESE NEXT METHODS ARE NEEDED TO WIRE YOUR AGENT UP TO THE CRAWLER GUI

  def setLearningRate(self, learningRate):
    self.learningRate = learningRate

  def setEpsilon(self, epsilon):
    self.epsilon = epsilon

  def setDiscount(self, discount):
    self.discount = discount

  # GENERAL RL AGENT METHODS

  def getValue(self, state):
    """
    Look up the current value of the state.
    """

    raise ValueError("Your code here.")

  def getQValue(self, state, action):
    """
    Look up the current q-value of the state action pair.
    """

    raise ValueError("Your code here.")

  def getPolicy(self, state):
    """
    Look up the current recommendation for the state.
    """

    raise ValueError("Your code here.")

  def getAction(self, state):
    """
    Choose an action: this will require that your agent balance
    exploration and exploitation as appropriate.
    """

    raise ValueError("Your code here.")

  def update(self, state, action, nextState, reward):
    """
    Update parameters in response to the observed transition.
    """

    raise ValueError("Your code here.")