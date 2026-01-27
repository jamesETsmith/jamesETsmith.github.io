---
title: Paper Speedrun Manifold-Constrained Hyper-Connections
date: 2026-01-21
tags: [deepseek,model architecture, resnet, manifold]
excerpt: Quick summary of the mHC paper to help me learn about it.
draft: true
---

## Sources
1. Manifold-Constrained Hyper-Connections paper from DeepSeek team: [https://www.arxiv.org/pdf/2512.24880](https://www.arxiv.org/pdf/2512.24880)
2. Hyper-connections paper from the ByteDance team: [https://arxiv.org/pdf/2409.19606](https://arxiv.org/pdf/2409.19606)
3. ResNet paper: [https://arxiv.org/pdf/1512.03385](https://arxiv.org/pdf/1512.03385)
4. Sinkhorn-Knopp Algorithm: [https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-s.pdf](https://msp.org/pjm/1967/21-2/pjm-v21-n2-p14-s.pdf)
5. Great overview on youtube from Jin-Bin Huang: [https://www.youtube.com/watch?v=jYn_1PpRzxI](https://www.youtube.com/watch?v=jYn_1PpRzxI)

## Speed Run🏃‍♂️

The authors have summarized their adaptation of the Hyper-Connections architecture very nicely in the TOC figure, shown below. This post will follow the story outlined in that figure and walk through each of the subfigures.

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
    - FLOPs don't increase significantly because the residual stream (left side of the diagram) requires significantly fewer operations than the residual connections (right side of the diagram) and the width of the residual stream only increases by the "small" expansion rate of 4.


Increasing the capacity/complexity of the residual connections isn't a new area of research, but the introduction of Hyper-Connections (HC) is interesting for several reasons: 1) it greatly increases the topological complexity without significantly increasing the operational complexity of the residual units, 2) it yielded noticeably better benchmark results for smaller models, 3) but training instability limited the size of models to 27B parameters (for reference DeepSeek-V3 has 671B parameters).



$$ \mathbf{x}_{l+1} = \mathcal{H}_l^{\text{res}} \mathbf{x}_l + \mathcal{H}_l^{\text{post} \top} \mathcal{F}(\mathcal{H}_l^{\text{pre}} \mathbf{x}_l, \mathcal{W}_l) $$

- $ \mathcal{H}_l^{res} \in \mathbb{R}^{nxn}$ is a learnable mapping that mixes features within the residual stream
- $ \mathcal{H}_l^{pre} \in \mathbb{R}^{1xn} $ is a learnable mapping that aggregates features from the nC-dim stream into a C-dim layer input
- $ \mathcal{H}_l^{post} \in \mathbb{R}^{1xn} $ is a learnable mapping that maps the layer output back onto the stream.

Looking at a recursive formula, it's easier to see where the instability from $\mathcal{H}_l^{res}$ can come from:

$$ \mathbf{x}_L = \left( \prod_{i=1}^{L-l} \mathcal{H}_{L-i}^{\text{res}} \right) \mathbf{x}_l + \sum_{i=l}^{L-1} \left( \prod_{j=1}^{L-1-i} \mathcal{H}_{L-j}^{\text{res}} \right) \mathcal{H}_i^{\text{post} \top} \mathcal{F}(\mathcal{H}_i^{\text{pre}} \mathbf{x}_i, \mathcal{W}_i) $$

As we apply $\mathcal{H}^{\text{res}}$ matrices repeatedly, we can amplify or suppress signal from our input and for large network depths this can lead to gradient explosion or vanishing.



### Manifold-Constrained Hyper-Connections

In Manifold-Constrained Hyper-Connections (mHC), the authors restrict the residual connection matrix $\mathcal{H}_l^{res}$ to be a doubly stochastic matrix (i.e. the rows and columns each sum to 1) using the Sinkhorn-Knopp algorithm.
This constraint restores the identity mapping that HC broke and improves the stability of training for large and deep models.
More formally, the double stochasticity has three important consequences:

1. The spectral norm (maximum singular value) of doubly stochastic matrices is bounded by 1, i.e. $\sigma_{max}(\mathcal{H}_l^{res}) \le 1$. This means that the signal gain will not accumulate over many deep layers and this should help mitigate the exploding gradient problem that plagues HC.
2. The set of doubly stochastic matrices is closed under matrix multiplication, meaning that multiplying two doubly stochastic matrices will always yield another doubly stochastic matrix. This means that we'll maintain these desired properties regardless of the network depth.
3. Since the doubly stochastic matrices contain only positive elements, we can view this residual mapping as a diffusion of information across all streams.

!!! implementation "Sinkhorn-Knopp Algorithm"
    1. Make all elements positive via an exponential operator
    2. for 20 iterations: normalize all the rows, then normalize all the columns


<img src="/images/mHC_training_instability.png" alt="mHC training instability illustration" style="max-width:100%; height:auto;" />

In addition to better training stability compared to vanilla HC, mHC outperforms HC and the baseline on most of the benchmarks studied in the paper, although the improvement is relatively modest.
With that said, I haven't looked into the benchmarks more to get a better sense of the spread of performance from other models.
For example, if the distribution of other results is narrow, these results would appear more impressive.

<img src="/images/mHC_benchmarks.png" alt="mHC benchmarks" style="max-width:100%; height:auto;" />


#### Performance improvements
TLDR: Introduces only a 6.7% time overhead when expansion rate is $n=4$.

See [this blog post](https://www.k-a.in/mHC.html) for a detailed breakdown of the performance improvements.
