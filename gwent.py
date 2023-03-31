from enum import Enum


class Card:
    def __init__(self, name, strength, kind):
        self.name = name
        self.strength = strength
        self.kind = kind

    def show_card(self):
        print(f'Name: {self.name} Strength: {self.strength} Kind: {self.kind.value}')


class Kind(Enum):
    MELEE = 'Melee'
    RANGED = 'Ranged'
    SIEGE = 'Siege'


class Faction(Enum):
    NILFGAARD = 'Nilfgaard'
    NORTHERN_REALMS = 'Northern Realms'
    NOVIGRAD = 'Novigrad'


class Deck:
    def __init__(self, cards, faction):
        self.cards = cards
        self.faction = faction

    def play_card(self, card):
        self.cards.remove(card)
        return card

    def print_deck(self):
        print(f'Faction: {self.faction.value}')
        for card in self.cards:
            card.show_card()


class Player:
    def __init__(self, name, _deck, hp):
        self.name = name
        self.deck = _deck
        self.hp = hp
        self.board = Board()
        self.not_terminated = True
        self.turn_active = True

    def play_card(self, card):
        self.deck.play_card(card)
        self.board.add_card(card)

    def play_cards(self):
        print(f'Current player: {self.name} with {self.deck.faction.value} HP({self.hp})\n\nCurrent board:\n')
        self.board.print_values()
        print('\nCurrent hand:')
        self.deck.print_deck()
        print(f'Please choose a card to play based on their name.\n'
              f'Type N to end your turn, type S to skip your turns.')
        prompt = input()
        if prompt == 'S':
            self.turn_active = False
            self.not_terminated = False
        elif prompt == 'N':
            self.turn_active = False
        else:
            card_to_play = next(x for x in self.deck.cards if x.name == prompt)
            self.play_card(card_to_play)

    def print_game(self):
        print(f'Name: {self.name} Faction: {self.deck.faction.value} HP: {self.hp}'
              f' Total Strength: {self.get_total_strength()}')
        self.board.print_values()

    def get_total_strength(self):
        return self.board.get_total_strength()

    def end_round(self, won):
        if not won:
            self.hp -= 1
        self.board.clean()

    def is_alive(self):
        return self.hp > 0

    def print_info(self):
        return f'{self.name} with {self.deck.faction.value}'


class Board:
    def __init__(self):
        self.melee_row = []
        self.ranged_row = []
        self.siege_row = []

    def get_row(self, card):
        if card.kind == Kind.MELEE:
            return self.melee_row
        elif card.kind == Kind.RANGED:
            return self.ranged_row
        return self.siege_row

    def add_card(self, card):
        row = self.get_row(card)
        row.append(card)

    def get_row_strength(self, row):
        strength = 0
        for card in row:
            strength += card.strength
        return strength

    def get_total_strength(self):
        return self.get_row_strength(self.melee_row) \
            + self.get_row_strength(self.ranged_row) + self.get_row_strength(self.siege_row)

    def clean(self):
        self.melee_row = []
        self.ranged_row = []
        self.siege_row = []

    def print_values(self):
        print(f'Melee Row: Strength {self.get_row_strength(self.melee_row)}')
        for card in self.melee_row:
            card.show_card()
        print(f'Ranged Row: Strength {self.get_row_strength(self.ranged_row)}')
        for card in self.ranged_row:
            card.show_card()
        print(f'Siege Row: Strength {self.get_row_strength(self.siege_row)}')
        for card in self.siege_row:
            card.show_card()


class Game:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two

    def print_game(self):
        self.player_one.print_game()
        self.player_two.print_game()

    def evaluate_round(self):
        print('\n\nRound Ended')
        player_one_won = self.player_one.board.get_total_strength() > self.player_two.board.get_total_strength()
        self.player_one.end_round(player_one_won)
        self.player_two.end_round(not player_one_won)
        player_who_won = self.player_one.name if player_one_won else self.player_two.name
        print(f'Player who won the round: {player_who_won}\n\n')

    def print_winner(self):
        print(f'Player who won the game: {self.player_one.name if self.player_one.is_alive else self.player_two.name}')

    def start_game(self):
        print(f'Game starting between {self.player_one.print_info()} and {self.player_two.print_info()}')
        while self.player_one.is_alive() and self.player_two.is_alive():
            self.player_one.not_terminated = True
            self.player_two.not_terminated = True
            while self.player_one.not_terminated or self.player_two.not_terminated:
                if self.player_one.not_terminated:
                    self.player_one.turn_active = True
                if self.player_two.not_terminated:
                    self.player_two.turn_active = True
                while self.player_one.turn_active:
                    self.player_one.play_cards()
                while self.player_two.turn_active:
                    self.player_two.play_cards()
            self.evaluate_round()

        self.print_winner()


cards = [
    Card('Poor Fucking Infantry', 1, Kind.MELEE),
    Card('Geralt of Rivia', 15, Kind.MELEE),
    Card('Vesemir', 6, Kind.MELEE),
    Card('Dethmold', 6, Kind.RANGED),
    Card('Trebuchet', 6, Kind.SIEGE),
    Card('Crinfid Reavers Dragon Hunter', 5, Kind.RANGED)
]
deck = Deck(cards, Faction.NOVIGRAD)
geralt = Player('Geralt of Rivia', deck, 2)

cards2 = [
    Card('Thaler', 1, Kind.MELEE),
    Card('Sabrina Glevissig', 10, Kind.RANGED),
    Card('Philippa Eilhart', 10, Kind.RANGED),
    Card('Ves', 5, Kind.MELEE),
    Card('Esterad Thissen', 50, Kind.MELEE),
    Card('Poor Fucking Infantry', 1, Kind.MELEE)
]
deck2 = Deck(cards2, Faction.NORTHERN_REALMS)
djikstra = Player('Djikstra', deck2, 2)

gwent_game = Game(geralt, djikstra)

gwent_game.start_game()
