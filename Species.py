class Species:
    def __init__(self, species_id):
        self.species_id = species_id
        self.members = []
        self.alive = None
        self.epoch_since_last_progress = 0
        self.check_if_alive()

    def check_if_alive(self):
        if len(self.members) == 0:
            self.alive = False
        elif len(self.members) > 0:
            self.alive = True
        elif len(self.members) < 0:
            self.alive = None

    def add_member(self, member):
        self.members.append(member)

    def get_number_of_members(self):
        return len(self.members)
