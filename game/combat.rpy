init python:
    class Health:
        """Displays a rudimentary health bar for actor"""
        def __init__(self, max_health, current_health):
            super(Health, self).__init__()
            self.max_health = max_health
            self.current_health = current_health


