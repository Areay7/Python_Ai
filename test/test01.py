def calculate_management_fee(average_holdings):
    fee = 0

    if average_holdings <= 10000:
        fee = average_holdings * 0.04
    elif average_holdings <= 30000:
        fee = 10000 * 0.04 + (average_holdings - 10000) * 0.03
    elif average_holdings <= 80000:
        fee = 10000 * 0.04 + (30000 - 10000) * 0.03 + (average_holdings - 30000) * 0.02
    elif average_holdings <= 200000:
        fee = 10000 * 0.04 + (30000 - 10000) * 0.03 + (80000 - 30000) * 0.02 + (average_holdings - 80000) * 0.01
    else:
        fee = 10000 * 0.04 + (30000 - 10000) * 0.03 + (80000 - 30000) * 0.02 + (200000 - 80000) * 0.01 + (average_holdings - 200000) * 0.005

    return fee

average_holdings = 85000
fee = calculate_management_fee(average_holdings)
print(f"投资者的管理费：{fee:.2f} 元")
