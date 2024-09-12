from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
knowledge0 = And(
    Or(AKnight, AKnave),                # A must be either a knight or a knave
    Not(And(AKnight, AKnave)),          # A cannot be both
    Implication(AKnight, And(AKnight, AKnave))  # If A is a knight, A's statement must be true
)

# Puzzle 1
knowledge1 = And(
    Or(AKnight, AKnave),                # A must be either a knight or a knave
    Or(BKnight, BKnave),                # B must be either a knight or a knave
    Not(And(AKnight, AKnave)),          # A cannot be both
    Not(And(BKnight, BKnave)),          # B cannot be both
    Implication(AKnight, And(AKnave, BKnave)),  # If A is a knight, A's statement must be true
    Implication(AKnave, Not(And(AKnave, BKnave)))  # If A is a knave, A's statement must be false
)

# Puzzle 2
knowledge2 = And(
    Or(AKnight, AKnave),                # A must be either a knight or a knave
    Or(BKnight, BKnave),                # B must be either a knight or a knave
    Not(And(AKnight, AKnave)),          # A cannot be both
    Not(And(BKnight, BKnave)),          # B cannot be both
    Implication(AKnight, Biconditional(AKnight, BKnight)),  # If A is a knight, A's statement must be true
    Implication(AKnave, Not(Biconditional(AKnight, BKnight))),  # If A is a knave, A's statement must be false
    Implication(BKnight, Not(Biconditional(AKnight, BKnight))),  # If B is a knight, B's statement must be true
    Implication(BKnave, Biconditional(AKnight, BKnight))    # If B is a knave, B's statement must be false
)

# Puzzle 3
knowledge3 = And(
    Or(AKnight, AKnave),                # A must be either a knight or a knave
    Or(BKnight, BKnave),                # B must be either a knight or a knave
    Or(CKnight, CKnave),                # C must be either a knight or a knave
    Not(And(AKnight, AKnave)),          # A cannot be both
    Not(And(BKnight, BKnave)),          # B cannot be both
    Not(And(CKnight, CKnave)),          # C cannot be both
    
    # B's statement: "A said 'I am a knave'."
    Implication(BKnight, Biconditional(AKnave, AKnight)),
    Implication(BKnave, Not(Biconditional(AKnave, AKnight))),
    
    # B's second statement: "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C's statement: "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")

if __name__ == "__main__":
    main()

