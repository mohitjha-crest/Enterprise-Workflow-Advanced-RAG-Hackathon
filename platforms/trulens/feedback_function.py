from trulens_eval import Feedback
from trulens_eval.feedback.provider import OpenAI
from trulens_eval.feedback import Groundedness
from trulens_eval.app import App
from create_custom_feedback import CustomFeedback
import numpy as np
from dotenv import load_dotenv
load_dotenv()


def create_feedback_functions(chat_engine=None, context=None):
    openai = OpenAI()
    openai.endpoint.rpm = 3
    custom_provider = CustomFeedback()
    if chat_engine is not None:
        context = App.select_context(chat_engine)
    grounded = Groundedness(groundedness_provider=OpenAI())

    # Groundedness of the feedback function
    f_groundedness = (
        Feedback(grounded.groundedness_measure_with_cot_reasons,
                 name="Groundedness")
        .on(context.collect())
        .on_output()
        .aggregate(grounded.grounded_statements_aggregator)
    )

    # Question/answer relevance between overall question and answer.
    f_qa_relevance = Feedback(
        openai.relevance, name="Answer Relevance"
    ).on_input_output()

    f_qs_relevance = (
        Feedback(openai.qs_relevance, name="Context Relevance")
        .on_input()
        .on(context)
        .aggregate(np.max)
    )
    f_similarity_score = Feedback(
        custom_provider.find_similarity_score,
        name="Answer similarity Score",
    ).on_input_output()

    f_hhem_score = Feedback(
        custom_provider.find_hhem_score,
        name="HHEM Score",
    ).on_input_output()

    tru_functions = [
        f_groundedness,
        f_qa_relevance,
        f_qs_relevance,
        f_similarity_score,
        f_hhem_score

    ]
    return tru_functions
