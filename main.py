# Import the necessary module
import re

# Raw UTG range string
utg_range ='77,66,55,44,33,22,ATo:0.25,A9o,A8o,A7,A6,A5s:0.5,A5o,A4s:0.5,A4o,A3s:0.5,A3o,A2s:0.5,A2o,KJo:0.25,KTo:0.75,K9o,K8,K7,K6,K5,K4,K3,K2,QJo:0.5,QTo,Q9o,Q8,Q7,Q6,Q5,Q4,Q3,Q2,JTo:0.75,J9o,J8o,J7,J6,J5,J4,J3,J2,T9o,T8o,T7s:0.55,T7o,T6,T5,T4,T3,T2,98o,97o,96s:0.55,96o,95,94,93,92,87o,86s:0.25,86o,85s:0.55,85o,84,83,82,76s:0.25,76o,75s:0.25,75o,74s:0.55,74o,73,72,65s:0.25,65o,64s:0.5,64o,63s:0.55,63o,62,54s:0.25,54o,53s:0.5,53o,52s:0.55,52o,43s:0.5,43o,42s:0.55,42o,32s:0.55,32o'

# Parses the utg range string into a dict where keys are the cards and values are the probabilities
def parse_utg_range(range_str):
    range_dict = {}
    components = range_str.split(',')
    for component in components:
        if ':' in component:
            card, prob = component.split(':')
            range_dict[card] = float(prob)
        else:
            range_dict[component] = 1.0
    return range_dict

# Calculates the conditional probabilities conditioned on UTG folding 
def calculate_conditional_probabilities(range_dict):
    conditional_probabilities = {}

    # Go through all the cards
    for card in range_dict:
        # The conditional probability is 1 - the probability that UTG plays the card
        conditional_probabilities[card] = 1 - range_dict[card]

    return conditional_probabilities

# Parse the UTG range
utg_range_dict = parse_utg_range(utg_range)

# Calculate the conditional probabilities
conditional_probabilities = calculate_conditional_probabilities(utg_range_dict)

# Print the results
for card, prob in conditional_probabilities.items():
    print(f'Card: {card}, Conditional Probability: {prob}')
