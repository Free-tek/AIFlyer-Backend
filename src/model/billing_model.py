from enum import Enum

class PaymentLinkDetails(Enum):
    STARTER = "plink_1QX9OeG2V6OlgcTIiCeSZal4"
    PRO = "plink_1QX9OwG2V6OlgcTIWRkzpDgF"
    PREMIUM = "plink_1QX9PLG2V6OlgcTIUUU69E0u"

class PlanTier(Enum):
    FREE = "free"
    STARTER = "starter"
    PRO = "pro"
    PREMIUM = "premium"