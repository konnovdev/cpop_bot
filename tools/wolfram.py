import wolframalpha

from config import WOLFRAMALPHA_API

client = wolframalpha.Client(WOLFRAMALPHA_API)


def get_wolfram_result(question: str):
    res = client.query(question)
    if res.success is False and res.error == "false":
        return "Nothing was found for <b>" + question + "</b>."\
            "\nPlease try a different query."
    answer = ""
    for pod in res.pods:
        pod_title = pod.title + ":\n"
        subpod_text = ""
        for sub in pod.subpods:
            if sub.plaintext is not None:
                subpod_text += f"{str(sub.plaintext)}\n"

        if subpod_text:
            answer += f"{pod_title}{subpod_text}\n"
    return answer
