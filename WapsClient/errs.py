
class FrontRunErr(Exception):
    pass



class FeatureNotReady(FrontRunErr):
    pass

class TooHighGas(FrontRunErr):
    pass

class LowBalance(FrontRunErr):
    pass