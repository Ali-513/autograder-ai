# import json
# from ..states import EvaluationState
# from ..prompts.evaluation import (
#     CORRECTNESS_PROMPT,
#     CODE_QUALITY_PROMPT,
#     FEEDBACK_PROMPT,
# )


# def evaluate_correctness(state: EvaluationState, llm):
#     test_results = state.get("test_results", [])
#     passed = sum(1 for tr in test_results if tr.get("passed"))
#     total = len(test_results)

#     if total == 0:
#         total = 1

#     if passed == total:
#         state["correctness"] = {
#             "status": "fully_correct",
#             "confidence": 1.0,
#             "passed": passed,
#             "total": total,
#         }
#         return state

#     if passed == 0:
#         state["correctness"] = {
#             "status": "incorrect",
#             "confidence": 0.0,
#             "passed": passed,
#             "total": total,
#         }
#         return state

#     prompt = CORRECTNESS_PROMPT.format(
#         question=state["question"],
#         code=state["code"],
#         test_results=json.dumps(test_results),
#     )

#     response = llm.generate(prompt)
#     try:
#         parsed = json.loads(response)
#     except Exception:
#         parsed = {"status": "partial", "explanation": "LLM response parse failed"}

#     state["correctness"] = {
#         "status": parsed.get("status", "partial"),
#         "explanation": parsed.get("explanation", ""),
#         "confidence": passed / total,
#         "passed": passed,
#         "total": total,
#     }
#     return state


# def evaluate_code_quality(state: EvaluationState, llm):
#     prompt = CODE_QUALITY_PROMPT.format(
#         question=state["question"],
#         code=state["code"],
#     )

#     response = llm.generate(prompt)
#     try:
#         state["code_quality"] = json.loads(response)
#     except Exception:
#         state["code_quality"] = {
#             "readability": 7,
#             "structure": 7,
#             "best_practices": 7,
#         }

#     return state


# def handle_partial_credit(state: EvaluationState):
#     passed = state["correctness"]["passed"]
#     total = state["correctness"]["total"]

#     score_ratio = passed / total

#     state["partial_credit"] = {
#         "eligible": score_ratio > 0.3,
#         "suggested_score": round(score_ratio * 100, 2),
#         "reason": "Core logic partially correct but fails some cases"
#         if score_ratio < 1
#         else "All cases passed",
#     }
#     return state


# def apply_rubric(state: EvaluationState):
#     if not state.get("rubric"):
#         return state

#     breakdown = {}
#     total_score = 0

#     for criteria, weight in state["rubric"].items():
#         if criteria == "correctness":
#             score = state["partial_credit"]["suggested_score"] * weight / 100
#         else:
#             avg_quality = sum(
#                 state["code_quality"].get(k, 7) for k in ["readability", "structure", "best_practices"]
#             ) / 30
#             score = avg_quality * weight

#         breakdown[criteria] = round(score, 2)
#         total_score += score

#     state["final_score"] = {
#         "total": round(total_score, 2),
#         "breakdown": breakdown,
#     }
#     return state


# def generate_feedback(state: EvaluationState, llm):
#     prompt = FEEDBACK_PROMPT + f"""

# Correctness:
# {state.get("correctness")}

# Code Quality:
# {state.get("code_quality")}

# Partial Credit:
# {state.get("partial_credit")}
# """
#     state["feedback"] = llm.generate(prompt)
#     return state




# import json
# from ..states import EvaluationState
# from ..prompts.evaluation import (
#     CORRECTNESS_PROMPT,
#     CODE_QUALITY_PROMPT,
#     FEEDBACK_PROMPT,
# )


# def evaluate_correctness(state: EvaluationState, llm):
#     """
#     Evaluate correctness of the submission based on test results and optionally use LLM
#     for partial evaluation if some tests passed.
#     """
#     test_results = state.get("test_results", [])
#     passed = sum(1 for tr in test_results if tr.get("passed"))
#     total = len(test_results) or 1  # Avoid division by zero

#     if passed == total:
#         state["correctness"] = {
#             "status": "fully_correct",
#             "confidence": 1.0,
#             "passed": passed,
#             "total": total,
#         }
#         return state

#     if passed == 0:
#         state["correctness"] = {
#             "status": "incorrect",
#             "confidence": 0.0,
#             "passed": passed,
#             "total": total,
#         }
#         return state

#     # Use LLM for partial correctness explanation
#     prompt = CORRECTNESS_PROMPT.format(
#         question=state["question"],
#         code=state.get("code", ""),
#         test_results=json.dumps(test_results),
#     )

#     response = llm.generate(prompt)
#     try:
#         parsed = json.loads(response)
#     except Exception:
#         parsed = {"status": "partial", "explanation": "LLM response parse failed"}

#     state["correctness"] = {
#         "status": parsed.get("status", "partial"),
#         "explanation": parsed.get("explanation", ""),
#         "confidence": passed / total,
#         "passed": passed,
#         "total": total,
#     }
#     return state


