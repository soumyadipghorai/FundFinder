class CalculateReturns:
    """
    A class to calculate returns for Lumpsum and SIP investments, including tax calculations for LTCG and STCG.
    """

    def __init__(self, Principle: float, expense_ratio: float, num_years: int, returns: float, stamp_duty: float = 0.005, investment_type: str = "SIP"):
        """
        Initializes the CalculateReturns class with the given parameters.

        Args:
            Principle (float): The principal investment amount.
            expense_ratio (float): The annual expense ratio of the fund.
            num_years (int): The investment duration in years.
            returns (float): The annual return percentage of the fund.
            stamp_duty (float, optional): The stamp duty percentage. Default is 0.005.
            investment_type (str, optional): The type of investment ("SIP" or "Lumpsum"). Default is "SIP".
        """
        self.Principle = Principle
        self.expense_ratio = expense_ratio
        self.num_years = int(num_years)
        self.stamp_duty = stamp_duty
        self.returns = returns
        self.investment_type = investment_type

    def calculate_returns_for_lumpsum(self):
        """
        Calculates the total return for a Lumpsum investment before tax.

        Returns:
            float: The total returns before tax.
        """
        return_before_tax = self.Principle * (pow(1 + (self.returns / 100) - (self.expense_ratio / 100), self.num_years) - self.stamp_duty)
        return round(return_before_tax)

    def __calculate_return_rate(self):
        """
        Calculates the monthly return rate for SIP based on the annual return and expense ratio.

        Returns:
            float: The monthly return rate.
        """
        return pow((1 + (self.returns / 100)) / (1 + (self.expense_ratio / 100)), 1 / 12) - 1

    def calculate_returns_for_SIP(self, num_year: int):
        """
        Calculates the total returns for an SIP investment before tax and the total principal invested.

        Args:
            num_year (int): The duration of the SIP in years.

        Returns:
            tuple: A tuple containing:
                - float: The total returns before tax.
                - float: The total principal invested.
        """
        rm = self.__calculate_return_rate()
        num_months = num_year * 12
        return_before_tax = self.Principle * (1 - (self.stamp_duty / 100)) * ((pow(1 + rm, num_months) - 1) / rm) * (1 + rm)
        total_principle = num_months * self.Principle
        return round(return_before_tax), round(total_principle)

    def calculate_tax(self):
        """
        Calculates the tax-adjusted returns based on LTCG and STCG rules.

        Returns:
            tuple: A tuple containing:
                - float: The total returns after tax.
                - float: The total returns before tax.
        """
        if self.num_years <= 1:
            if self.investment_type != "SIP":
                return_before_tax = self.calculate_returns_for_lumpsum()
                profit = return_before_tax - self.Principle
            else:
                return_before_tax, total_principle = self.calculate_returns_for_SIP(num_year=self.num_years)
                profit = return_before_tax - total_principle

            total_tax = profit * 0.2 if profit > 0 else 0
            return round(return_before_tax - total_tax), round(return_before_tax)

        else:
            if self.investment_type != "SIP":
                return_before_tax = self.calculate_returns_for_lumpsum()
                profit = return_before_tax - self.Principle
                if profit <= 125000:
                    return round(return_before_tax), round(return_before_tax)
                else:
                    total_tax = (profit - 125000) * 0.125
                    return round(return_before_tax - total_tax), round(return_before_tax)
            else:
                return_before_tax, total_principle = self.calculate_returns_for_SIP(num_year=self.num_years)

                # Calculate LTCG for SIP
                temp_rbt, temp_principle = self.calculate_returns_for_SIP(num_year=self.num_years - 1)
                LTCG = temp_rbt - temp_principle
                LTCG_tax = 0.125 * (LTCG - 125000) if LTCG > 125000 else 0

                # Calculate STCG for SIP
                STCG_before_tax, stcg_principle = self.calculate_returns_for_SIP(num_year=1)
                STCG = STCG_before_tax - stcg_principle
                STCG_tax = 0.2 * STCG if STCG > 0 else 0

                total_tax = LTCG_tax + STCG_tax
                return round(return_before_tax - total_tax), round(return_before_tax)
