from babyagi_task_executor.schemas import InputSchema
from babyagi_task_executor.utils import get_logger
from litellm import completion
import yaml


logger = get_logger(__name__)

def run(inputs: InputSchema, worker_nodes = None, orchestrator_node = None, flow_run = None, cfg: dict = None):
    logger.info(f"Running with inputs {inputs.objective}")
    logger.info(f"Running with inputs {inputs.task}")

    user_prompt = cfg["inputs"]["user_message_template"].replace("{{task}}", inputs.task).replace("{{objective}}", inputs.objective)

    messages = [
        {"role": "system", "content": cfg["inputs"]["system_message"]},
        {"role": "user", "content": user_prompt}
    ]

    result = completion(
        model=cfg["models"]["ollama"]["model"],
        messages=messages,
        temperature=cfg["models"]["ollama"]["temperature"],
        max_tokens=cfg["models"]["ollama"]["max_tokens"],
        api_base=cfg["models"]["ollama"]["api_base"],
    ).choices[0].message.content

    logger.info(f"Result: {result}")

    return result


if __name__ == "__main__":
    with open("babyagi_task_executor/component.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    inputs = InputSchema(
        task="Weather pattern between year 1900 and 2000?", 
        objective="Write a blog post about the weather in London."
    )

    run(inputs, cfg=cfg)