# def evaluate_code_quality(state: EvaluationState, llm):
#     """
#     Evaluate code quality using LLM.
#     """
#     prompt = CODE_QUALITY_PROMPT.format(
#         question=state["question"],
#         code=state.get("code", ""),
#     )

#     response = llm.generate(prompt)
#     try:
#         state["code_quality"] = json.loads(response)
#     except Exception:
#         # Provide default reasonable scores if LLM fails
#         state["code_quality"] = {
#             "readability": 7,
#             "structure": 7,
#             "best_practices": 7,
#         }

#     return state


# def handle_partial_credit(state: EvaluationState):
#     """
#     Compute partial credit based on correctness.
#     """
#     passed = state["correctness"].get("passed", 0)
#     total = state["correctness"].get("total", 1)

#     score_ratio = passed / total

#     state["partial_credit"] = {
#         "eligible": score_ratio > 0.3,
#         "suggested_score": round(score_ratio * 100, 2),
#         "reason": "Core logic partially correct but fails some cases"
#         if score_ratio < 1
#         else "All cases passed",
#     }
#     return state


# def apply_rubric(state: EvaluationState):
#     """
#     Apply rubric if provided to calculate final score.
#     """
#     if not state.get("rubric"):
#         return state

#     breakdown = {}
#     total_score = 0

#     for criteria, weight in state["rubric"].items():
#         if criteria == "correctness":
#             score = state["partial_credit"].get("suggested_score", 0) * weight / 100
#         else:
#             avg_quality = sum(
#                 state["code_quality"].get(k, 7) for k in ["readability", "structure", "best_practices"]
#             ) / 30
#             score = avg_quality * weight

#         breakdown[criteria] = round(score, 2)
#         total_score += score

#     state["final_score"] = {
#         "total": round(total_score, 2),
#         "breakdown": breakdown,
#     }
#     return state


# def generate_feedback(state: EvaluationState, llm):
#     """
#     Generate feedback string for the submission using LLM.
#     """
#     prompt = FEEDBACK_PROMPT + f"""

# Correctness:
# {state.get('correctness')}

# Code Quality:
# {state.get('code_quality')}

# Partial Credit:
# {state.get('partial_credit')}
# """
#     try:
#         response = llm.generate(prompt)
#         state["feedback"] = response
#     except Exception:
#         state["feedback"] = "Could not generate feedback."

#     return state





# import json
# from langchain_core.messages import HumanMessage
# from ..states import EvaluationState
# from ..prompts.evaluation import (
#     CORRECTNESS_PROMPT,
#     CODE_QUALITY_PROMPT,
#     FEEDBACK_PROMPT,
# )


# def evaluate_correctness(state: EvaluationState, llm):
#     """
#     Evaluate correctness of the submission based on test results and optionally use LLM
#     for partial evaluation if some tests passed.
#     """
#     test_results = state.get("test_results", [])
#     passed = sum(1 for tr in test_results if tr.get("passed"))
#     total = len(test_results) or 1  # Avoid division by zero

#     if passed == total:
#         state["correctness"] = {
#             "status": "fully_correct",
#             "confidence": 1.0,
#             "passed": passed,
#             "total": total,
#         }
#         return state

#     if passed == 0:
#         state["correctness"] = {
#             "status": "incorrect",
#             "confidence": 0.0,
#             "passed": passed,
#             "total": total,
#         }
#         return state

#     # Use LLM for partial correctness explanation
#     prompt = CORRECTNESS_PROMPT.format(
#         question=state["question"],
#         code=state.get("code", ""),
#         test_results=json.dumps(test_results),
#     )

#     messages = [HumanMessage(content=prompt)]
#     try:
#         response = llm.generate(messages)
#         text_output = response.generations[0][0].text
#         parsed = json.loads(text_output)
#     except Exception:
#         parsed = {"status": "partial", "explanation": "LLM response parse failed"}

#     state["correctness"] = {
#         "status": parsed.get("status", "partial"),
#         "explanation": parsed.get("explanation", ""),
#         "confidence": passed / total,
#         "passed": passed,
#         "total": total,
#     }
#     return state


# def evaluate_code_quality(state: EvaluationState, llm):
#     """
#     Evaluate code quality using LLM.
#     """
#     prompt = CODE_QUALITY_PROMPT.format(
#         question=state["question"],
#         code=state.get("code", ""),
#     )

#     messages = [HumanMessage(content=prompt)]
#     try:
#         response = llm.generate(messages)
#         text_output = response.generations[0][0].text
#         state["code_quality"] = json.loads(text_output)
#     except Exception:
#         # Provide default reasonable scores if LLM fails
#         state["code_quality"] = {
#             "readability": 7,
#             "structure": 7,
#             "best_practices": 7,
#         }

#     return state


# def handle_partial_credit(state: EvaluationState):
#     """
#     Compute partial credit based on correctness.
#     """
#     passed = state["correctness"].get("passed", 0)
#     total = state["correctness"].get("total", 1)

#     score_ratio = passed / total

#     state["partial_credit"] = {
#         "eligible": score_ratio > 0.3,
#         "suggested_score": round(score_ratio * 100, 2),
#         "reason": "Core logic partially correct but fails some cases"
#         if score_ratio < 1
#         else "All cases passed",
#     }
#     return state


