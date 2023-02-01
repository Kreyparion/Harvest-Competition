# ENV
from env.environnement import Env
# AGENT
from agents.agent import Agent
from implemented_agents import agents_map
# PYTHON
from argparse import ArgumentParser


N_EPISODES = 100

def train(agent : Agent, env : Env, display = False, save_best = False):

    best_score = 0
    for episode in range(N_EPISODES):
        print(f"Episode {episode} starts.")

        state = env.reset()
        done = False
        while not done:
            # Agent takes action
            action = agent.act(state, training = True)

            # Action has effect on environment
            next_state, reward, done = env.step(action)

            # Agent observe the transition and possibly learns
            agent.observe(state, action, reward, next_state, done)
            agent.learn()

            # Render environment for user to see
            env.render()

            # Update state
            state = next_state

        print(f"Score : {env.score}")

        if env.score > best_score:
            best_score = env.score
            if save_best:
                env.save_solution()

        if display:
            env.final_render()
        
        
        



if __name__ == "__main__":
    
    # Get args
    parser = ArgumentParser(description="Run a reinforcement learning agent")
    parser.add_argument("--agent", type=str, required=True, help="Agent to run")
    args = parser.parse_args()
    agent_name = args.agent

    # Create the environnement
    seed = 42
    env = Env(seed)
    # Create the agent
    agent = agents_map[agent_name](env)
    # Run the agent
    train(agent, env)