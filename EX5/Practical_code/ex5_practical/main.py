import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the states and rewards
states = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']
rewards = {
    's1': -0.05, 's2': -0.05, 's3': -0.05,
    's4': -0.05, 's5': -10, 's6': -0.05,
    's7': 15, 's8': -0.05, 's9': 30
}
absorbing_states = {'s5', 's7', 's9'}

# Define the discount factor
gamma = 0.99

# Initialize value function
V = {s: 0 for s in states}
V_history = []
policy_history = []

# Define the actions and state transitions
actions = ['Left', 'Right', 'Up', 'Down']
transitions = {
    's1': {'Left': 's1', 'Right': 's2', 'Down': 's1', 'Up': 's4'},
    's2': {'Left': 's1', 'Right': 's3', 'Down': 's2', 'Up': 's5'},
    's3': {'Left': 's2', 'Right': 's3', 'Down': 's3', 'Up': 's6'},
    's4': {'Left': 's4', 'Right': 's5', 'Down': 's1', 'Up': 's7'},
    's5': {'Left': 's5', 'Right': 's5', 'Down': 's2', 'Up': 's8'},
    's6': {'Left': 's5', 'Right': 's6', 'Down': 's3', 'Up': 's9'},
    's7': {'Left': 's7', 'Right': 's8', 'Down': 's4', 'Up': 's7'},
    's8': {'Left': 's7', 'Right': 's9', 'Down': 's5', 'Up': 's8'},
    's9': {'Left': 's8', 'Right': 's9', 'Down': 's6', 'Up': 's9'},
}


# Define the actions and the given policy
given_policy = {
    's1': 'Up', 's2': 'Right', 's3': 'Up',
    's4': 'Up', 's5': 'Left', 's6': 'Up',
    's7': 'Left', 's8': 'Left', 's9': 'Left'
}


# Define the probabilities for stochastic transitions
prob_success = 0.9
prob_failure = 0.1 / 3  # Three adjacent cells

# Initialize value function for stochastic case with given policy
V_given_policy = {s: 0 for s in states}

# Perform value iteration for the given policy in stochastic MDP
for iteration in range(10):
    V_new = V_given_policy.copy()
    for s in states:
        if s in absorbing_states:
            V_new[s] = rewards[s]
        else:
            a = given_policy[s]
            next_state = transitions[s][a]
            adj_states = [transitions[s][adj_a] for adj_a in actions if transitions[s][adj_a] != next_state]
            V_new[s] = (
                prob_success * (rewards[s] + gamma * V_given_policy[next_state]) +
                prob_failure * sum(rewards[s] + gamma * V_given_policy[adj_s] for adj_s in adj_states)
            )
    V_given_policy = V_new

# Convert to DataFrame for comparison
given_policy_value_df = pd.DataFrame([V_given_policy], columns=states)

# Print the DataFrame
print(given_policy_value_df)

# Save the result table as an image
fig, ax = plt.subplots(figsize=(12, 6))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)
result_table = pd.plotting.table(ax, given_policy_value_df.round(3), loc='center', cellLoc='center', colWidths=[0.1]*len(given_policy_value_df.columns))
result_table.auto_set_font_size(False)
result_table.set_fontsize(10)
result_table.scale(1.2, 1.2)
plt.savefig('given_policy_result_table_adjusted.png', bbox_inches='tight')

# Return the DataFrame and image path
given_policy_value_df, 'given_policy_result_table_adjusted.png'