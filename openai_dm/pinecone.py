import itertools
import torch


def upload_embeddings_to_index(index, embeddings, batch_size=100):
    upsert_gen = batch_generator(embeddings, batch_size)
    counter = 0
    for vectors in upsert_gen:
        print(counter * batch_size)
        index.upsert(vectors=vectors)
        counter += 1


def batch_generator(iterable, batch_size=100):
    """A helper function to break an iterable into chunks of size batch_size."""
    it = iter(iterable)
    batch = tuple(itertools.islice(it, batch_size))
    while batch:
        yield batch
        batch = tuple(itertools.islice(it, batch_size))


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[
        0
    ]  # First element of model_output contains all token embeddings
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def create_embeddings(
    doc_list,
    tokenizer,
    embedding_model,
    additional_metadata,
    max_length=300,
    overlap=20,
):
    embeddings = []
    for i, doc in enumerate(doc_list):
        tokens = tokenizer(
            [doc], padding=False, truncation=False, max_length=4096, return_tensors="pt"
        )
        seq_length = tokens["input_ids"].shape[1]
        start_idx = 0
        end_idx = min(seq_length, max_length) + 1

        chunk_counter = 0
        while start_idx <= seq_length:
            id = f"doc_{i}_chunk_{chunk_counter}"
            model_input = {
                k: v[0][start_idx:end_idx].unsqueeze(0) for k, v in tokens.items()
            }
            with torch.no_grad():
                try:
                    model_output = embedding_model(**model_input)
                except IndexError:
                    print(id)
                    # error = model_input
                    start_idx = end_idx - overlap
                    end_idx = start_idx + max_length + 1
                    chunk_counter += 1
                    continue

            sentence_embeddings = mean_pooling(
                model_output, model_input["attention_mask"]
            )

            embedding_dict = {
                "id": id,
                "values": sentence_embeddings[0].tolist(),
                "metadata": {
                    "text": tokenizer.convert_tokens_to_string(
                        tokenizer.convert_ids_to_tokens(
                            model_input["input_ids"][0].tolist()
                        )
                    ),
                    "embedding_model": embedding_model,
                },
            }
            embedding_dict["metadata"].update(additional_metadata)
            embeddings.append(embedding_dict)

            start_idx = end_idx - overlap
            end_idx = start_idx + max_length + 1
            chunk_counter += 1


if __name__ == "__main__":
    pass
