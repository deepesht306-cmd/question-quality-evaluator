CACHE = {}
import time
LAST_CALL_TIME = 0
COOLDOWN_SECONDS = 3
use_llm = True 

def greet():
    print("Hello, Welcome to Question Evaluator!!")
    print("\nNote: This evaluates question structure, not intelligence.\n")


def length_score(question):
    words = question.split()
    count = len(words)

    if count < 5:
        return 2
    elif count <= 12:
        return 5
    else:
        return 8


def keyword_score(question):
    keywords = ["why", "how", "explain", "compare", "what"]
    question = question.lower()

    for word in keywords:
        if word in question:
            return 8
    return 4


def context_score(question):
    context_words = ["beginner", "student", "example", "simple", "college"]
    question = question.lower()

    count = 0
    for word in context_words:
        if word in question:
            count += 1

    if count == 0:
        return 3
    elif count == 1:
        return 6
    else:
        return 9


def generate_suggestion(question):
    suggestions = []

    if length_score(question) <= 4:
        suggestions.append("Try adding a bit more detail to your question.")

    if keyword_score(question) <= 4:
        suggestions.append("Consider using words like 'how', 'why', or 'explain'.")

    if context_score(question) <= 3:
        suggestions.append("Add context like your level (student/beginner) or ask for examples.")

    if not suggestions:
        return "Your question is already clear and well structured."

    return " ".join(suggestions)


def llm_evaluate_question(question):
    from openai import OpenAI
    client = OpenAI()

    evaluation_prompt = f"""
You are an assistant that evaluates the quality of a user's question.
Evaluate only the question structure, not the intelligence of the user.

Rate the question on:
- Clarity (1-10)
- Specificity (1-10)
- Depth (1-10)

Provide one short constructive suggestion.

Return strictly in this format:
Clarity: X/10
Specificity: X/10
Depth: X/10
Suggestion: <one sentence>

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You evaluate question quality."},
            {"role": "user", "content": evaluation_prompt}
        ]
    )

    return response.choices[0].message.content


def quality_label(score):
    if score >= 8:
        return "Excellent"
    elif score >= 6:
        return "Good"
    elif score >= 4:
        return "Fair"
    else:
        return "Needs improvement"


def extract_llm_suggestion(llm_text):
    for line in llm_text.splitlines():
        if line.lower().startswith("suggestion"):
            return line.split(":", 1)[1].strip()
    return None


def show_user_report(final_score, suggestion):
    label = quality_label(final_score)

    print("Question Quality Summary")
    print("------------------------")
    print(f"Overall Quality: {label} ({final_score}/10)\n")

    print("How to improve:")
    print(f"• {suggestion}\n")

    print("Note: This evaluates question structure, not intelligence.")


def rate_question(question):

    if len(question.strip()) < 5:
        return {
            "score": 0.0,
            "label": "Needs improvement",
            "suggestion": "Please enter a more complete question for useful feedback."
        }

    if len(question) > 500:
        warning = "Your question is quite long. Consider shortening it."
    else:
        warning = None

    # Rule-based scoring
    l = length_score(question)
    k = keyword_score(question)
    c = context_score(question)
    final_score = round((l + k + c) / 3, 1)

    # LLM gate
    use_llm = 4.5 <= final_score < 8.5

    llm_suggestion = None
    if use_llm:
        if question in CACHE:
            llm_suggestion = CACHE[question]
        else:
            try:
                llm_text = llm_evaluate_question(question)
                llm_suggestion = extract_llm_suggestion(llm_text)
                CACHE[question] = llm_suggestion
            except Exception:
                llm_suggestion = None

    final_suggestion = llm_suggestion or generate_suggestion(question)

    if warning:
        final_suggestion = warning + " " + final_suggestion

    return {
        "score": final_score,
        "label": quality_label(final_score),
        "suggestion": final_suggestion
    }



def main():
    greet()
    question = input("Enter your question: ")
    rate_question(question)


# def run_tests():
#     questions = get_test_questions()
#     for q in questions:
#         print("\nQ:", q)
#         rate_question(q)


# def get_test_questions():
#     return [
#         # Very weak
#         "AI?",
#         "help",

#         # Weak
#         "What is AI",
#         "Explain ML",

#         # Medium
#         "What is AI and how is it used?",
#         "Explain neural networks for beginners",

#         # Strong
#         "What is AI and how is it used in daily life for a college student? Give examples.",
#         "Compare supervised and unsupervised learning with real-world examples.",

#         # Very strong
#         "As a biology student, how can I use AI in research? Explain with two examples and limitations.",
#         "How does overfitting occur in small datasets, and how can regularization help? Explain simply.",

#         # Garbage / invalid
#         "kbfoagcvoiiyil pg[hdv"
#     ]


# run_tests()


if __name__ == "__main__":
    main()



