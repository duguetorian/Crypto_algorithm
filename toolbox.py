from math import floor, ceil, sqrt


def isGen(p, g):
    """
    Tests if g is a generator of F_p*, prints intermediate calculations 
    and the conclusion
    """

    intermediate_result = 1
    print(f"{g}^0 mod {p} = {intermediate_result}")
    found = [True] * 2 + [False] * (p - 2)

    for i in range(1, p - 1):
        intermediate_result = (intermediate_result * g) % p
        found[intermediate_result] = True
        print(f"{g}^{i} mod {p} = {intermediate_result}")

    if all(found):
        print(f"{g} est donc bien générateur de F_{p}*")
    else:
        print(f"{g} n'est donc pas générateur de F_{p}*")

# isGen(167, 5)

def divInFp(a, b, p):
    """
    returns a/b dans F_p
    """
    if b % p == 0:
        return "inf"

    potentialResults = [
        a/b, 
        (a - p) / b, 
        (a + p) / b, 
        a / (b + p), 
        a / (b - p)
    ]

    for result in potentialResults:
        if result == floor(result):
            return result

    return 0


def PplusQ(P, Q, a, p):
    """
    Caculates P + Q where P and Q are two points of the eliptic curb
    {(x,y), y^2 = x^3 + a * x + b} in F_p
    """
    x_p, y_p = P
    x_q, y_q = Q

    s = 0

    if  x_p == x_q and y_p == y_q:
        s = divInFp(3 * x_p**2 + a, 2 * y_p, p)
    else:
        s = divInFp(y_q - y_p, x_q - x_p, p)

    if s == "inf":
        return ["inf", "inf"]

    t = y_p - s * x_p

    x_PplusQ = s**2 - x_p - x_q
    y_PplusQ = -s * x_PplusQ -t

    # The floor is juste to convert float to int
    return [floor(x_PplusQ) % p, floor(y_PplusQ) % p] 


def succesiveMultiples(P, a, p):
    """
    Calculates and prints the successives multiples of point P 
    in the Eliptic curb {(x,y), y^2 = x^3 + a * x + b} in F_p
    """
    print(f"[1]P = {P}")

    intermediateResult = P
    i = 1

    while intermediateResult[0] != "inf":
        i += 1
        intermediateResult = PplusQ(intermediateResult, P, a, p)
        print(f"[{i}]P = {intermediateResult}")


# succesiveMultiples([0, 1], 2, 5)

def BSGS(g, y, p):
    """
    Applies BSGS to find x solution of g^x = y mod p,
    prints intermediate calculations and conclusion
    """
    m = ceil(sqrt(p - 1))

    print("Baby steps:")
    print(f"{g}^0 = 1 mod {p}")
    intermediateResult = 1
    babySteps = [1]

    for j in range(1, m):
        intermediateResult = intermediateResult * g % p
        babySteps.append(intermediateResult)
        print(f"{g}^{j} = {intermediateResult} mod {p}")

    print("\n\nGiant steps:")
    b = floor(g**(p - 1 - m)) % p

    print(f"{y} x {b}^0 = {y} mod {p}")
    intermediateResult = y

    for i in range(1, m):
        intermediateResult = intermediateResult * b % p
        print(f"{y} x {b}^{i} = {intermediateResult} mod {p}")

        try:
            j = babySteps.index(intermediateResult)
            print(f"\n\nOn a donc : x = {i} x {m} + {j} = {i * m + j}")
            break
        except:
            pass

# BSGS(3, 57, 113)
