
class Material:
    values = {}

    def __init__(self, name, EMod, Nu, Rho):
        self.name = name
        self.emod = EMod
        self.nu = Nu
        self.rho = Rho
        Material.values.update({name: [EMod, Nu, Rho]})


steel = Material("steel", 210 * 10**9, 0.27, 7.84 * 10**3)
aluminum = Material("aluminum", 70 * 10**9, 0.34, 2.70 * 10**3)
glass = Material("glass", 65 * 10**9, 0.24, 2.50 * 10**3)
concrete = Material("concrete", 30 * 10**9, 0.20, 2.40 * 10**3)
rubber = Material("rubber", 5 * 10**9, 0.39, 1.20 * 10**3)

