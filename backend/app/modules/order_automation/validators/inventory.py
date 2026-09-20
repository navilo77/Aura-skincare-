class InventoryValidator:
    @staticmethod
    def validate_reservation(quantity_on_hand: int, quantity_reserved: int, requested_quantity: int) -> None:
        available = quantity_on_hand - quantity_reserved
        if requested_quantity > available:
            raise ValueError("Insufficient available inventory for reservation")
        if quantity_reserved + requested_quantity > quantity_on_hand:
            raise ValueError("Reservation would exceed quantity on hand")

    @staticmethod
    def validate_deduction(quantity_on_hand: int, quantity_to_deduct: int) -> None:
        if quantity_to_deduct > quantity_on_hand:
            raise ValueError("Cannot deduct more than quantity on hand")
