from itertools import product, permutations
from functools import reduce
from random import sample, shuffle, choice



rank_to_numeric_value = {
    'A': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    'J': 8,
    'Q': 9, 
    'K': 10
}

suit_full_to_short_name = {
    'diamonds': 'd',
    'hearts': 'h',
    'spades': 's',
    'clubs': 'c'
}

def card_rank_check(rank):
    return type(rank) == str and rank in rank_to_numeric_value.keys()

def card_suit_check(suit):
    return type(suit) == str and suit in suit_full_to_short_name.keys()



class Card:
    # Initialization: a 'Card' object is defined by two elements - its suit and rank.
    def __init__(self, rank, suit):
        # both the suit and the rank values need to bare particular characteristics in order to be considered as valid
        assert card_rank_check(rank), "got a card of non-integer rank or of a rank outside of scopa's range"
        assert card_suit_check(suit), "got a card of non-string suit"
        self.rank = rank
        self.suit = suit

    # String representation of a 'Card' object upon 'print()' statements
    def __str__(self):
        return f"{self.rank} of {self.suit}"

    # A card is assigned a 'value' based on the rank it bares
    def card_value(self):
        return rank_to_numeric_value[self.rank]
    
    # Every single card of a single deck bares a unique identifier
    def key(self):
        return self.rank + suit_full_to_short_name[self.suit]

    # The following 2 methods are used in order to make sure that python can quickly and efficiently make card comparisons 
    # based on a unique id of theirs, defined by their rank and suit (we can find each rank-suit combo only once in a deck, and
    # Scopa is a single-deck game)
    # Equality comparison method
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank == other.rank and self.suit == other.suit
        return False
    # Hashing methods to ensure that cards can be used in sets/dictionaries
    def __hash__(self):
        return hash((self.rank, self.suit))


        

class Deck:
    def __init__(self):
        self.cards = list(Card(el[0], el[1]) for el in product(rank_to_numeric_value.keys(), suit_full_to_short_name.keys(), repeat=1))
        
    def card_removal(self, cards_removed):
        for card in cards_removed:
            self.cards.remove(card)

    def deal_hand(self, cards_no):  
        assert cards_no in [3,4], "invalid number of cards for a player hand or the board"
        cards = sample(self.cards, cards_no)
        self.card_removal(cards)
        return Hand(cards)

    def remaining_card_no(self):
        return len(self.cards)
    def empty_deck(self):
        return self.remaining_card_no() == 0

    def __str__(self):
        return f"Deck with {self.remaining_card_no()} cards remaining"



class Hand:
    def __init__(self, cards):
        self.cards = cards

    def play_card(self, card):
        self.cards.remove(card)

    def add_card_to_board(self, card):
        self.cards.append(card)

    def hand_cards_no(self):
        return len(self.cards)


        

class PlayerPile:
    def __init__(self):
        self.cards = []
        self.scopas = 0

    def add_cards_to_pile(self, cards):
        self.cards += cards

    def pile_count(self):
        return len(self.cards)

    def sette_bello(self):
        return Card('7', 'diamonds') in self.cards

    def scopas_score(self):
        self.scopas += 1
    
    def highest_primiera(self):
        primiera_values = {7: 21, 6: 18, 5: 16, 4: 14, 3: 13, 2: 12, 1: 11, 8: 10, 9: 10, 10: 10}
        suits = {'Coins': 0, 'Cups': 0, 'Swords': 0, 'Clubs': 0}

        for card in self.cards:
            if card.rank in primiera_values:
                suits[card.suit] = max(suits[card.suit], primiera_values[card.rank])

        return sum(suits.values())



class Player:
    def __init__(self, idvalue):
        assert type(idvalue) == int, "invalid - non integer player id value attempted"
        self.idvalue = idvalue

    def __str__(self):
        return f"Player {self.idvalue} has a current score of {self.score}."



class PlayerAction:
    def __init__(self, player_id_value, hand, board, opponent_hand):
        self.player_id_value = player_id_value
        self.hand = hand
        self.board = board
        self.opponent_hand = opponent_hand


    def available_actions(self):
        actions = []

        if not self.opponent_hand.cards:
            actions.append('collect_pile')
            return actions

        # Check for capture opportunities
        for card in self.hand.cards:
            try: 
                board_length = self.board.hand_cards_no()
            except:
                board_length = 0

            for r in range(1, board_length + 1):
                for combo in permutations(self.board.cards, r):
                    if sum(c.card_value() for c in combo) == card.card_value():
                        actions.append((card, list(combo)))

        # If no capture options, discard is the fallback action
        if not actions:
            actions.append('discard')

        return actions

            




def calculate_primiera(pile):
    primiera_values = {
        '7': 21, '6': 18, 'A': 16, '5': 15, '4': 14, '3': 13, '2': 12,
        'K': 10, 'J': 10, 'Q': 10
    }
    suits = {'clubs': 0, 'diamonds': 0, 'hearts': 0, 'spades': 0}

    for card in pile.cards:
        if card.rank in primiera_values:
            suits[card.suit] = max(suits[card.suit], primiera_values[card.rank])

    primiera_sum = sum(suits.values())
    suits_covered = sum(1 for value in suits.values() if value > 0)

    return primiera_sum, suits_covered



