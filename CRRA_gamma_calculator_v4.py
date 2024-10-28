import math
import pandas as pd

def utility(x, gamma, W0):

    W = W0 + x  # total wealth
    if W <= 0:
        raise ValueError("Total wealth (W0 + x) must be greater than 0 for standard CRRA.")
    if gamma == 1:
        return math.log(W)
    else:
        return (W ** (1 - gamma) - 1) / (1 - gamma)

def solve_for_X2(gamma, sure_amount, X1, p1, p2, W0):

    # find utilities
    U_sure = utility(sure_amount, gamma, W0)
    U_X1 = utility(X1, gamma, W0)

    U_X2 = (U_sure - p1 * U_X1) / p2

    # invert utility function to find X2
    if gamma == 1:
        X2 = math.exp(U_X2) - W0
    else:
        base = U_X2 * (1 - gamma) + 1
        if base <= 0:
            raise ValueError("No solution exists with the given parameters.")
        X2 = base ** (1 / (1 - gamma)) - W0

    return X2

# PARAMETERS
gamma_list = [round(0 + 0.1 * i, 1) for i in range(31)]  # gamma from 0.0 to 3.0 in steps of 0.1
sure_amount = 150
X1 = 300
p1 = 0.5 # probability of gain prospeect
p2 = 1 - p1
W0 = 1000 # starting wealth

results = []

for gamma_value in gamma_list:
    try:
        X2 = solve_for_X2(gamma_value, sure_amount, X1, p1, p2, W0)
        EV = p1 * X1 + p2 * X2  # expected value
        RP = round((EV - sure_amount) * 100 / sure_amount, 3)  # risk premium (%)
        results.append([gamma_value, X1, round(X2, 2), round(EV, 2), RP])
    except ValueError as e:
        results.append([gamma_value, X1, None, None, None])

pd.set_option('display.max_rows', None)

df = pd.DataFrame(results, columns=['γ', 'X1', 'X2', 'EV', 'RP (%)'])

print(df)

# define X1 amounts from (sure_amount + 10) to (sure_amount * 2) in increments of (sure_amount/15)
# adjusting to match increments of 10 as per original code
X1_list = list(range(160, 301, 10))  # [160, 170, 180, ..., 300]

X2_table = pd.DataFrame(index=X1_list, columns=gamma_list)


for X1_value in X1_list:
    for gamma_value in gamma_list:
        try:
            X2 = solve_for_X2(gamma_value, sure_amount, X1_value, p1, p2, W0)
            X2_table.at[X1_value, gamma_value] = round(X2, 2)
        except ValueError:
            X2_table.at[X1_value, gamma_value] = None

# optionally, display the table
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# print("\nX2 Table (Rows: X1 from $160 to $300 in $10 increments, Columns: Gamma 0.0 to 3.0 in 0.1 increments):\n")
# print(X2_table)


X2_table.to_csv('X2_table_CRRA.csv', index=True)
