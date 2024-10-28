import math
import pandas as pd

def utility_gain(x, gamma):
    if gamma == 1:
        return math.log(1 + x)
    else:
        return ((1 + x) ** (1 - gamma) - 1) / (1 - gamma)

def utility_loss(x, gamma, lam):
    if gamma == 1:
        return -lam * math.log(1 + x)
    else:
        return -lam * ((1 + x) ** (1 - gamma) - 1) / (1 - gamma)

def solve_for_X2_lambda(Y_G, Y_L, X1, p1, lambda_value):
    p2 = 1 - p1
    # compute utility of gain
    U_gain = utility_gain(X1, Y_G)
    # expected utility equation: EU = p1 * U_gain + p2 * U_loss = 0
    # solve for U_loss
    U_loss = - (p1 * U_gain) / p2
    # invert utility function to find X2
    if Y_L == 1:
        exponent = -U_loss / lambda_value
        X2 = math.exp(exponent) - 1
    else:
        base = -U_loss * (1 - Y_L) / lambda_value + 1
        if base <= 0:
            raise ValueError("Invalid base; cannot compute loss amount.")
        X2 = base ** (1 / (1 - Y_L)) - 1
    return X2  # X2 is the loss aamount

# PARAMETERS
lambda_list = [round(1 + 0.1 * i, 1) for i in range(41)]  # lambdas from 1.0 to 5.0 in steps of 0.1
Y_G = 1  # gamma in gains
Y_L = 1  # gamma in losses
X1 = 100   # gain prospect
p1 = 0.5   # probability of gain prospect

results = []

for lam in lambda_list:
    try:
        X2 = solve_for_X2_lambda(Y_G, Y_L, X1, p1, lam)
        
        EV = p1 * X1 - (1 - p1) * X2  # expected value (subtract loss)
        EV_rounded_temp = round(EV, 10)
        EV_round = EV_rounded_temp if EV_rounded_temp != 0.0 else 0.0
        
        results.append([lam, X1, X2, EV_round])
    except ValueError as e:
        # for cases where no solution exists
        results.append([lam, X1, None, None])


df = pd.DataFrame(results, columns=['λ', 'X1 (Gain)', 'X2 (Loss)', 'EV'])

print(df)
