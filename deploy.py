import boto3
import logging
import time
import sys
cloudformation = boto3.client("cloudformation")
s3 = boto3.client("s3")
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
sh.setFormatter(formatter)
logger.addHandler(sh)


def load_code():
    s3.put_object(
        Bucket="cta-bus-and-train-tracker", 
        Key="config/backend.zip",
        Body=open("deploy.zip", "rb")
    )


def check_stack_status(stack_name: str) -> str:
    stacks = cloudformation.list_stacks(
        StackStatusFilter=[
            "CREATE_IN_PROGRESS",
            "CREATE_FAILED",
            "CREATE_COMPLETE",
            "ROLLBACK_IN_PROGRESS",
            "ROLLBACK_FAILED",
            "ROLLBACK_COMPLETE",
            "DELETE_IN_PROGRESS",
            "DELETE_FAILED",
            "UPDATE_IN_PROGRESS",
            "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS",
            "UPDATE_COMPLETE",
            "UPDATE_FAILED",
            "UPDATE_ROLLBACK_IN_PROGRESS",
            "UPDATE_ROLLBACK_FAILED",
            "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS",
            "UPDATE_ROLLBACK_COMPLETE",
            "REVIEW_IN_PROGRESS",
            "IMPORT_IN_PROGRESS",
            "IMPORT_COMPLETE",
            "IMPORT_ROLLBACK_IN_PROGRESS",
            "IMPORT_ROLLBACK_FAILED",
            "IMPORT_ROLLBACK_COMPLETE",
        ]
    )["StackSummaries"]
    for stack in stacks:
        if stack["StackName"] == stack_name:
            return stack["StackStatus"]


def build_stack(stack: str) -> None:
    if check_stack_status(stack) is not None:
        logging.error("Stack already exists")
        raise ValueError("Stack already exists")

    start = time.time()
    cloudformation.create_stack(
        StackName=stack,
        TemplateBody=open("template.yaml").read(),
        OnFailure="DELETE",
        Capabilities=["CAPABILITY_IAM"],
    )

    while check_stack_status(stack) == "CREATE_IN_PROGRESS":
        logging.debug("Waiting for stack")
        time.sleep(5)

    final_status = check_stack_status(stack)
    if final_status != "CREATE_COMPLETE":
        logging.error(f"The formation completed with status: {final_status}.")
        raise ValueError(f"The formation completed with status: {final_status}.")
    logging.info(
        f"Stack creation took {round(time.time() - start, 2)} seconds to complete"
    )



def main():
    # load_code()
    build_stack("web-test")


if __name__ == '__main__':
    main()