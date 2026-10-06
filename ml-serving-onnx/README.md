# ml-serving-onnx

A Java 21 class `OrderScorer` that runs an ONNX model with ONNX Runtime, a Python script that writes the model, and a JUnit test.

## Goal

Run ONNX inference inside a plain Java process: no model server and no Python at request time. The model is a tiny linear layer, `y = x @ W + b`, over three order features (quantity, unit price, discount).

## Run it

```
python3 make_model.py
mvn -B test
```

Expected: `make_model.py` prints `wrote model.onnx 167 bytes`, and Maven reports `OrderScorerTest` with one passing test. Both were run here.

## What it proves

- `make_model.py` writes a valid ONNX file with a hand-written protobuf encoder, so the `onnx` Python package is not needed.
- `OrderScorer.java` creates the session once and `score()` runs a `[1,3]` float tensor through it, returning two floats.
- `OrderScorerTest` checks that `[2, 3, 1]` gives `[3.5, 3.5]`, which matches the hand calculation with `W = [[1,0],[0,1],[1,1]]` and `b = [0.5, -0.5]`.

## Trade-offs

- The model runs in the application's JVM and memory, with no separate scaling or versioning.
- The ONNX Runtime native library (version 1.20.0) is bundled in the dependency and makes the artifact bigger.
- `model.onnx` is git-ignored; the test needs `make_model.py` to run first.

## When not to use it

- When several services share one model or it needs independent scaling, use a model server (see `kserve-triton-serving`).
- For large models that need a GPU: the session here uses default CPU options.
