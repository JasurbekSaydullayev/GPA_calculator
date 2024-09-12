import requests


def send_post_request(data):
    url = "http://127.0.0.1:8000/gpa/"

    headers = {
        'Content-Type': 'application/json',
    }

    response = requests.post(url, json=data, headers=headers)

    return response.json()


pairs = [
    (93, 4), (71, 6), (67, 6), (69, 8), (89, 4), (70, 2), (77, 6), (86, 2),
    (86, 4), (87, 4), (84, 6), (68, 4), (77, 4), (88, 6), (82, 6), (82, 6),
    (0, 6), (75, 6), (68, 6), (83, 6), (0, 6), (0, 6), (73, 6), (79, 6),
    (80, 2), (69, 6), (80, 6), (87, 4), (65, 6), (85, 6), (90, 2), (78, 4),
    (70, 6), (74, 6), (71, 6), (87, 4), (77, 2)
]

i = 0

for A, B in pairs:
    i += 1
    data = {
        'username': "Jasurbek",
        'key': "123",
        'subject_name': f"Subject{i}",
        'subject_score': f'{A}',
        'subject_credit': f"{B}",
    }

    result = send_post_request(data)
    print(result)
