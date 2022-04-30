class Player:
    def __init__(self, id, wins = 0, losses = 0, ranking = 1000, tourney_placings = ""):
        self.id = id
        self.wins = wins
        self.losses = losses
        self.ranking = ranking
        self.tourney_placings = tourney_placings
    