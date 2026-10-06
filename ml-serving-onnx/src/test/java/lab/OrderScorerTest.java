package lab;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class OrderScorerTest {
    @Test
    void matchesHandComputedLinearModel() throws Exception {
        // x = [2,3,1], W = [[1,0],[0,1],[1,1]], b = [0.5,-0.5] -> [3.5, 3.5]
        try (OrderScorer scorer = new OrderScorer(Path.of("model.onnx"))) {
            assertArrayEquals(new float[] {3.5f, 3.5f}, scorer.score(new float[] {2f, 3f, 1f}), 1e-5f);
        }
    }
}
