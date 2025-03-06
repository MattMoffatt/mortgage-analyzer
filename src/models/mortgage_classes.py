import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime as dt
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

########################################################
"""
Mortgage dataclass documentation: 

Abstract mortgage dataclass to house the CurrentMortgage class
and NewMortgageScenario dataclasses for comparisons.

Properties:
    rate - interest rate on mortgage (as a percentage, e.g. 4.5 for 4.5%),
    years - years on loan term,
    tax - annual expected tax,
    ins - annual expected insurance,
    sqft - house square footage,
    monthly_tax - calculated from tax,
    monthly_ins - calculated from ins,
    total_periods - years * 12
    monthly_interest - interest rate / 100 / 12
    principal_and_interest - total mortgage principal and interest payment

    optional:
        extra_principal - amount of monthly extra principal you are paying
        prepay_periods - number of periods you expect to pay the extra principal

    methods:
        price - house price (calc'd or given based on subclass),
        total_pmt - principal + interest + tax + ins + pmi (calc'd or given based on subclass),
        monthly_pmi - amount of pmi paid monthly (calc'd or given based on subclass),
        periods_remaining - number of periods based on loan term or remaining term,
        end_date - calc'd from start_date and years or now() and years
        amortization_schedule - create a pandas dataframe of an amortization schedule
        estimate_equity_at_year - estimate equity after a certain number of years (assumed appreciation = 3%)

"""


