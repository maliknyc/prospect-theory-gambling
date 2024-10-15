import math
import pandas as pd

def utility(x, gamma):
    if x >= 0:
        # gains
        if gamma == 1:
            return math.log(1 + x)
        else:
            return ((1 + x) ** (1 - gamma) - 1) / (1 - gamma)
    else:
        # losses
        x = -x  
        if gamma == 1:
            return -math.log(1 + x)
        else:
            return -((1 + x) ** (1 - gamma) - 1) / (1 - gamma)

def solve_for_X2_losses(gamma, sure_amount, X1, p1, p2):
    if X1 <= 0 or sure_amount <= 0:
        raise ValueError("Loss amounts must be positive.")
    if p1 + p2 != 1:
        raise ValueError("Probabilities must sum to 1.")

    # compute utility of sure loss
    U_sure = utility(-sure_amount, gamma)
    # compute utility of smaller loss in gamble
    U_X1 = utility(-X1, gamma)
    # set up expected utility 
    U_X2 = (U_sure - p1 * U_X1) / p2
    # invert utility function to solve for X2
    if gamma == 1:
        X2 = math.exp(-U_X2) - 1
    else:
        base = -U_X2 * (1 - gamma) + 1
        if base <= 0:
            raise ValueError("Invalid base; cannot compute loss amount.")
        X2 = (base ** (1 / (1 - gamma))) - 1
    return X2  # X2 is positive, representing the loss amount

# PARAMETERS
gamma_list = [round(0 + 0.1 * i, 1) for i in range(31)]  # gamma from 0.0 to 3.0 in steps of 0.1
sure_amount = 100  # sure loss amount
X1 = 200          # larger loss amount in the gamble
p1 = 0.5         # probability of losing X1
p2 = 1 - p1       # probability of losing X2

results = []

for gamma_value in gamma_list:
    try:
        X2 = solve_for_X2_losses(gamma_value, sure_amount, X1, p1, p2)
        # expected loss (negative value)
        EV = -(p1 * X1 + p2 * X2)
        # risk premium calculation
        RP = round((sure_amount + EV) * 100 / sure_amount, 3)
        results.append([gamma_value, X1, X2, -EV, RP])  # -EV to show expected loss as positive
    except ValueError as e:
        results.append([gamma_value, X1, None, None, None])

pd.set_option('display.max_rows', None)

df = pd.DataFrame(results, columns=['γ', 'X1 (Loss)', 'X2 (Loss)', 'Expected Loss', 'Risk Premium (%)'])

print(df)
