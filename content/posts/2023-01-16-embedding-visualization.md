---
title: Embedding Visualization in HTML
date: 2023-01-16
tags: [HTML, Visualization, JavaScript]
excerpt: This post is a collection of different things I've wanted to try embedding in HTML including Compiler Explorer and Jupyterlite.
---

### General

This post is mostly a collection of different things I've wanted to try embedding in HTML and is more of a sandbox than a real post.

### Compiler Explorer

<div class="embed-container">
    <iframe width="100%" height="600px"
        src="https://godbolt.org/e#z:OYLghAFBqd5QCxAYwPYBMCmBRdBLAF1QCcAaPECAMzwBtMA7AQwFtMQByARg9KtQYEAysib0QXACx8BBAKoBnTAAUAHpwAMvAFYTStJg1DIApACYAQuYukl9ZATwDKjdAGFUtAK4sGIM6SuADJ4DJgAcj4ARpjEIJLSAA6oCoRODB7evv6kyamOAiFhkSwxcQm2mPYFDEIETMQEmT5%2BAXaYDul1DQRFEdGx8dIK9Y3N2W2jvaH9pYMJAJS2qF7EyOwc5gDMocjeWADUJltuYsAkhAgsx9gmGgCC27v7mEcnTiPEmKw3d49mOwYey8h2ObgAbh0iMRfg8/gRMCxEgYEW83HsmAoFAcACqw%2B4YrEHACyTAIxDwqiOAHYrA8DgzEhTwWT2H8GQzUgAvTAAfQIBwYvOIqAA7gpecc6fcOQduXyBUK0LQJVL2RyRugQCBIQ4SGC8VtsAd0GSmJKttL1QdEl4orQ8MgQNaSWSKaoIAsDiBBcKxRKIBolr7lQGgyZaRGACJq%2Bkc0nkykQeX830i8WkOV4HmppWeBRen1C9MB4v%2B4N5lW8iCVgs06Wy2Wm%2Bq8gB0XyUxEhNb94oOACoQ/mFrGZRzoy6E%2B7k9mFWn/ZmU4reaHMziDizaCO443vfPxdWy%2BKKyv84fTyqvRGG7uTWa2x3Zz2SwOh5fR7e5QQtSAaLRaBAzbmq2MTAKEnqZkBbauBBG5iCOlouhOcI7gcAD0aEHFQFKuF%2BP4pOS3wsEcZgAGyoIksRkvqJxgsm37agRXysCR5EKJmaAMCMrqJlS5ikSwV6RqhGGNvwxAHDOOYChJxxRgcGhSgcsknPuqqWsp1jWEJN4MqJn7iZJS4HMgbzyYpGmmWCb7qRYJlaZYOkuvpn4cqJKRotZ1wiZhn7IWOem%2BeO1Ixj5jZfAQqwMAcKQfm5mH%2BbK4KoHg6A2hSgievWLqyoZUlzip5lKSpbhqRadkwpY2nZahBkkEZs6plZWxFZZaI2eV9lVY5NUBa5sqatqaBeAKYLWVBJgAKwWBJg5HhKJF2aYk3yWNqnmGYJFmHF/WJf1eFDSso20apg0gK4tA7Y2e0Mv5E6ISh9yhAKLBMOBTmoVOlJgs9pGSPyNwHCwEDSAcoNmAhulA62TLPZ6o7RhwSy0Jwk28H4HBaKQqCcG4Dl2QoKxrK82w8KQBCaEjSwANYgJNGj6Jwkjo5T2OcLwCggAzFOY0jpBwLAMCICgqBInQsTkJQaBi/QcTAFwZhcKQWDgo6mAAGp4JgooAPKURjZN/gixCcxAUSs1EoQNAAnpwZOW8wxDWzrUTaFCdu8NLbCCDrDC0LbvPK4ihjAOIgf4F8nSQpzgeYKoHQjRsZPPVUrMOlExA2x4WCs4mLAe0sVAGMACia9reuMB7MiCCIYjsFI1fyEoais7oSsGEYKD4/oeBRJzkBLBRNQxwAtDrWwHCPmpyaY3UWGYWPtJ0zgQK44x%2BErwQzCUZR6HkaQCOve8pAfDB9DvgxK0vNTdGMngtHo19dFM58DHEV9TEfH89K/czv0shNVjrAkMjVGLNA44w4AcVQAAOUiI8/oHGAMgUyCtWxcEkrgQg9VSYLF4DzLQCwaZ0wZijDgzNSD53pqQDGWNIEcy5uTSmSwBbCyOraAgksIDS0SOLYg4RWAbFgfAxByDUFmHQbwTA%2BBoSpT0PwGuohxANwUU3FQ6hA5t1IKKTOiQC6Mw4GjGhrNIE6xGhwmKVBoFwIQZIJBKCDhoIwRADwMtYgkS2FwPBTDeZENIAgb4WA4gQTIRQqhDNaG8HobYRhBCqakFptQshWxwF0PZj4whoCOBmFSVE9JcS/GQhNukeIQA"></iframe>
</div>

### Jupyterlite

Copy and paste the Python code into the box below to visualize a protein molecule.

```python
%pip install py3Dmol
import py3Dmol
p = py3Dmol.view(query='mmtf:1ycr')
p.setStyle({'cartoon': {'color':'spectrum'}})
p
```

<div class="embed-container">
    <iframe src="https://jupyterlite.github.io/demo/repl/index.html?kernel=python" width="100%"
        height="400px">
    </iframe>
</div>