@dataclass
class Mortgage(ABC):
    _rate: float = field(repr=True)
    _years: int = field(repr=True)
    _tax: float = field(repr=True)
    _ins: float = field(repr=True)
    _sqft: int = field(repr=True)
    _extra_principal: Optional[float] = field(default=0.0, repr=True)  # optional
    _prepay_periods: Optional[int] = field(default=0, repr=True)  # optional

    def __post_init__(self):
        # Store initial values
        rate = self._rate
        years = self._years
        tax = self._tax
        ins = self._ins
        sqft = self._sqft
        extra_principal = self._extra_principal
        prepay_periods = self._prepay_periods

        # Apply validation through setters
        self.rate = rate
        self.years = years
        self.tax = tax
        self.ins = ins
        self.sqft = sqft
        self.extra_principal = extra_principal
        self.prepay_periods = prepay_periods

    @property
    def rate(self) -> float:
        return self._rate

    @rate.setter
    def rate(self, value: float):
        if value <= 0:
            raise ValueError("Interest rate must be positive")
        if value > 25:
            raise ValueError("Interest rate is unreasonably high (>25%)")
        self._rate = value

    @property
    def years(self) -> int:
        return self._years

    @years.setter
    def years(self, value: int):
        if value <= 0:
            raise ValueError("Loan term must be positive")
        if value > 50:
            raise ValueError("Loan term exceeds 50 years")
        self._years = value

    @property
    def tax(self) -> float:
        return self._tax

    @tax.setter
    def tax(self, value: float):
        if value < 0:
            raise ValueError("Property tax cannot be negative")
        self._tax = value

    @property
    def ins(self) -> float:
        return self._ins

    @ins.setter
    def ins(self, value: float):
        if value < 0:
            raise ValueError("Insurance cannot be negative")
        self._ins = value

    @property
    def sqft(self) -> int:
        return self._sqft

    @sqft.setter
    def sqft(self, value: int):
        if value <= 0:
            raise ValueError("Square footage must be positive")
        self._sqft = value

    @property
    def monthly_tax(self) -> float:
        return self.tax / 12

    @property
    def monthly_ins(self) -> float:
        return self.ins / 12

    @property
    def total_periods(self) -> int:
        return self.years * 12

    @property
    def extra_principal(self) -> float:
        return self._extra_principal

    @extra_principal.setter
    def extra_principal(self, value: float):
        if value < 0:
            raise ValueError("Extra principal payment cannot be negative")
        self._extra_principal = value

    @property
    def prepay_periods(self) -> int:
        return self._prepay_periods

    @prepay_periods.setter
    def prepay_periods(self, value: int):
        if value < 0:
            raise ValueError("Prepay periods cannot be negative")
        self._prepay_periods = value

    @property
    def monthly_interest(self) -> float:
        return self.rate / 100 / 12

    @property
    def principal_and_interest(self) -> float:
        if self.monthly_interest == 0:
            return self.loan_amount / self.periods_remaining

        # calculate principal_and_interest
        return self.loan_amount * (
            self.monthly_interest
            * (1 + self.monthly_interest) ** self.periods_remaining
            / ((1 + self.monthly_interest) ** self.periods_remaining - 1)
        )

    """
    These abstract methods need to be implemented at the sub class level
    due to differences in how the calculations will run between the two 
    subclasses.
    """

    @abstractmethod
    def price(self) -> float:
        pass

    @abstractmethod
    def total_pmt(self) -> float:
        pass

    @abstractmethod
    def monthly_pmi(self) -> float:
        pass

    @abstractmethod
    def periods_remaining(self) -> int:
        pass

    @abstractmethod
    def end_date(self) -> str:
        pass

    @abstractmethod
    def loan_amount(self) -> float:
        pass

    # Calculation methods

    def amortization_schedule(self) -> pd.DataFrame:
        """
        Create an amortization shcedule that can be used for visualizing loan
        payoff. Can be affected by extra pricinpal payments.
        """
        schedule = []
        remaining_balance = self.loan_amount

        for period in range(1, self.periods_remaining + 1):
            if remaining_balance <= 0:
                break

            interest_pmt = remaining_balance * self.monthly_interest
            principal_pmt = min(
                self.principal_and_interest - interest_pmt, remaining_balance
            )
            extra_principal = (
                min(self.extra_principal, remaining_balance - principal_pmt)
                if remaining_balance > principal_pmt
                else 0
            )
            remaining_balance -= principal_pmt + extra_principal

            schedule.append(
                {
                    "month": period,
                    "payment": self.principal_and_interest,
                    "principal": principal_pmt,
                    "interest": interest_pmt,
                    "principal_paydown": extra_principal,
                    "balance": max(0, remaining_balance),
                }
            )

            df = pd.DataFrame(schedule)

            # Round monetary values to 2 decimal places
            for col in df.columns:
                df[col] = df[col].round(2)

        return df

    def _calculate_remaining_balance_at_year(self, loan_year: int) -> float:
        """
        Helper method to calculate the remaining loan balance after a given number of years

        Parameters:
        - loan_year: Number of years to project

        Returns:
        - Remaining balance in dollars
        """

        remaining_balance = self.loan_amount

        for month in range(loan_year * 12):
            interest_pmt = remaining_balance * self.monthly_interest
            principal_pmt = min(
                self.principal_and_interest - interest_pmt, remaining_balance
            )
            extra_principal = (
                min(self.extra_principal, remaining_balance - principal_pmt)
                if remaining_balance > principal_pmt
                else 0
            )
            remaining_balance -= principal_pmt + extra_principal

        return max(0, remaining_balance)  # Ensure we don't return negative balance

    def estimate_value_at_year(
        self, loan_year: int, annual_appreciation: float = 0.03
    ) -> float:
        """
        Estimate property value after a certain number of years

        Parameters:
        - loan_year: Number of years to project
        - annual_appreciation: Annual home value appreciation rate (default 3%)

        Returns:
        - Estimated property value in dollars
        """

        return self.price * ((1 + annual_appreciation) ** loan_year)

    def estimate_equity_at_year(
        self, loan_year: int, annual_appreciation: float = 0.03
    ) -> float:
        """
        Estimate equity after a certain number of years

        Parameters:
        - loan_year: Number of years to project
        - annual_appreciation: Annual home value appreciation rate (default 3%)

        Returns:
        - Estimated equity in dollars
        """

        future_value = self.estimate_value_at_year(loan_year, annual_appreciation)
        remaining_balance = self._calculate_remaining_balance_at_year(loan_year)

        return future_value - remaining_balance
    
    def pmi_periods_remaining(self) -> int:
        """
        Calculate how many months of PMI payments remain until reaching 80% LTV ratio.
        
        Returns:
            int: Number of monthly periods until PMI can be removed, or 0 if PMI is 
                not required or already below 80% LTV.
        """
        # If already at 80% LTV or less, no PMI needed
        if self.loan_amount / self.price <= 0.8:
            return 0
            
        # Start with current loan amount
        current_balance = self.loan_amount
        target_balance = self.price * 0.8  # 80% of property value is the threshold
        periods = 0
        
        # Continue until reaching target balance or loan is paid off
        while current_balance > target_balance and periods < self.periods_remaining:
            # Calculate interest for this period
            interest = current_balance * self.monthly_interest
            
            # Calculate principal payment
            principal_payment = min(
                self.principal_and_interest - interest, 
                current_balance
            )
            
            # Calculate any extra principal
            extra_principal = (
                min(self.extra_principal, current_balance - principal_payment)
                if (current_balance > principal_payment and 
                    (self.prepay_periods == 0 or periods < self.prepay_periods))
                else 0
            )
            
            # Update the current balance
            current_balance -= (principal_payment + extra_principal)
            periods += 1
            
        # Return the number of periods calculated (or 0 if we didn't reach the target)
        return periods if current_balance <= target_balance else 0
        


############################################################

