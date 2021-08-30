class Species:
    def __init__(self, species_id):
        self.species_id = species_id
        self.members = []
        self.alive = None
        self.check_if_alive()

    def check_if_alive(self):
        if len(self.members) == 0:
            self.alive = False
        elif len(self.members) > 0:
            self.alive = True
        elif len(self.members) < 0:
            self.alive = None

