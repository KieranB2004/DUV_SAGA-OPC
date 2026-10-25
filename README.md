# 193 nm DUV Optical Proximity Correction

## Project Goal

Develop a Python simulator for simplified 193 nm DUV
lithography and investigate machine-learning-based OPC
using a surrogate-assisted genetic algorithm.

## Scope

- Import rectangular target geometry from KLayout GDSII.
- Simulate the aerial image using two-dimensional FFTs.
- Estimate the printed pattern using an intensity threshold.
- Optimize geometric mask corrections.
- Compare a direct genetic algorithm with a
  Gaussian-process surrogate-assisted genetic algorithm.
- Visualize the target, candidate mask, predicted print,
  and optimization progress.

## Limitations

- Scalar optical model.
- Simplified threshold-printing model.
- No measured wafer data.

## Validation

- Test each numerical component independently.
- Check physical and numerical consistency.
- Record configuration and random seeds.
