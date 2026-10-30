# Local Qwen2.5 model setup with Ollama

This project uses Ollama for local inference. The application expects the
Ollama model name `ashvon-qwen2.5`.

## 1. Prerequisites

- Install Ollama for your operating system.
- Have the Qwen2.5 GGUF file available locally.
- Ensure the GGUF file is a model you are permitted to use and redistribute.

The Modelfile in this folder expects this exact filename:

```text
models/
├── Modelfile
└── qwen2.5-7b-instruct-q4_K_M.gguf
```

If your GGUF filename differs, edit the `FROM` line in `Modelfile` to match.
Do not rename or convert the model unless you know the source model's format
and licensing requirements.

## 2. Import the GGUF into Ollama

Open a terminal and change into this directory:

```bash
cd models
```

Create the Ollama model:

```bash
ollama create ashvon-qwen2.5 -f Modelfile
```

The command imports the local GGUF into Ollama's managed model store. It does
not require downloading the GGUF again.

## 3. Test the model

```bash
ollama run ashvon-qwen2.5
```

Try a short prompt, then exit the interactive session with `/bye`.

You can also check the installed model:

```bash
ollama list
```

## 4. Confirm the Ollama service

Ollama normally runs as a background service. Check that its local API is
reachable at:

```text
http://localhost:11434
```

The Python application will use:

- Chat model: `ashvon-qwen2.5`
- Embedding model: `nomic-embed-text`

## 5. Embedding model note

The Qwen2.5 chat model is not used as the embedding model. This project uses
a separate local embedding model configured by `OLLAMA_EMBEDDING_MODEL`.

For an initially connected setup, obtain the embedding model once:

```bash
ollama pull nomic-embed-text
```

For a fully offline target machine, transfer/import the embedding model into
Ollama on that machine as part of the model handover. The application must not
attempt to pull a model automatically at runtime.

## 6. Offline operation

After Ollama, the Qwen2.5 model, and the embedding model are installed locally,
chat generation and embedding calls run against the local Ollama service.
The website crawl/refresh step requires internet access, but normal chatbot
queries do not need internet once the ChromaDB index has been built.

## 7. Model licensing and packaging

Before including a GGUF in the client submission, verify the upstream model
license and redistribution terms. If redistribution is not permitted, deliver
the Modelfile, exact model identifier, checksum, and instructions for the
client to obtain the model through an authorized channel instead.
