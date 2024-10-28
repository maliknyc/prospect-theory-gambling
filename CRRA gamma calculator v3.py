import math
import pandas as pd

def utility(x, gamma):
    if gamma == 1:
        return math.log(1 + x)
    else:
        return ((1 + x) ** (1 - gamma) - 1) / (1 - gamma)

def solve_for_X2(gamma, sure_amount, X1, p1, p2):
    if X1 < -1 or sure_amount < -1:
        raise ValueError("Amounts must be greater than -1.")
    if p1 + p2 != 1:
        raise ValueError("Probabilities must sum to 1.")
    U_sure = utility(sure_amount, gamma)
    U_X1 = utility(X1, gamma)
    U_X2 = (U_sure - p1 * U_X1) / p2
    if gamma == 1:
        X2 = math.exp(U_X2) - 1
    else:
        base = U_X2 * (1 - gamma) + 1
        if base <= 0:
            raise ValueError("No solution exists with the given parameters.")
        X2 = base ** (1 / (1 - gamma)) - 1
    return X2

# PARAMETERS
gamma_list = [round(0 + 0.1 * i, 1) for i in range(31)]  # gamma from 0.0 to 3.0 in steps of 0.1
sure_amount = 150
X1 = 300
p1 = 0.5
p2 = 1 - p1

results = []

for gamma_value in gamma_list:
    try:
        X2 = solve_for_X2(gamma_value, sure_amount, X1, p1, p2)
        EV = p1 * X1 + p2 * X2  # expected value
        RP = round((EV - sure_amount) * 100 / sure_amount, 3)  # risk premium (%)
        results.append([gamma_value, X1, round(X2, 2), round(EV, 2), RP])
    except ValueError as e:
        # Handle cases where no solution exists
        results.append([gamma_value, X1, None, None, None])

pd.set_option('display.max_rows', None)


df = pd.DataFrame(results, columns=['γ', 'X1', 'X2', 'EV', 'RP (%)'])

print(df)

# define X1 amounts from (sure_amount + 10) to (sure_amount * 2) in increments of (sure_amount/15)
X1_list = list(range(160, 301, 10))  # [170, 180, 190, ..., 310]

# initialize dataframe w/ X1 values as indexes and gammas as columns
X2_table = pd.DataFrame(index=X1_list, columns=gamma_list)

# fill dataframe with X2 values
for X1_value in X1_list:
    for gamma_value in gamma_list:
        try:
            X2 = solve_for_X2(gamma_value, sure_amount, X1_value, p1, p2)
            X2_table.at[X1_value, gamma_value] = round(X2, 2)
        except ValueError:
            X2_table.at[X1_value, gamma_value] = None

#pd.set_option('display.max_columns', None)
#pd.set_option('display.width', None)

#print("\nX2 Table (Rows: X1 from $170 to $450 in $20 increments, Columns: Gamma 0.0 to 3.0 in 0.1 increments):\n")
#print(X2_table)

# export X2 Table to a CSV!
X2_table.to_csv('X2_table.csv', index=True)



