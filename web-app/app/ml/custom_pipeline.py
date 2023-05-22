import pandas as pd
from imblearn.over_sampling import RandomOverSampler
from imblearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelBinarizer

from ml.sentence_transformer_vectorizer import CustomSentenceTransformer


class CustomPipeline(Pipeline):

    def __init__(self, steps):
        super().__init__(steps)
        self.label_binarizer = LabelBinarizer()

    def fit(self, X, y=None, **fit_params):
        new_y = self.label_binarizer.fit_transform(y)
        super().fit(X, new_y, **fit_params)

    def format_predict(self, X, **predict_params):
        predictions = super().predict_proba(X, **predict_params)
        temp_result = {}
        for i, label in enumerate(predictions):
            label_name = self.label_binarizer.classes_[i]
            label_probas = []
            for probas in label:
                label_probas.append(probas[-1])
            temp_result[label_name] = label_probas

        result = []
        for i in range(len(X)):
            final_prediction = {}
            for label_name, prediction_probas in temp_result.items():
                final_prediction[label_name] = prediction_probas[i]
            result.append(final_prediction)

        return result


if __name__ == "__main__":
    train_data = [
        ("falar com atendente", "atendente"),
        ("falar com pessoa", "atendente"),
        ("estou sem sinal", "funcionamento_nulo"),
        ("quero agendar manutenção", "agendar_vt"),
        ("Me manda a segunda via", "segunda_via"),
        ("já paguei, libera sinal", "promessa"),
        ("nao quero falar com robo", "atendente"),
        ("meu sinal ta falhando", "funcionamento_nulo"),
        ("como agendar manutenção", "agendar_vt"),
        ("quero a segunda via", "segunda_via"),
        ("libera sinal, vou pagar agora", "promessa"),
    ]

    train_df = pd.DataFrame(train_data)
    train_df.columns = ["text", "label"]

    train_x, train_y = train_df["text"], train_df["label"]

    pipeline = CustomPipeline(
        [
            ("vect", CustomSentenceTransformer()),
            ("smt", RandomOverSampler(random_state=42)),
            ("clf", MultiOutputClassifier(MLPClassifier(random_state=42, alpha=0.1))),
        ]
    )

    pipeline.fit(train_x, train_y)
    # como usar:
    pipeline.format_predict(["Qero 2a via"])
