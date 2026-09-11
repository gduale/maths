import random

OPERATIONS = {"addition": ("Addition", "+", "On rassemble les nombres", "peach"), "multiplication": ("Multiplication", "×", "On compte plus vite", "lavender"), "soustraction": ("Soustraction", "−", "On apprend à retirer", "mint"), "division": ("Division", "÷", "On partage équitablement", "yellow")}

CATEGORIES = {
    "add_sub": ("Addition et soustraction", "+ −", "On ajoute et on retire", "peach"),
    "mul_div": ("Multiplication et division", "× ÷", "On multiplie et on partage", "lavender"),
}
CATEGORY_OPERATIONS = {
    "add_sub": ("addition", "soustraction"),
    "mul_div": ("multiplication", "division"),
}
LEGACY_CATEGORIES = {operation: category for category, operations in CATEGORY_OPERATIONS.items() for operation in operations}

def category_for(operation):
    return LEGACY_CATEGORIES.get(operation, operation)

def operation_details(operation):
    return CATEGORIES.get(operation) or OPERATIONS[operation]

def generate_questions(operation, table):
    questions = []
    operations = list(CATEGORY_OPERATIONS[category_for(operation)]) * 5
    random.shuffle(operations)
    holes = ["left", "right", "result"] * 3 + [random.choice(["left", "right", "result"])]
    random.shuffle(holes)
    for index, number in enumerate(random.sample(range(1, 11), 10)):
        operation = operations[index]
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
        question = {"left": left, "right": right, "result": result, "hole": hole, "operation": operation}
        question["answer"] = question[hole]
        questions.append(question)
    return questions
