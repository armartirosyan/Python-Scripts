ni-project #6 - Blackjack

import simplegui
import random
import time

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                          CARD_SIZE)
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        text = "Hand contains "
        for card in self.cards:
            text += str(card) + " "
        return text

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        ace = False
        for card in self.cards:
            if str(card)[1] == 'A' and value + 10 <=21:
                value += VALUES[str(card)[1]] +10
                ace = True
            else:
                if ace and value + VALUES[str(card)[1]] >21:
                    value = value +VALUES[str(card)[1]] -10
                    ace = False
                else:
                    value += VALUES[str(card)[1]]
        return value

    def draw(self, canvas, pos):
        for card in self.cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(str(card)[1]),
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(str(card)[0]))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            pos[0]+=78




# define deck class
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def __str__(self):
        text = "Deck contains "
        for card in self.deck:
            text += str(card) + " "
        return text

def deal():
    global outcome, in_play, deck, player, dealer, stand, score
    if in_play:
        outcome = "You forfeited!"
        score -=1
        lose.play()
        in_play= False
        stand = True
    else:
        outcome ="Hit or Stand?"
        deck = Deck()
        deck.shuffle()
        player = Hand()
        player.add_card(deck.deal_card())
        deal_card.play()
        player.add_card(deck.deal_card())
        deal_card.play()
        dealer = Hand()
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        in_play = True
        stand = False

def hit():
    global outcome, in_play, deck, player, dealer,score, stand

    if in_play and not stand:
        player.add_card(deck.deal_card())
        deal_card.play()
        if player.get_value()<=21:
            pass
        else:
            in_play = False
            outcome = "Sorry but you bust! Good luck next time!"
            stand = True
            score -=1
            lose.play()

def stand():
    global outcome, in_play, deck, player, dealer, score, stand
    stand = True
    if in_play:
        while dealer.get_value()<17:
            deal_card.play()
            dealer.add_card(deck.deal_card())
            if dealer.get_value() > 21:
                outcome = "Dealer bust player won"
                score +=1
                win.play()
                in_play = False
                break
        else:
            if player.get_value() >= dealer.get_value() and in_play:
                outcome = "Player won!"
                win.play()
                score +=1
                in_play=False
            else:
                lose.play()
                outcome = "Dealer won!"
                score -=1
                in_play= False


    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):

    canvas.draw_text('BlackJack', [100,100], 48, 'Aqua')
    canvas.draw_text('Dealer',[35,200],24, "Black")
    canvas.draw_text('Player',[35,400],24, "Black")
    canvas.draw_text(outcome,[175,350],24, "Black")
    canvas.draw_text('Score: ' + str(score), [400,100], 30, 'Black')

    if not stand:
        dealer.draw(canvas,[100,200])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                            [136,248], CARD_SIZE)
    else:
        dealer.draw(canvas,[100,200])

    player.draw(canvas,[100,400])



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
deal_card=simplegui.load_sound('https://drive.google.com/uc?export=download&id=0B2yN-6ogsjeTOUw2R1QwZG01YWs')
win=simplegui.load_sound('https://drive.google.com/uc?export=download&id=0B2yN-6ogsjeTR1Q2VHg3LXpfa00')
lose = simplegui.load_sound('https://drive.google.com/uc?export=download&id=0B2yN-6ogsjeTejVMaDk5ajRSaTQ')
# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
