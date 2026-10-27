MINIMUM_SERVICE_FEE_RS = 500


def minimum_service_fee(fee_rs):
    try:
        fee = int(fee_rs or 0)
    except (TypeError, ValueError):
        fee = 0
    return max(MINIMUM_SERVICE_FEE_RS, fee)
