from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sentence_transformers.cross_encoder import CrossEncoder

from trulens_eval import Provider
from dotenv import load_dotenv
load_dotenv()


class CustomFeedback(Provider):
    def find_similarity_score(
        self, question: str, statement: str
    ) -> float:

        excel_file = '/Users/bsoni/Desktop/IThelpdesk/ithelpdesk-bot-rag/SOP Questions test result.xlsx'
        df = pd.read_excel(excel_file, dtype={'Actual Response': 'str'})
        filtered_df = df.loc[df['Query'] == question, 'Expected Response']

        if not filtered_df.empty:
            exp_answer = filtered_df.iloc[0]
        else:
            exp_answer = "Value not found."

        expected_responses = [exp_answer]
        actual_responses = [statement]

        all_responses = expected_responses + actual_responses
        vectorizer = TfidfVectorizer()
        tfidf_vectors = vectorizer.fit_transform(all_responses)
        n_expected_responses = len(expected_responses)
        expected_vs_actual_cos_sim = cosine_similarity(
            tfidf_vectors[:n_expected_responses], tfidf_vectors[n_expected_responses:])

        print("--------------------------------------------------")
        print(f"similarity score is:{float(expected_vs_actual_cos_sim[0][0])}")
        print("--------------------------------------------------")

        if not filtered_df.empty:
            df.loc[df['Query'] == question, 'Cosine Similarity Score'] = float(
                expected_vs_actual_cos_sim[0][0])
            df.loc[df['Query'] == question, 'Actual Response'] = statement
            df.to_excel(excel_file, index=False)

        return float(expected_vs_actual_cos_sim[0][0])

    def find_hhem_score(
        self, question: str, statement: str
    ) -> float:

        # Pre-trained cross encoder
        model = CrossEncoder("vectara/hallucination_evaluation_model")

        list_statement = [statement]
        ranks = model.rank(question, list_statement)
        rank = [rank["score"] for rank in ranks]
        print(question, "--------------------------",
              list_statement, "--------", rank)
        return float(rank[0])
