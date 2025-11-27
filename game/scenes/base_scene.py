class Scene:
    """
    Absztrakt scene.
    A többi jelenet ebből származik.
    """

    def __init__(self, game: "Game"):
        self.game = game

    # Életciklus-metódusok
    def enter(self):
        """A jelenet aktiválásakor hívódik meg."""
        pass

    def exit(self):
        """A jelenet elhagyásakor hívódik meg."""
        pass

    # Fő loop metódusok
    def handle_event(self, event):
        pass

    def update(self, dt: float):
        pass

    def draw(self, surface):
        pass
