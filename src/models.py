from pydantic import BaseModel


class CustomerInput(BaseModel):
    age: int
    gender: str
    tenure_months: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    payment_method: str
    paperless_billing: str
    num_support_tickets: int
    num_logins_last_month: int
    feature_usage_score: float
    late_payments: int
    partner: str
    dependents: str
    internet_service: str
    online_security: str
    online_backup: str
    device_protection: str
    tech_support: str
    streaming_tv: str
    streaming_movies: str