"""
CurrentMortgage dataclass documentation:

Properties:

Mortgage Abstract Class - inherited
----------------------------------------
    rate - interest rate on mortgage (as a percentage, e.g. 4.5 for 4.5%),
    years - years on loan term,
    tax - annual expected tax,
    ins - annual expected insurance,
    sqft - house square footage

    Optional:
        extra_principal - amount of monthly extra principal you are paying
        prepay_periods - number of periods you expect to pay the extra principal

CurrentMortgage Class
----------------------------------------
    total_pmt - principal + interest + tax + ins + pmi,
    original_loan - original mortgage amount,
    current_loan - current principal balance left unpaid,
    start_date - loan origination date as a string,
    price_per_sqft - estimated price per sqft from Zillow or Redfin or other,
    price - calc'd from price_per_sqft * sqft
    monthly_pmi - monthly pmi paid,

    Calculated:
        loan_age_days - age of loan in days calculated using datetime functions,
        periods_passed - convert loan_age_days to number of periods passed,
        end_date - date when mortgage is paid off based on start_date and years
        loan_begin_date - datetime object of the loan start date
        loan_end_date - datetime object of the loan end date
        days_remaining - number of days until the loan is paid off
        periods_remaining - number of payment periods remaining until the loan is paid off
        loan_to_value - ratio of current loan amount to property value
        equity_value - difference between property value and current loan amount
        monthly_escrow_shortage_pmt - amount of total_pmt allocated to recovering escrow deficit

"""


@dataclass(kw_only=True)
class CurrentMortgage(Mortgage):
    _original_loan: float = field(repr=True)
    _loan_amount: float = field(repr=True)
    _start_date: str = field(repr=True)
    _price_per_sqft: float = field(repr=True)
    _monthly_pmi: float = field(repr=True)
    _total_pmt: float = field(repr=True)

    def __post_init__(self):
        # Call parent validation
        super().__post_init__()

        # Store initial values
        original_loan = self._original_loan
        loan_amount = self._loan_amount
        start_date = self._start_date
        price_per_sqft = self._price_per_sqft
        monthly_pmi = self._monthly_pmi
        total_pmt = self._total_pmt

        # Apply validation through setters
        self.original_loan = original_loan
        self.loan_amount = loan_amount
        self.start_date = start_date
        self.price_per_sqft = price_per_sqft
        self.monthly_pmi = monthly_pmi
        self.total_pmt = total_pmt

    @property
    def original_loan(self) -> float:
        return self._original_loan

    @original_loan.setter
    def original_loan(self, value: float):
        if value <= 0:
            raise ValueError("Original loan amount must be positive")
        self._original_loan = value

    @property
    def loan_amount(self) -> float:
        return self._loan_amount

    @loan_amount.setter
    def loan_amount(self, value: float):
        if value < 0:
            raise ValueError("Current loan amount cannot be negative")
        if value > self.original_loan:
            raise ValueError("Current loan amount cannot exceed original loan")
        self._loan_amount = value

    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, value: str):
        # Basic format validation
        try:
            dt.strptime(value, "%m/%d/%Y")
        except ValueError:
            raise ValueError("Start date must be in format 'MM/DD/YYYY'")
        self._start_date = value

    @property
    def price_per_sqft(self) -> float:
        return self._price_per_sqft

    @price_per_sqft.setter
    def price_per_sqft(self, value: float):
        if value <= 0:
            raise ValueError("Price per square foot must be positive")
        self._price_per_sqft = value

    @property
    def monthly_pmi(self) -> float:
        return self._monthly_pmi

    @monthly_pmi.setter
    def monthly_pmi(self, value: float):
        if value < 0:
            raise ValueError("Monthly PMI cannot be negative")
        self._monthly_pmi = value

    @property
    def total_pmt(self) -> float:
        return self._total_pmt

    @total_pmt.setter
    def total_pmt(self, value: float):
        if value <= 0:
            raise ValueError("Total payment must be positive")
        self._total_pmt = value

    @property
    def price(self) -> float:
        return self.price_per_sqft * self.sqft

    @property
    def loan_begin_date(self) -> dt:
        return dt.strptime(self.start_date, "%m/%d/%Y")

    @property
    def loan_age_days(self) -> int:
        return (dt.now() - self.loan_begin_date).days

    @property
    def periods_passed(self) -> int:
        return math.ceil(self.loan_age_days / 30.4) - 1

    @property
    def loan_end_date(self) -> dt:
        return self.loan_begin_date + relativedelta(years=self.years)

    @property
    def end_date(self) -> str:
        return self.loan_end_date.strftime("%m/%d/%Y")

    @property
    def days_remaining(self) -> int:
        return (self.loan_end_date - dt.now()).days

    @property
    def periods_remaining(self) -> int:
        return math.ceil(self.days_remaining / 30.4) - 1

    @property
    def loan_to_value(self) -> float:
        return self.loan_amount / self.price

    @property
    def equity_value(self) -> float:
        return self.price - self.loan_amount

    @property
    def monthly_escrow_shortage_pmt(self) -> float:
        return (
            self.total_pmt
            - self.monthly_tax
            - self.monthly_ins
            - self.monthly_pmi
            - self.extra_principal
            - self.principal_and_interest
        )


