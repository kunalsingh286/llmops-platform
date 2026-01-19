import json
import mlflow
from backend.app.llm.ollama_llama import OllamaLlamaProvider
from backend.app.datasets.versioning import dataset_hash

DATASET_PATH = "evaluation/offline/sample_dataset.json"
PROMPT_NAME = "qa"

def load_dataset():
    with open(DATASET_PATH) as f:
        return json.load(f)

def simple_success_metric(response: str, expected: str) -> int:
    return int(any(word.lower() in response.lower() for word in expected.split()))

def run_evaluation():
    dataset = load_dataset()
    dataset_version = dataset_hash(dataset)

    llm = OllamaLlamaProvider()

    mlflow.set_experiment("offline_prompt_evaluation")

    with mlflow.start_run():
        successes = []

        for sample in dataset:
            full_prompt = f"You are a precise assistant.\nUser: {sample['input']}"
            response = llm.generate(full_prompt)

            success = simple_success_metric(response, sample["expected"])
            successes.append(success)

        accuracy = sum(successes) / len(successes)

        mlflow.log_param("prompt_name", PROMPT_NAME)
        mlflow.log_param("dataset_version", dataset_version)
        mlflow.log_metric("accuracy", accuracy)

        print(f"Offline Evaluation Accuracy: {accuracy:.2f}")

if __name__ == "__main__":
    run_evaluation()
