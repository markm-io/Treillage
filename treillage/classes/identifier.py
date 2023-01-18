class Identifier(dict):
    def __init__(self, native: int, partner: str = ""):
        self.native = native
        self.partner = partner
        dict.__init__(self, native=native, partner=partner)
