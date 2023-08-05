def convert_to_similar_flop(flop):

   RANKS = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
   SUITS = ['spade', 'diamond', 'club']

   sorted_flop = sorted(flop, key=lambda x: RANKS[x[0]], reverse=True)

   flop_suits = [s for r,s in sorted_flop]
   suit_counts = {suit:flop_suits.count(suit) for suit in flop_suits}

   # Assign new suits to the sorted flop
   new_flop = [(rank, 'spade') if i < suit_counts[flop_suits[0]] 
               else (rank, 'diamond') if i < (suit_counts[flop_suits[0]] + suit_counts.get(flop_suits[1], 0)) 
               else (rank, 'club') 
               for i, (rank, suit) in enumerate(sorted_flop)]

   return new_flop
flop_rainbow = [('K', 'heart'), ('10', 'diamond'), ('2', 'club')]
print(convert_to_similar_flop(flop_rainbow))  # [('K', 'spade'), ('10', 'diamond'), ('2', 'club')]

flop_twotone = [('K', 'heart'), ('10', 'heart'), ('2', 'club')]
print(convert_to_similar_flop(flop_twotone))  # [('K', 'spade'), ('10', 'spade'), ('2', 'diamond')]

flop_monotone = [('K', 'heart'), ('10', 'heart'), ('2', 'heart')]
print(convert_to_similar_flop(flop_monotone))  # [('K', 'spade'), ('10', 'spade'), ('2', 'spade')]
