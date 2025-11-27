from __future__ import annotations

from typing import Dict, Optional


class SceneManager:
    """
    Egyszerű scene manager.
    """

    def __init__(self, game: "Game"):
        self.game = game
        self.scenes: Dict[str, "Scene"] = {}
        self.current: Optional["Scene"] = None
        self.current_name: Optional[str] = None

    def register(self, name: str, scene: "Scene"):
        self.scenes[name] = scene

    def go_to(self, name: str):
        if self.current:
            self.current.exit()

        self.current_name = name
        self.current = self.scenes[name]
        self.current.enter()

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt: float):
        if self.current:
            self.current.update(dt)

    def draw(self, surface):
        if self.current:
            self.current.draw(surface)
