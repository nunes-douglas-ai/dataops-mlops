import os.path
import pickle

import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import Pipeline

from configs.app_configs import AppSettings
from ml.sentence_transformer_vectorizer import CustomSentenceTransformer
from utils.logger import app_logger as logger
from utils.version import __version__

CVS_QTY = 10

VECTORIZERS = [
    CustomSentenceTransformer()
]

CLASSIFIERS = [
    RandomForestClassifier(random_state=42)
]


def make_pipeline(vectorizer, classifier):
    logger.info("Creating pipeline...")
    text_pipe_clf = Pipeline(
        [
            ('vect', vectorizer),
            ('clf', classifier)
        ]
    )
    logger.info("Pipeline created %s", text_pipe_clf)
    return text_pipe_clf


def eval_pipeline(pipeline, X, y):
    logger.info("Starting evaluation")
    y_pred = cross_val_predict(pipeline, X, y, cv=CVS_QTY)
    metrics = classification_report(y, y_pred, output_dict=True)
    logger.info("Final metrics %s", metrics)
    return metrics, y_pred


def train_pipeline(pipeline, X, y):
    logger.info("Starting training")
    trained_model = pipeline.fit(X, y)
    logger.info("Training finished")
    return trained_model


def train_eval_without_mlflow(pipeline, X, y):
    logger.info("Training without MlFlow")
    trained_model = train_pipeline(pipeline, X, y)
    return trained_model


def mlflow_log_testing_metrics(pipeline, X, y):
    metrics, y_pred = eval_pipeline(pipeline, X, y)
    prefix = "testing"
    flatten_metrics = {}
    for key1, value1 in metrics.items():
        if isinstance(value1, dict):
            for key2, value2 in value1.items():
                new_key = f"{prefix}_{key1}_{key2}"
                flatten_metrics[new_key] = value2
        else:
            flatten_metrics[key1] = value1
    mlflow.log_metrics(flatten_metrics)
    mlflow.log_param("test-cvs-qty", CVS_QTY)
    test_cm = ConfusionMatrixDisplay.from_predictions(y, y_pred)
    mlflow.log_figure(test_cm.figure_, 'testing_confusion_matrix.png')


def train_eval_with_mlflow(app_settings, pipeline, X, y):
    logger.info("Training with MlFlow")
    mlflow.set_tracking_uri(app_settings.mlflow_host)
    mlflow.set_experiment(app_settings.mlflow_experiment)

    with mlflow.start_run():
        mlflow.log_param("app-version", __version__)

        mlflow.sklearn.autolog(disable=True)
        mlflow_log_testing_metrics(pipeline, X, y)

        mlflow.sklearn.autolog(disable=False)
        trained_model = train_pipeline(pipeline, X, y)
        mlflow.log_param("full-pipeline", str(trained_model))


def save_model(trained_model, app_settings):
    models_path = os.path.basename(app_settings.models_path)
    model_file_name = app_settings.model_file_name
    model_file_path = os.path.join(models_path, model_file_name)

    with open(model_file_path, 'wb') as f:
        pickle.dump(trained_model, f)


if __name__ == "__main__":
    logger.info("Starting Training")
    app_settings = AppSettings()

    annotated_df = pd.read_csv(app_settings.train_file)

    X = annotated_df[app_settings.text_col]
    y = annotated_df[app_settings.label_col]

    for vectorizer in VECTORIZERS:
        for classifier in CLASSIFIERS:
            try:
                ml_pipeline = make_pipeline(vectorizer, classifier)

                if app_settings.enable_mlflow:
                    train_eval_with_mlflow(app_settings, ml_pipeline, X, y)
                else:
                    trained_model = train_eval_without_mlflow(ml_pipeline, X, y)
                    save_model(trained_model, app_settings)
            except Exception as exc:
                logger.error("Exception trying to train with %s and %s", vectorizer, classifier, exc_info=exc)
