import random

OPERATIONS = {"addition": ("Addition", "+", "On rassemble les nombres", "peach"), "multiplication": ("Multiplication", "×", "On compte plus vite", "lavender"), "soustraction": ("Soustraction", "−", "On apprend à retirer", "mint"), "division": ("Division", "÷", "On partage équitablement", "yellow")}

def generate_questions(operation, table):
    questions = []
    holes = ["left", "right", "result"] * 3 + [random.choice(["left", "right", "result"])]
    random.shuffle(holes)
    for index, number in enumerate(random.sample(range(1, 11), 10)):
        if operation == "addition":
            left, right, result = number, table, number + table
        elif operation == "soustraction":
            left, right, result = number + table, table, number
        elif operation == "multiplication":
            left, right, result = number, table, number * table
        else:
            left, right, result = number * table, table, number
        hole = holes[index]
        # Keep the selected table visible in commutative missing-term questions.
        if operation in ("addition", "multiplication") and hole == "right":
            left, right = right, left
        question = {"left": left, "right": right, "result": result, "hole": hole}
        question["answer"] = question[hole]
        questions.append(question)
    return questions
