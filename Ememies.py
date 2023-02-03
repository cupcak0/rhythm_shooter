class Enemy:
    def __init__(self, health, damage, pos, player_health):
        self.health = health
        self.damage = damage
        self.pos = pos
        self.live = True
        self.player_health = player_health

    def get_damage(self, player_damage):
        if self.live:
            self.health -= player_damage

    def make_damage(self):
        if self.live:
            self.player_health -= self.damage

    def pos(self):
        if self.live:
            pass

    def death(self):
        if self.health <= 0:
            self.live = False
