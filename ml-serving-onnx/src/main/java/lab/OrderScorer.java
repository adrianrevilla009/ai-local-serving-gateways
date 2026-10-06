package lab;

import ai.onnxruntime.OnnxTensor;
import ai.onnxruntime.OrtEnvironment;
import ai.onnxruntime.OrtException;
import ai.onnxruntime.OrtSession;

import java.nio.file.Path;
import java.util.Map;

/** Loads an ONNX model once and scores one order feature vector (quantity, unit price, discount). */
public class OrderScorer implements AutoCloseable {
    private final OrtEnvironment env = OrtEnvironment.getEnvironment();
    private final OrtSession session;

    public OrderScorer(Path model) throws OrtException {
        this.session = env.createSession(model.toString(), new OrtSession.SessionOptions());
    }

    public float[] score(float[] features) throws OrtException {
        try (OnnxTensor input = OnnxTensor.createTensor(env, new float[][] {features});
             OrtSession.Result result = session.run(Map.of("x", input))) {
            return ((float[][]) result.get(0).getValue())[0];
        }
    }

    @Override
    public void close() throws OrtException {
        session.close();
    }

    public static void main(String[] args) throws Exception {
        try (OrderScorer scorer = new OrderScorer(Path.of(args.length > 0 ? args[0] : "model.onnx"))) {
            float[] y = scorer.score(new float[] {2f, 3f, 1f});
            System.out.println("y = [" + y[0] + ", " + y[1] + "]");
        }
    }
}
