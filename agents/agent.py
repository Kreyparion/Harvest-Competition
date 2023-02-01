from env.utils import Action, State
from env.environnement import Env
from abc import ABC, abstractmethod




class Agent(ABC):
    """
    Base class for all of our model-based agents. 
    An agent is an object that can interact with an environment and learn from it.
    """
    def __init__(self, env : Env, **kwargs):
        self.env = env

    @abstractmethod
    def act(self, state, training = True) -> Action:
        """Return the action to take in the given state"""
        pass

    @abstractmethod
    def observe(self, state, action, reward, next_state, done):
        """Observe the transition and stock in memory"""
        pass

    @abstractmethod
    def learn(self):
        """Learn using the memory"""
        pass    
