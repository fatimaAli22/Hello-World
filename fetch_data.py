from bs4 import BeautifulSoup
import requests


def fetch_top_questions(api_key, count=5, answers_count=5):
    base_url = f"https://api.stackexchange.com/2.3/questions"

    question_params = {
        "site": "stackoverflow",
        "key": api_key,
        "sort": "votes",
        "order": "desc",
        "pagesize": count,
        "tagged": "networking",
    }

    answers_params = {
        "site": "stackoverflow",
        "key": api_key,
        "order": "desc",
        "sort": "votes",
        "pagesize": answers_count,
        "filter": "!*SU8CGYZitCB.D*(BDVIficKj7nFMLLDij64nVID)N9aK3GmR9kT4IzT*5iO_1y3iZ)6W.G*",
    }

    try:
        response = requests.get(base_url, params=question_params)
        response.raise_for_status()

        questions = response.json().get("items", [])

        question_data = []
        for question in questions:
            title = question["title"]
            question_id = question["question_id"]

            answers_url = f"{base_url}/{question_id}/answers"

            answers_response = requests.get(answers_url, params=answers_params)
            answers_response.raise_for_status()

            answers_data = answers_response.json().get("items", [])

            # Extract top answers and their score
            top_answers = [(answer["body"], answer["score"]) for answer in answers_data]

            # Sort answers based on score
            top_answers.sort(key=lambda x: x[1], reverse=True)

            # Take top 5 answers if available, otherwise take all available answers
            top_answers = top_answers[: min(answers_count, len(top_answers))]

            # Format answer bodies
            answer_bodies = [answer[0] for answer in top_answers]

            # Append question data
            question_data.append((title, question_id, answer_bodies))

        return question_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

    return None




    top_questions = fetch_top_questions(api_key, count=5)

    if top_questions:
        write_to_files(top_questions)
        print("Questions text have been written to './data/text/questions.txt'")
        print("Answers text have been written to './data/text/answers.txt'")
    else:
        print("Failed to fetch top questions and answers.")
