"""Offline checks for the KServe manifest and the Triton model repository layout. Needs PyYAML."""
import pathlib
import re
import sys

import yaml

here = pathlib.Path(__file__).parent
errors = []

isvc = yaml.safe_load((here / "inference-service.yaml").read_text())
model = isvc["spec"]["predictor"]["model"]
if isvc["kind"] != "InferenceService" or not isvc["apiVersion"].startswith("serving.kserve.io/"):
    errors.append("not a KServe InferenceService")
if not model["storageUri"].startswith(("s3://", "gs://", "pvc://")):
    errors.append("storageUri must be s3://, gs:// or pvc://")
if "limits" not in model["resources"]:
    errors.append("resource limits missing")

pb = (here / "model_repository" / "order-scorer" / "config.pbtxt").read_text()
for needle in ('name: "order-scorer"', 'platform: "onnxruntime_onnx"', "dynamic_batching"):
    if needle not in pb:
        errors.append(f"config.pbtxt lacks {needle}")
if isvc["metadata"]["name"] not in pb:
    errors.append("InferenceService name differs from Triton model name")
if not re.search(r'name: "x".*dims: \[ 3 \]', pb) or not re.search(r'name: "y".*dims: \[ 2 \]', pb):
    errors.append("tensor names/dims differ from ml-serving-onnx model (x:3 -> y:2)")

if errors:
    sys.exit("FAIL: " + "; ".join(errors))
print("ok: KServe manifest and Triton config.pbtxt are consistent")
