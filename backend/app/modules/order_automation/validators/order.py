class OrderValidator:
    @staticmethod
    def validate_status_transition(current_status: str, new_status: str) -> None:
        allowed = {
            "pending": ["processing", "cancelled"],
            "processing": ["shipped", "cancelled"],
            "shipped": ["delivered"],
            "delivered": [],
            "cancelled": [],
        }
        if new_status not in allowed.get(current_status, []):
            raise ValueError(f"Invalid status transition from {current_status} to {new_status}")
