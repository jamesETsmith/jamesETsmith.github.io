---
title: Paper Speedrun Manifold-Constrained Hyper-Connections
date: 2026-01-21
tags: [deepseek,model architecture, resnet]
excerpt: Quick summary of the mHC paper to help me learn about it.
---

## Sources
- Original paper from DeepSeek team: [https://www.arxiv.org/pdf/2512.24880](https://www.arxiv.org/pdf/2512.24880)
- Hyper-connections paper from the ByteDance team: [https://arxiv.org/pdf/2409.19606](https://arxiv.org/pdf/2409.19606)
- ResNet paper: [https://arxiv.org/pdf/1512.03385](https://arxiv.org/pdf/1512.03385)
- Sinkhorn-Knopp Algorithm: [https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-s.pdf](https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-s.pdf)
- Great overiew on youtube from Jin-Bin Huang: [https://www.youtube.com/watch?v=jYn_1PpRzxI](https://www.youtube.com/watch?v=jYn_1PpRzxI)

## Speed Run🏃‍♂️

The authors have summarized their adaptation of the Hyper-Connections architecture very nicely in the TOC figure, shown below. This post will be follow the story outlined in that figure and walk through each of the subfigures.

<img src="/images/mHC_overview.png" alt="mHC paper overview" style="max-width:100%; height:auto;" />

### Residual Connection

$$ x_{l+1} = x_l + \mathcal{F}(x_l, W_l) $$

This architecture means that deep networks will maintain signal from the input at an arbitrary depth.
[He et al](https://arxiv.org/pdf/1603.05027) showed that this "identity mapping" property maintains stability and efficiency during large scale training.
Note that residual connections are a key design element used in LLMs although they tend to look more complicated in practice.

### Hyper-Connections

Increasing the capacity/complexity of the residual connections isn't a new area of research, but the introduction of hyper-connections is interesting for several reasons: 1) it greatly increases the topological complexity without significantly increasing the operational complexity of the residual units, 2) it yielded noticeably better benchmark results for smaller models, 3) but training instability limited the size of models to 27B parameters (for reference DeepSeek-V3 has 671B parameters).






### Manifold-Constrained


<img src="/images/mHC_training_instability.png" alt="mHC training instability illustration" style="max-width:100%; height:auto;" />


!!! implementation Sinkhorn-Knopp Algorithm
    Here's an implementation of the sinkhorn-knopp algorithm

Here's a new paragraph