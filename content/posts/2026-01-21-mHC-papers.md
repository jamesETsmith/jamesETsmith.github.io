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

Generalizing to a network with a shallow ($l$) and deep ($L$) portion:

$$ \mathbf{x}_L = \mathbf{x}_l + \sum_{i=l}^{L-1} \mathcal{F}(\mathbf{x}_i, \mathcal{W}_i) $$

### Hyper-Connections

!!! key-points
    - FLOPs don't increase significantly because they only increases the expansion rate by "small" factors like 4.


Increasing the capacity/complexity of the residual connections isn't a new area of research, but the introduction of hyper-connections is interesting for several reasons: 1) it greatly increases the topological complexity without significantly increasing the operational complexity of the residual units, 2) it yielded noticeably better benchmark results for smaller models, 3) but training instability limited the size of models to 27B parameters (for reference DeepSeek-V3 has 671B parameters).



$$ \mathbf{x}_{l+1} = \mathcal{H}_l^{\text{res}} \mathbf{x}_l + \mathcal{H}_l^{\text{post} \top} \mathcal{F}(\mathcal{H}_l^{\text{pre}} \mathbf{x}_l, \mathcal{W}_l) $$

- $ \mathcal{H}_l^{res} \in \mathbb{R}^{nxn}$ is a learnable mapping that mixes features within the residual stream
- $ \mathcal{H}_l^{pre} \in \mathbb{R}^{1xn} $ is a learnable mapping that aggregates features from the nC-dim stream into a C-dim layer input
- $ \mathcal{H}_l^{post} \in \mathbb{R}^{1xn} $ is a learnable mapping that maps the layer output back onto the stream.

Looking at a recursive formula, it's easier to see where the instability from $\mathcal{H}_l^{res}$ can come from:

$$ \mathbf{x}_L = \left( \prod_{i=1}^{L-l} \mathcal{H}_{L-i}^{\text{res}} \right) \mathbf{x}_l + \sum_{i=l}^{L-1} \left( \prod_{j=1}^{L-1-i} \mathcal{H}_{L-j}^{\text{res}} \right) \mathcal{H}_i^{\text{post} \top} \mathcal{F}(\mathcal{H}_i^{\text{pre}} \mathbf{x}_i, \mathcal{W}_i) $$

As we apply the different $ \mathcal{H} $ matrices repeatedly, we can amplify or suppress signal from our input and for large network depths this can lead to gradient explosion or vanishing.

> Why does't it add to the FLOPs by a noticeable amount for each computer unit?




### Manifold-Constrained Hyper-Connections

In Manifold-Constrained Hyper-Connections (mHC), the authors project $\mathcal{H}$ 


<img src="/images/mHC_training_instability.png" alt="mHC training instability illustration" style="max-width:100%; height:auto;" />


!!! implementation Sinkhorn-Knopp Algorithm
    Here's an implementation of the sinkhorn-knopp algorithm

- Introduces only a 6.7% time overhead when exapansion rate is $n=4$.