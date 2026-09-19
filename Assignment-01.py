from abc import ABC, abstractmethod
from typing import Dict, Type



# Task 1: Payment Method Hierarchy


class PaymentMethod(ABC):
    @abstractmethod
    def get_details(self) -> str:
        """Returns string representation of payment parameters."""
        pass

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Processes the payment transaction for the given amount."""
        pass


class RazorpayCardPayment(PaymentMethod):
    def __init__(self, card_number: str, expiry: str, cvv: str, **kwargs):
        self.card_number = card_number
        self.expiry = expiry
        self.cvv = cvv

    def get_details(self) -> str:
        masked_card = f"**** **** **** {self.card_number[-4:]}" if len(self.card_number) >= 4 else self.card_number
        return f"Razorpay Card [{masked_card}]"

    def pay(self, amount: float) -> bool:
        print(f"[Razorpay Gateway] Charging {self.get_details()}: INR {amount:.2f}")
        return True


class RazorpayUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str, **kwargs):
        self.upi_id = upi_id

    def get_details(self) -> str:
        return f"Razorpay VPA [{self.upi_id}]"

    def pay(self, amount: float) -> bool:
        print(f"[Razorpay Gateway] Requesting collect payment from {self.get_details()}: INR {amount:.2f}")
        return True


class StripeCardPayment(PaymentMethod):
    def __init__(self, card_number: str, exp_month: str, exp_year: str, cvc: str, **kwargs):
        self.card_number = card_number
        self.exp_month = exp_month
        self.exp_year = exp_year
        self.cvc = cvc

    def get_details(self) -> str:
        masked_card = f"Ending in {self.card_number[-4:]}" if len(self.card_number) >= 4 else self.card_number
        return f"Stripe Card Token [{masked_card}]"

    def pay(self, amount: float) -> bool:
        print(f"[Stripe API] Authorizing card {self.get_details()} for ${amount:.2f}")
        return True


class StripeUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str, **kwargs):
        self.upi_id = upi_id

    def get_details(self) -> str:
        return f"Stripe UPI Intent [{self.upi_id}]"

    def pay(self, amount: float) -> bool:
        print(f"[Stripe API] Initiating UPI Intent for {self.get_details()}: ${amount:.2f}")
        return True



# Task 2: Payment Method Factory (Abstract Factory)


class FactoryPaymentMethod(ABC):
    factory: Dict[str, Type[PaymentMethod]] = {}

    @classmethod
    def get_payment_object(cls, method_type: str, **kwargs) -> PaymentMethod:
        normalized_type = method_type.strip().lower()
        if normalized_type not in cls.factory:
            raise ValueError(f"Unsupported payment method '{method_type}' for {cls.__name__}.")
        
        target_class = cls.factory[normalized_type]
        return target_class(**kwargs)


class RazorpayFactory(FactoryPaymentMethod):
    factory = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment
    }


class StripeFactory(FactoryPaymentMethod):
    factory = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment
    }



# Task 3: Aggregator Hierarchy


class Aggregator(ABC):
    def __init__(self, name: str, processing_fee: float, payment_factory: Type[FactoryPaymentMethod]):
        self.name = name
        self.processing_fee = processing_fee
        self.payment_factory = payment_factory

    def call_get_payment_object(self, method_type: str, amount: float, **kwargs) -> bool:
        total_amount = amount + (amount * self.processing_fee / 100.0)
        print(f"\nProcessing via {self.name} (Fee: {self.processing_fee}% | Total: {total_amount:.2f})...")
        
        # Delegates object creation to respective factory
        payment_obj = self.payment_factory.get_payment_object(method_type, **kwargs)
        return payment_obj.pay(total_amount)


class RazorpayAggregator(Aggregator):
    def __init__(self):
        super().__init__(name="Razorpay", processing_fee=2.0, payment_factory=RazorpayFactory)


class StripeAggregator(Aggregator):
    def __init__(self):
        super().__init__(name="Stripe", processing_fee=2.9, payment_factory=StripeFactory)


# Task 4: Aggregator Factory


class AggregatorFactory:
    factory: Dict[str, Type[Aggregator]] = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator
    }

    @classmethod
    def get_aggregator_object(cls, aggregator_name: str) -> Aggregator:
        key = aggregator_name.strip().lower()
        if key not in cls.factory:
            raise KeyError(f"Aggregator '{aggregator_name}' is not registered.")
        return cls.factory[key]()

    @classmethod
    def register_aggregator(cls, name: str, aggregator_cls: Type[Aggregator]):
        """Allows extension without altering factory core logic (Open/Closed Principle)."""
        cls.factory[name.strip().lower()] = aggregator_cls




# Task 5: CLI Client Workflow


def prompt_non_empty(message: str) -> str:
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

def main():
    print("==========================================")
    print("   Multi-Gateway Payment Engine Console   ")
    print("==========================================")
    
    try:
        gateway_choice = prompt_non_empty("Select Gateway (stripe / razorpay): ").lower()
        aggregator = AggregatorFactory.get_aggregator_object(gateway_choice)

        method_choice = prompt_non_empty("Select Payment Method (card / upi): ").lower()
        
        payment_kwargs = {}
        if method_choice == "card":
            payment_kwargs["card_number"] = prompt_non_empty("Enter Card Number: ")
            if gateway_choice == "razorpay":
                payment_kwargs["expiry"] = prompt_non_empty("Enter Expiry (MM/YY): ")
                payment_kwargs["cvv"] = prompt_non_empty("Enter CVV: ")
            else:
                payment_kwargs["exp_month"] = prompt_non_empty("Enter Exp Month (MM): ")
                payment_kwargs["exp_year"] = prompt_non_empty("Enter Exp Year (YY): ")
                payment_kwargs["cvc"] = prompt_non_empty("Enter CVC: ")
        elif method_choice == "upi":
            payment_kwargs["upi_id"] = prompt_non_empty("Enter UPI ID (e.g. user@bank): ")
        else:
            raise ValueError(f"Invalid payment method '{method_choice}'. Expected 'card' or 'upi'.")

        raw_amount = prompt_non_empty("Enter Payment Amount: ")
        amount = float(raw_amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        # Route execution dynamically
        success = aggregator.call_get_payment_object(method_choice, amount, **payment_kwargs)
        
        if success:
            print("\nTransaction status: SUCCESS")
        else:
            print("\nTransaction status: FAILED")

    except (ValueError, KeyError) as e:
        print(f"\n[Execution Error]: {e}")
    except Exception as e:
        print(f"\n[Unexpected Error]: {e}")

if __name__ == "__main__":
    main()
