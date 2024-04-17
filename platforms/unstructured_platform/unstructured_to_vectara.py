from unstructured.ingest.connector.local import SimpleLocalConfig
from unstructured.ingest.connector.vectara import (
    SimpleVectaraConfig,
    VectaraAccessConfig,
    WriteConfig,
)
from unstructured.ingest.interfaces import (
    PartitionConfig,
    ProcessorConfig,
    ReadConfig,
    ChunkingConfig
)
from unstructured.ingest.runner import LocalRunner
from unstructured.ingest.runner.writers.base_writer import Writer
from unstructured.ingest.runner.writers.vectara import (
    VectaraWriter,
)
from dotenv import load_dotenv
import os

load_dotenv()

VECTARA_CLIENT_ID = os.environ.get("VECTARA_CLIENT_ID")
VECTARA_SECRET = os.environ.get("VECTARA_SECRET")
VECTARA_CUSTOMER_ID = os.environ.get("VECTARA_CUSTOMER_ID")
VECTARA_CORUPS_NAME = os.environ.get("VECTARA_CORUPS_NAME")
OUTPUT_DIR = "data/chunked_data"
INPUT_DIR = "data/testing/SOPs/"
MAX_CHAR = 2500

def get_writer() -> Writer:
    return VectaraWriter(
        connector_config=SimpleVectaraConfig(
            access_config=VectaraAccessConfig(
                oauth_client_id=VECTARA_CLIENT_ID,
                oauth_secret=VECTARA_SECRET
            ),
            customer_id=VECTARA_CUSTOMER_ID,
            corpus_name=VECTARA_CORUPS_NAME
        ),
        write_config=WriteConfig(),
    )


if __name__ == "__main__":
    writer = get_writer()
    runner = LocalRunner(
        processor_config=ProcessorConfig(
            verbose=True,
            output_dir=OUTPUT_DIR,
            num_processes=2,
        ),
        connector_config=SimpleLocalConfig(
            input_path=INPUT_DIR,
        ),
        read_config=ReadConfig(),
        partition_config=PartitionConfig(strategy='auto'),
        chunking_config=ChunkingConfig(
            chunk_elements=True, chunking_strategy="by_title", max_characters=MAX_CHAR),
        writer=writer,
        writer_kwargs={},
    )
    runner.run()
