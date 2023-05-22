prime = 0.05

def calc_paying_from_budget(persent: float, sum_of_month: int):
    number_of_year = sum_of_month/12.0
    return lambda pay_in_total: pay_in_total / ((prime + persent) * number_of_year + 1)



htz_36=calc_paying_from_budget(0.0025, 36)
geely=calc_paying_from_budget(0.007, 60)
htz_72=calc_paying_from_budget(0.01, 72)



def cal_pay_from_price(persent: float, sum_of_month: int):
    number_of_year = sum_of_month / 12.0
    return lambda pay_from_price: (number_of_year * (persent+prime) + 1) * pay_from_price


htz_36_ = cal_pay_from_price(0.0025, 36)
geely_ = cal_pay_from_price(0.007, 60)
htz_72_ = cal_pay_from_price(0.01, 72)


amount_of_loan = 150_000
max_willing_to_pay = 2000



a=1
