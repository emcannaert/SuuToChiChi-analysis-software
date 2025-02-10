import json
import matplotlib.pyplot as plt

# Load the JSON file
with open('POG/LUM/2016preVFP_UL/pileup_weights.json', 'r') as f:
    data = json.load(f)

# Extract the relevant data (nominal and up weights)
nominal_weights = data['corrections'][0]['data']['content'][0]['value']['content']
#up_weights = data['corrections'][0]['data']['content'][1]['value']['content']

# The bin edges for the number of true interactions
bin_edges = data['corrections'][0]['data']['content'][0]['value']['edges']

# Plot the nominal and up weights
plt.figure(figsize=(10, 6))
plt.step(bin_edges[:-1], nominal_weights, label='Nominal', where='post', color='b', linestyle='-', linewidth=2)
#plt.step(bin_edges[:-1], up_weights, label='Up', where='post', color='r', linestyle='--', linewidth=2)

# Customize the plot
plt.xlabel('Number of True Interactions')
plt.ylabel('Pileup Weight')
plt.title('Pileup Weight Distribution (Nominal and Up Variations)')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()