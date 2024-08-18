class  CalculateReturns : 
    def __init__(self, Principle: float, expense_ratio: float, num_years: int, returns: float, stamp_duty: float = 0.005, investment_type: str = "SIP") : 
        self.Principle = Principle
        self.expense_ratio = expense_ratio
        self.num_years = int(num_years)
        self.stamp_duty = stamp_duty
        self.returns = returns
        self.investment_type = investment_type

    def calculate_returns_for_lumpsum(self) : 
        return self.Principle * (pow(1 + (self.returns/100) - (self.expense_ratio/100), self.num_years) - self.stamp_duty)
    
    def __calculate_return_rate(self) : 
        return (pow((1 + (self.returns / 100)) / (1 + (self.expense_ratio / 100)), 1 / 12) - 1)

    def calculate_returns_for_SIP(self) : 
        rm, num_months = self.__calculate_return_rate(), self.num_years * 12
        return self.Principle * (1 - (self.stamp_duty/100)) * ((pow(1 + rm, num_months) - 1) / rm) * (1 + rm)
    
    def calculate_tax(self) : 
        if self.num_years <= 1 : 
            if self.investment_type != "SIP" : output = self.calculate_returns_for_lumpsum() 
            else : output = self.calculate_returns_for_SIP()
            return round(output*0.8), round(output)
        else : 
            if self.investment_type != "SIP" : output = self.calculate_returns_for_lumpsum() 
            else : output = self.calculate_returns_for_SIP()

            if output <= 125000 : 
                return round(output), round(output)
            else : 
                return round(125000 + 0.875*(output - 125000)), round(output)