"""Write model.onnx (y = x @ W + b, 3 -> 2 floats) with a hand-rolled protobuf encoder: no onnx package needed."""
import struct
import sys


def varint(n):
    out = b""
    while True:
        b, n = n & 0x7F, n >> 7
        out += bytes([b | (0x80 if n else 0)])
        if not n:
            return out


def field(num, wire, payload):
    return varint(num << 3 | wire) + payload


def num(n, v): return field(n, 0, varint(v))
def msg(n, b): return field(n, 2, varint(len(b)) + b)
def text(n, s): return msg(n, s.encode())


def tensor(name, dims, values):
    body = b"".join(num(1, d) for d in dims) + num(2, 1)
    body += msg(4, struct.pack(f"<{len(values)}f", *values)) + text(8, name)
    return body


def value_info(name, dims):
    shape = b"".join(msg(1, num(1, d)) for d in dims)
    return text(1, name) + msg(2, msg(1, num(1, 1) + msg(2, shape)))


def node(op, ins, outs):
    return b"".join(text(1, i) for i in ins) + b"".join(text(2, o) for o in outs) + text(3, op.lower()) + text(4, op)


graph = (msg(1, node("MatMul", ["x", "W"], ["xw"])) + msg(1, node("Add", ["xw", "b"], ["y"]))
         + text(2, "linear")
         + msg(5, tensor("W", [3, 2], [1, 0, 0, 1, 1, 1])) + msg(5, tensor("b", [2], [0.5, -0.5]))
         + msg(11, value_info("x", [1, 3])) + msg(12, value_info("y", [1, 2])))
model = num(1, 8) + msg(7, graph) + msg(8, text(1, "") + num(2, 13))

path = sys.argv[1] if len(sys.argv) > 1 else "model.onnx"
open(path, "wb").write(model)
print("wrote", path, len(model), "bytes")
