Example Outputs
===============

To evaluate the performance of the toolkit, a set of synthetic gait features (manually created data) with a format similar to the output of the Feature Extraction step, including spatiotemporal parameters (e.g., speed) and specific clinical data (e.g., strength), was used for the AI Interpretation stage.

In the diagnosis box, "cerebral palsy, unilateral, with right side affected" was entered to evaluate the system in the presence of pathology. The data was manipulated to simulate an equinus gait condition to test whether it could be recognized by the toolkit; this condition was not mentioned in the diagnosis.

The following shows how the **Quick Summary Prompt** option performed in describing the input. The numerical values were replaced with "X". However, by comparing the outputs with the input data, the performance in describing the input variables was accurate.

We would appreciate it if you test the other embedded prompts on your real cases and share your feedback.

Quick Summary Prompt — Rapid Reasoning Summary
-----------------------------------------------

1. **Pattern**: Right spastic hemiplegic gait with mild equinus at initial contact plus right in‑toeing.

2. **Lead deviation**: Right in‑toeing. The patient's right foot progression angle is internally rotated on average (−X°) versus the left (+X°), a ~X° asymmetry; relative to typical external foot progression of ~X–X°, this is ≈X–X° more internal than expected. Within right spastic hemiplegia, this is most plausibly driven by reduced external tibial torsion on the right (transmalleolar axis X° right vs X° left) together with dynamic internal hip rotation (right hip rotation mean −X°).

3. **Downstream chain**: The internal foot progression shortens the effective foot lever in late stance, reducing push‑off efficiency and contributing to shorter steps and slower walking. Concurrent mild equinus/forefoot initial contact on the right (ankle −X° plantarflexed at X% GC; normative heel‑strike near neutral, quantitative lab reference not provided) aligns with impaired dorsiflexion, further promoting cautious loading and longer double support.

4. **Asymmetry**: Present; right worse. Evidence: right stance X% (≈−X% vs X% reference) vs left X% (≈+X% vs reference), and right in‑toeing vs left out‑toeing as above. These findings are consistent with the right being the hemiplegic side.

5. **Functional consequence**: The patient walks slower and more cautiously than healthy controls (speed X vs X m/s, −X%; stride length X vs X m, −X%; cadence X vs X steps/min, −X%; stride width X vs X m, +X%; double support X% vs X%, +X%), indicating increased energetic cost and a stability‑seeking strategy, with potential elevated trip risk on the right from plantarflexed initial contact and reduced swing‑phase dorsiflexion.
