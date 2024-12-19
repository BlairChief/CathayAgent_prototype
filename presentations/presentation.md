---
marp: true
title: Deep Residual Learning for Image Recognition
paginate: true
theme: uncover
---

# Deep Residual Learning for Image Recognition

Presented by: [Your Name]

---

## Introduction

- Deep Learning has revolutionized the field of image recognition.
- Traditional deep neural networks face challenges as they become deeper.
- **ResNet** or Residual Network is introduced by Kaiming He et al. to address these challenges.

---

## What is Deep Residual Learning?

- Residual Learning aims to solve degradation problems associated with deep networks.
- They allow layers to fit a residual mapping instead of directly attempting to fit the desired underlying mapping.

---

## ResNet Architecture

- **Skip Connections**: Core innovation allowing layers to skip one or more other layers.
- Skip connections help gradient flow easily during backpropagation.
- Layers can now learn residual functions instead of unreferenced functions.

---

## Mathematical Formulation

- Let the original mapping be $\mathcal{H}(x)$.
- We let the stacked layers fit $F(x) = \mathcal{H}(x) - x$.
- The original function becomes $\mathcal{H}(x) = F(x) + x$.

---

## Key Innovations

- **Ease of Optimization**: Simpler learning objectives improve convergence.
- **Reduced Training Error**: Model generalizes well to unseen data.
- **Network Depth**: Allows building deeper networks with improved performance.
  
---

## Performance Benchmarks

- ResNet architectures such as ResNet-50, ResNet-101, have demonstrated better accuracy on ImageNet datasets.
- They won the ImageNet Large Scale Visual Recognition Challenge 2015.

---

## Applications of ResNet

- Image Classification
- Object Detection
- Semantic Segmentation
- Used in autonomous systems, medical imaging analysis, etc.

---

## Visual Representation

![ResNet Architecture](https://miro.medium.com/max/1400/1*LgYPwDiIVX40O9DJ4HiY_A.png)

*Image Source: Medium.com*

---

## Python Implementation Example

```python
import torch
import torch.nn as nn

class BasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.relu(out)
        out = self.conv2(out)
        out += residual
        out = self.relu(out)
        return out
```

---

## Conclusion

- The introduction of ResNets has been pivotal in advancing deep learning architectures.
- Their robustness and efficiency make them ideal for a variety of image recognition tasks.
- ResNet's innovations continue to influence modern architectures in deep learning research.

---

## References

1. Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun, *"Deep Residual Learning for Image Recognition"*, 2015.
2. Ian Goodfellow et al., *"Deep Learning"*, MIT Press, 2016.
3. Blogs and tutorials on Medium, Coursera, and other platforms providing insights on ResNets.

---