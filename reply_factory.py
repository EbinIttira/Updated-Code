
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []
    mark=0

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if not current_question_id:
        return False, "No current question available."


    question_list = PYTHON_QUESTION_LIST  
    if current_question_id < 0 or current_question_id >= len(question_list):
        return False, "Invalid question ID."

    question = question_list[current_question_id]
    # expected_answer = question.get("answer")  
    # print(expected_answer)
    options = question.get("options", [])  
    

    if answer not in options:
        return False, "Invalid answer selected. Please choose from the available options."


    if "answers" not in session:
        session["answers"] = {}

    session["answers"][current_question_id] = answer
    session.save()

    return True, ""  



def get_next_question(current_question_id):

    question_list = PYTHON_QUESTION_LIST  
    if current_question_id < 0 or current_question_id >= len(question_list) - 1:
        return None, -1

    next_question_id = current_question_id + 1
    next_question = question_list[next_question_id]["question_text"]
    print(next_question)
    return next_question, next_question_id


def generate_final_response(session):
    answers = session.get("answers", {})
    print(answers)
    score = 0


    for question_id, answer in answers.items():
        question = PYTHON_QUESTION_LIST[question_id]
        if question and question.get("answer") == answer:
            score += 1

    final_response = f"Your final score is {score} out of {len(PYTHON_QUESTION_LIST)}."
    return final_response
