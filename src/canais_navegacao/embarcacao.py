class Embarcacao:
    """Representa os dados básicos de uma embarcação."""

    def __init__(self, lpp: float, boca: float, calado: float, cb: float) -> None:
        self.lpp = lpp
        self.boca = boca
        self.calado = calado
        self.cb = cb