def game():
    deck = Deck()
    player_1 = Player(idvalue=1)
    player_2 = Player(idvalue=2)

    player_1_pile = PlayerPile()
    player_2_pile = PlayerPile()
    board = deck.deal_hand(4)

    player_1_hand = deck.deal_hand(3)
    player_2_hand = deck.deal_hand(3)

    current_player = 1

    while not deck.empty_deck() or player_1_hand.hand_cards_no() > 0 or player_2_hand.hand_cards_no() > 0:
        if player_1_hand.hand_cards_no() == 0 and player_2_hand.hand_cards_no() == 0 and not deck.empty_deck():
            player_1_hand = deck.deal_hand(3)
            player_2_hand = deck.deal_hand(3)

        if current_player == 1:
            actions = PlayerAction(current_player, player_1_hand, board, player_2_hand).available_actions()
            action = choice(actions)

            if action == 'discard':
                card = choice(player_1_hand.cards)
                player_1_hand.play_card(card)
                board.add_card_to_board(card)
            elif action == 'collect_pile':
                card = choice(player_1_hand.cards)
                player_1_hand.play_card(card)
                player_1_pile.add_cards_to_pile(board.cards)
                board = Hand([])
            else:
                card, captured_cards = action
                player_1_hand.play_card(card)
                if len(board.cards) == len(captured_cards):  # Scopa condition
                    player_1_pile.scopas_score()

                board = Hand([c for c in board.cards if c not in captured_cards])
                player_1_pile.add_cards_to_pile([card] + captured_cards)
        else:
            actions = PlayerAction(current_player, player_2_hand, board, player_1_hand).available_actions()
            action = choice(actions)

            if action == 'discard':
                card = choice(player_2_hand.cards)
                player_2_hand.play_card(card)
                board.add_card_to_board(card)
            elif action == 'collect_pile':
                card = choice(player_2_hand.cards)
                player_2_hand.play_card(card)
                player_2_pile.add_cards_to_pile(board.cards)
                board = Hand([])
            else:
                card, captured_cards = action
                player_2_hand.play_card(card)
                if len(board.cards) == len(captured_cards):  # Scopa condition
                    player_2_pile.scopas_score()
                board = Hand([c for c in board.cards if c not in captured_cards])
                player_2_pile.add_cards_to_pile([card] + captured_cards)

        current_player = 2 if current_player == 1 else 1

    ### Primiera concerns
    player_1_primiera, player_1_suits = calculate_primiera(player_1_pile)
    player_2_primiera, player_2_suits = calculate_primiera(player_2_pile)

    def primiera_score(p1_suits, p2_suits, p1_value, p2_value):
        if p1_suits == 4 and p2_suits < 4:
            return 1, 0
        elif p2_suits == 4 and p1_suits < 4:
            return 0, 1
        elif p1_suits > p2_suits:
            return 1, 0
        elif p2_suits > p1_suits:
            return 0, 1
        else:  # both have the same number of suits
            if p1_value > p2_value:
                return 1, 0
            elif p2_value > p1_value:
                return 0, 1
            else:
                return 0, 0  # tie

    p1_primiera_score, p2_primiera_score = primiera_score(player_1_suits, player_2_suits, player_1_primiera, player_2_primiera)


    player_1_score = sum([
        len(player_1_pile.cards) > len(player_2_pile.cards),
        any(card.rank == '7' and card.suit == 'diamonds' for card in player_1_pile.cards),
        len([card for card in player_1_pile.cards if card.suit == 'diamonds']) > len([card for card in player_2_pile.cards if card.suit == 'diamonds']),
        p1_primiera_score > p2_primiera_score
    ]) + player_1_pile.scopas

    player_2_score = sum([
        len(player_2_pile.cards) > len(player_1_pile.cards),
        any(card.rank == '7' and card.suit == 'diamonds' for card in player_2_pile.cards),
        len([card for card in player_2_pile.cards if card.suit == 'diamonds']) > len([card for card in player_1_pile.cards if card.suit == 'diamonds']),
        p2_primiera_score > p1_primiera_score
    ]) + player_2_pile.scopas

    print('Player 1 got', player_1_score, 'points.\n')

    print('Player 1 point breakdown:\n')
    print('Points from Scopas Scored:', player_1_pile.scopas)
    print('Has more pile cards in total:', len(player_1_pile.cards) > len(player_2_pile.cards))
    print('Got the Sette Bello:', any(card.rank == '7' and card.suit == 'diamonds' for card in player_1_pile.cards))
    print('Higher primiera score:', p1_primiera_score > p2_primiera_score)
    print('More diamonds in their pile:', len([card for card in player_1_pile.cards if card.suit == 'diamonds']) > len([card for card in player_2_pile.cards if card.suit == 'diamonds']))
    print('\n\n')

    print('Player 2 got', player_2_score, 'points.\n')

    print('Player 2 point breakdown:\n')
    print('Points from Scopas Scored:', player_2_pile.scopas)
    print('Has more pile cards in total:', len(player_2_pile.cards) > len(player_1_pile.cards))
    print('Got the Sette Bello:', any(card.rank == '7' and card.suit == 'diamonds' for card in player_2_pile.cards))
    print('Higher primiera score:', p2_primiera_score > p1_primiera_score)
    print('More diamonds in their pile:', len([card for card in player_2_pile.cards if card.suit == 'diamonds']) > len([card for card in player_1_pile.cards if card.suit == 'diamonds']))
    print('\n\n')


    if player_1_score > player_2_score:
        print('Player 1 wins!')
    elif player_1_score < player_2_score:
        print('Player 2 wins!')
    else:
        print('Tie!')



if __name__ == "__main__":
    game()



