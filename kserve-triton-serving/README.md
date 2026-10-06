# kserve-triton-serving

A KServe `InferenceService` (`inference-service.yaml`), a Triton model config (`model_repository/order-scorer/config.pbtxt`) and `validate.py`, which cross-checks them.

## Goal

Show how the ONNX scorer from `ml-serving-onnx` would be served on Kubernetes through KServe with the Triton runtime, and catch mismatches between the manifest and the Triton config before deploying.

## Run it

```
pip install pyyaml
python3 validate.py
```

Expected: `ok: KServe manifest and Triton config.pbtxt are consistent`.

Not run end to end: there is no cluster here. The manifest was never applied, no Triton server was started, and `model.onnx` is not placed in the model repository (Triton expects it as `order-scorer/1/model.onnx`, which you upload to the `storageUri` bucket).

## What it proves

- `inference-service.yaml` is a `serving.kserve.io/v1beta1` InferenceService in `RawDeployment` mode, with the `kserve-tritonserver` runtime, 1 to 3 replicas scaled at 70% CPU, and requests plus limits set.
- `config.pbtxt` declares the `onnxruntime_onnx` platform, input `x` (3 floats), output `y` (2 floats), `max_batch_size: 8` and dynamic batching with a 1 ms queue delay.
- `validate.py` fails if the service name differs from the Triton model name, if `storageUri` is not `s3://`, `gs://` or `pvc://`, or if the tensor shapes drift from the Java model.

## Trade-offs

- `s3://models/order-scorer` is an example path; you must supply the bucket and credentials.
- Raw deployment mode skips Knative, so there is no scale to zero.
- The validation is text and YAML matching, not a Triton or KServe schema check.

## When not to use it

- For one service that owns its model, in-process inference (`ml-serving-onnx`) is simpler.
- On a cluster without KServe installed; the manifest will not apply.