# def apply_rubric(state: EvaluationState):
#     """
#     Apply rubric if provided to calculate final score.
#     """
#     if not state.get("rubric"):
#         return state

#     breakdown = {}
#     total_score = 0

#     for criteria, weight in state["rubric"].items():
#         if criteria == "correctness":
#             score = state["partial_credit"].get("suggested_score", 0) * weight / 100
#         else:
#             avg_quality = sum(
#                 state["code_quality"].get(k, 7) for k in ["readability", "structure", "best_practices"]
#             ) / 30
#             score = avg_quality * weight

#         breakdown[criteria] = round(score, 2)
#         total_score += score

#     state["final_score"] = {
#         "total": round(total_score, 2),
#         "breakdown": breakdown,
#     }
#     return state


# def generate_feedback(state: EvaluationState, llm):
#     """
#     Generate feedback string for the submission using LLM.
#     """
#     prompt = FEEDBACK_PROMPT + f"""

# Correctness:
# {state.get('correctness')}

# Code Quality:
# {state.get('code_quality')}

# Partial Credit:
# {state.get('partial_credit')}
# """
#     messages = [HumanMessage(content=prompt)]
#     try:
#         response = llm.generate(messages)
#         text_output = response.generations[0][0].text
#         state["feedback"] = text_output
#     except Exception:
#         state["feedback"] = "Could not generate feedback."

#     return state


import json
from langchain_core.messages import HumanMessage
from ..states import EvaluationState
from ..prompts.evaluation import (
    CORRECTNESS_PROMPT,
    CODE_QUALITY_PROMPT,
    FEEDBACK_PROMPT,
)


def _invoke_llm(llm, prompt: str) -> str:
    """Safe helper to call ChatModel correctly"""
    msg = HumanMessage(content=prompt)
    response = llm.invoke([msg])
    return response.content


def evaluate_correctness(state: EvaluationState, llm):
    test_results = state.get("test_results", [])
    passed = sum(1 for tr in test_results if tr.get("passed"))
    total = len(test_results) or 1

    if passed == total:
        state["correctness"] = {
            "status": "fully_correct",
            "confidence": 1.0,
            "passed": passed,
            "total": total,
        }
        return state

    if passed == 0:
        state["correctness"] = {
            "status": "incorrect",
            "confidence": 0.0,
            "passed": passed,
            "total": total,
        }
        return state

    prompt = CORRECTNESS_PROMPT.format(
        question=state["question"],
        code=state["code"],
        test_results=json.dumps(test_results),
    )

    try:
        text = _invoke_llm(llm, prompt)
        parsed = json.loads(text)
    except Exception as e:
        parsed = {
            "status": "partial",
            "explanation": f"LLM failure: {str(e)}"
        }

    state["correctness"] = {
        "status": parsed.get("status", "partial"),
        "explanation": parsed.get("explanation", ""),
        "confidence": passed / total,
        "passed": passed,
        "total": total,
    }
    return state


def evaluate_code_quality(state: EvaluationState, llm):
    prompt = CODE_QUALITY_PROMPT.format(
        question=state["question"],
        code=state["code"],
    )

    try:
        text = _invoke_llm(llm, prompt)
        state["code_quality"] = json.loads(text)
    except Exception:
        state["code_quality"] = {
            "readability": 7,
            "structure": 7,
            "best_practices": 7,
            "comments": "LLM unavailable"
        }

    return state


def handle_partial_credit(state: EvaluationState):
    passed = state["correctness"]["passed"]
    total = state["correctness"]["total"]

    score_ratio = passed / total

    state["partial_credit"] = {
        "eligible": score_ratio > 0.3,
        "suggested_score": round(score_ratio * 100, 2),
        "reason": (
            "Core logic partially correct but fails some cases"
            if score_ratio < 1 else "All cases passed"
        ),
    }
    return state


def apply_rubric(state: EvaluationState):
    if not state.get("rubric"):
        return state

    breakdown = {}
    total_score = 0

    for criteria, weight in state["rubric"].items():
        if criteria == "correctness":
            score = state["partial_credit"]["suggested_score"] * weight / 100
        else:
            avg_quality = sum(
                state["code_quality"].get(k, 7)
                for k in ["readability", "structure", "best_practices"]
            ) / 30
            score = avg_quality * weight

        breakdown[criteria] = round(score, 2)
        total_score += score

    state["final_score"] = {
        "total": round(total_score, 2),
        "breakdown": breakdown,
    }
    return state


def generate_feedback(state: EvaluationState, llm):
    # Using .format() to inject values into the new structured prompt
    prompt = FEEDBACK_PROMPT.format(
        correctness_analysis=state.get("correctness", "N/A"),
        code_quality_review=state.get("code_quality", "N/A"),
        partial_credit_info=state.get("partial_credit", "N/A")
    )

    try:
        state["feedback"] = _invoke_llm(llm, prompt)
    except Exception as e:
        state["feedback"] = f"Feedback generation failed: {str(e)}"

    return state
