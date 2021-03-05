# CardEvaluator
### Introduction

The project is used to calculate the winning probability of each stage of Texas Hold'em.  

Two algorithms are adopted according to different round in Texas Hold'em. In the preflop, we use the cache matrix which relies on [PokerStove](https://github.com/andrewprock/pokerstove) to calcuate the winning probability directly. In the flop, turn and river, we enumerate the remaining public cards and calculate the winning probability based on the card strength. 

The input is hand, board and opponent range( i.e. the distribution of opponent hand). If the opponent range is not specified, we will generate normal distribution after removing the card conflicts. The output is the winning probability under such circumstances.

All results will be produced in up to 0.5 s.

### Setup

Decompress compressed package to get the cache matrix.

```bash
unzip data.zip
```



### Card Encoding

For each card, a string is used for storage, which is composed of suit and rank of the card. 

* rank: 2, 3, 4, 5, 6,7, 8, 9, T, J, Q, K, A
* suit: c(club), d(diamond), s(spade), h(heart),
* e.g:  'Ts'  represents 'Spade 10'.  'Jc' represents 'club J,  '4d' represents 'diamond4'

### Example

```python
lookup = Lookup()

hand = ['Kc', 'Jh']
board = ['5c', '4c', 'Ac', '6c', 'Qc']
print(lookup.calc(hand, board))   // 0.996
    
start = time.time()
hand = ['Kc', 'Jh']
board = ['5c', '4c', 'Ac', '6c']
print(lookup.calc(hand, board))    // 0.984
    
start = time.time()
hand = ['Kc', 'Jh']
board = ['5c', '4c', 'Ac']
print(lookup.calc(hand, board))    // 0.641

hand = ['Kc', 'Jh']
board = []
print(lookup.calc(hand, board))    // 0.605
```

