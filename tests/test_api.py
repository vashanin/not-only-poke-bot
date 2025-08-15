import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


@pytest.mark.parametrize(
    "endpoint,params,expected_output",
    [
        ("/api/v1/battle", {"pokemon1": "Pikachu", "pokemon2": "Bulbasaur"}, "Pikachu or Bulbasaur"),
    ],
)
def test_battle_question(endpoint, params, expected_output):
    correctness_metric = GEval(
        name="Correctness",
        criteria="Determine if the 'actual output' is correct based on the 'expected output'.",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        threshold=0.6,
    )

    response = client.get(endpoint, params=params).json()

    test_case = LLMTestCase(
        input=f"Who would win a battle between {params['pokemon1']} and {params['pokemon2']}?",
        actual_output=response["winner"],
        expected_output=expected_output,
    )

    assert_test(test_case, [correctness_metric])


@pytest.mark.parametrize(
    "endpoint,params,expected_output",
    [
        (
            "/api/v1/chat",
            {"question": "What are the base stats of Charizard?"},
            "A JSON (dictionary) structure, which includes stats of the hp, attack, defense, special attack, "
            "special defense, and speed.",
        ),
        (
            "/api/v1/chat",
            {"question": "What is the weather in Kyiv right now?"},
            "A JSON (dictionary) structure, which includes weather, temperature, humidity, and wind info in Kyiv.",
        ),
        (
            "/api/v1/chat",
            {"question": "What is the capital of Germany?"},
            "A JSON (dictionary) structure, with answer that the capital of Germany is Berlin.",
        ),
    ],
)
def test_chat_questions(endpoint, params, expected_output):
    correctness_metric = GEval(
        name="Correctness",
        criteria="Determine if the 'actual output' is correct based on the 'expected output'.",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        threshold=0.6,
    )

    response = client.post(endpoint, json=params).json()
    print("test_chat_questions", response, flush=True)

    test_case = LLMTestCase(
        input=params["question"],
        actual_output=str(response),
        expected_output=expected_output,
    )

    assert_test(test_case, [correctness_metric])