############################################################

"""
NewMortgageScenario dataclass documentation:

Properties:

Mortgage Abstract Class - inherited
----------------------------------------
    rate - interest rate on mortgage (as a percentage, e.g. 4.5 for 4.5%),
    years - years on loan term,
    tax - annual expected tax,
    ins - annual expected insurance,
    sqft - house square footage

    Optional:
        extra_principal - amount of monthly extra principal you are paying
        prepay_periods - number of periods you expect to pay the extra principal

NewMortgageScenario Class
----------------------------------------
    price - given

    calculated:
        downpayment_percent - percent of purchase price expected to pay down,
        downpayment_amount - dollar amount of downpayment,
        monthly_pmi - calculated based on assumed rate and downpayment percent,
        total_pmt - principal_and_interest + monthly_tax + monthly_ins + monthly_pmi + extra_principal
        price_per_sqft - calculated price / sqft
        loan_amount - calculated price - downpayment_amount

"""


@dataclass(kw_only=True)
class NewMortgageScenario(Mortgage):
    _price: float = field(repr=True)
    # allow either downpayment_percent or downpayment_amount to be provided
    _downpayment_percent: Optional[float] = field(default=None, repr=True)
    _downpayment_amount: Optional[float] = field(default=None, repr=True)
    _pmi_rate: float = field(default=0.005, repr=True)

    def __post_init__(self):
        # Call parent validation
        super().__post_init__()

        # Store initial values
        price = self._price
        downpayment_percent = self._downpayment_percent
        downpayment_amount = self._downpayment_amount
        pmi_rate = self._pmi_rate

        # Apply validation through setters
        self.price = price
        self.pmi_rate = pmi_rate

        # Handle downpayment logic
        if downpayment_percent is None and downpayment_amount is None:
            self._downpayment_percent = 0.2
            self._downpayment_amount = self.price * 0.2
        elif downpayment_percent is not None and downpayment_amount is not None:
            self.downpayment_percent = downpayment_percent
            # Percent takes precedence, so amount will be calculated from it
        elif downpayment_percent is not None:
            self.downpayment_percent = downpayment_percent
        else:  # downpayment_amount is not None
            self.downpayment_amount = downpayment_amount

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def pmi_rate(self) -> float:
        return self._pmi_rate

    @pmi_rate.setter
    def pmi_rate(self, value: float):
        if value < 0:
            raise ValueError("PMI rate cannot be negative")
        if value > 0.05:  # 5% would be extremely high for PMI
            raise ValueError("PMI rate is unreasonably high (>5%)")
        self._pmi_rate = value

    @property
    def downpayment_percent(self) -> float:
        return self._downpayment_percent

    @downpayment_percent.setter
    def downpayment_percent(self, value: float):
        if value < 0:
            raise ValueError("Downpayment percentage cannot be negative")
        if value > 1:
            raise ValueError("Downpayment percentage cannot exceed 100%")
        self._downpayment_percent = value
        self._downpayment_amount = self.price * value

    @property
    def downpayment_amount(self) -> float:
        return self._downpayment_amount

    @downpayment_amount.setter
    def downpayment_amount(self, value: float):
        if value < 0:
            raise ValueError("Downpayment amount cannot be negative")
        if value > self.price:
            raise ValueError("Downpayment amount cannot exceed price")
        self._downpayment_amount = value
        self._downpayment_percent = value / self.price

    @property
    def loan_amount(self) -> float:
        return self.price - self.downpayment_amount

    @property
    def monthly_pmi(self) -> float:
        if self.downpayment_percent >= 0.2:
            return 0.0
        else:
            return self.loan_amount * self.pmi_rate / 12

    @property
    def periods_remaining(self) -> int:
        return self.years * 12

    @property
    def price_per_sqft(self) -> float:
        return self.price / self.sqft

    @property
    def total_pmt(self) -> float:
        return (
            self.principal_and_interest
            + self.monthly_tax
            + self.monthly_ins
            + self.monthly_pmi
            + self.extra_principal
        )

    @property
    def end_date(self) -> str:
        start_date = dt.now()
        end_date = start_date + relativedelta(years=self.years)
        return end_date.strftime("%m/%d/%Y")

    @property
    def closing_costs(self) -> float:
        return self.price * 0.03
    
    @property
    def initial_investment(self) -> float:
        return self.downpayment_amount + self.closing_costs
    
