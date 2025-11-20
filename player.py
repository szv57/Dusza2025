from card import Card


class Player:
    def __init__(self):
        self.collection = []
        self.deck       = []
    

    def collection_add(self, card: Card):
        if not any(c.name == card.name for c in self.collection):
            self.collection.append(card)