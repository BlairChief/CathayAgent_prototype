from math import log
from json import dumps
from typing import Union
from phi.tools import Toolkit
from phi.utils.log import logger

class FirstMillionCalculator(Toolkit):
    def __init__(self):
        super().__init__(name='first_million_calculator')
        self.register(self.calculate_first_million)

    def calculate_first_million(
        self,
        annual_return_rate: Union[float, int],
        target_amount: Union[float, int],
        monthly_saving: Union[float, int]
    ):
        monthly_return_rate = (annual_return_rate / 100) / 12
        months_needed = log((target_amount * monthly_return_rate / monthly_saving) + 1) / log(1 + monthly_return_rate)
        years_needed = months_needed / 12

        logger.info(f"Parameters:\n1. Annual return rate: {annual_return_rate}\n2. Target amount: {target_amount}\n3. Monthly saving: {monthly_saving}\n\nReturns:\n1. Monthly return rate: {monthly_return_rate}\n2. Months needed: {months_needed}\n3. Years needed: {years_needed}.")
        return dumps({
            "operation": "calculate_first_million",
            "result": years_needed
        })