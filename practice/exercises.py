import random

OPERATIONS = {"addition": ("Addition", "+", "On rassemble les nombres", "peach"), "multiplication": ("Multiplication", "×", "On compte plus vite", "lavender"), "soustraction": ("Soustraction", "−", "On apprend à retirer", "mint"), "division": ("Division", "÷", "On partage équitablement", "yellow")}

def generate_questions(operation, table):
    questions = []
    swapped_positions = set(random.sample(range(10), 5))
    for index, number in enumerate(random.sample(range(1, 11), 10)):
        if operation == "addition":
            left, right, result = number, table, number + table
        elif operation == "soustraction":
            left, right, result = number + table, table, number
        elif operation == "multiplication":
            left, right, result = number, table, number * table
        else:
            left, right, result = number * table, table, number
        # Keep the selected table visible: addition/subtraction train +/- table.
        # Commutative operations allow the missing term on either side.
        if operation in ("addition", "multiplication") and index in swapped_positions:
            left, right = right, left
            hole = "right"
        else:
            hole = "left"
        questions.append({"left": left, "right": right, "result": result, "hole": hole, "answer": left if hole == "left" else right})
    # In subtraction/division, alternate the position while retaining the table relationship.
    if operation in ("soustraction", "division"):
        for question in random.sample(questions, 5):
            question["hole"] = "right"
            question["answer"] = question["right"]
    return questions
