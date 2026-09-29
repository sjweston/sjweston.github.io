---
title: 'BrainAGE as a measure of maturation during early adolescence'
authors:
- Lucy B Whitmore
- Sara J Weston
- Kathryn L Mills
date: '2023-01-01'
publishDate: '2023-01-01T00:00:00Z'
publication_types:
- article-journal
publication: '*Imaging Neuroscience*'
abstract: |
  The Brain-Age Gap Estimation (BrainAGE) is an important new tool that purports to evaluate brain
  maturity when used in adolescent populations. However, it is unclear whether BrainAGE tracks with
  other maturational metrics in adolescence. In the current study, we related BrainAGE to metrics of
  pubertal and cognitive development using both a previously validated model and a novel model trained
  specifically on an early adolescent population. The previously validated model was used to predict
  BrainAGE in two age bands, 9-11 and 10-13 years old, while the novel model was used with 9-11 year
  olds only. Across both models and age bands, an older BrainAGE was related to more advanced pubertal
  development. The relationship between BrainAGE and cognition was less clear, with conflicting
  relationships across the two models. Additionally, longitudinal analysis revealed moderate to high
  stability in BrainAGE across early adolescence. The results of the current study provide initial
  evidence that BrainAGE tracks with some metrics of maturation, including pubertal development.
  However, the conflicting results between BrainAGE and cognition lead us to question the utility of
  these models for non-biological processes.
summary: 'We tested whether BrainAGE, an MRI-based estimate of how mature a brain looks, tracks puberty and cognition in about 11,000 children aged 9 to 13. It was associated with pubertal development, but its association with cognition was unclear.'
tags:
- brain development
- BrainAGE
- puberty
- adolescence
- neuroimaging
featured: false
url_pdf: https://pmc.ncbi.nlm.nih.gov/articles/PMC12007541/
url_code: https://github.com/LucyWhitmore/BrainAGE-Maturation
url_dataset: https://doi.org/10.15154/1523041
url_preregistration: ''
url_project: ''
url_slides: ''
url_poster: ''
url_video: ''
---

## Why we asked

Brain scans can be used to guess a person's age. BrainAGE is the gap between that guess and the person's actual age, so a child whose scan looks like a 12-year-old's at age 10 has an older BrainAGE. In older adults, an older-looking brain goes along with conditions like Alzheimer's disease. In adolescents, researchers have often read the gap as a sign of faster or slower brain maturation, and some have linked it to mental health. It was unclear whether the gap tracks other things that mature during adolescence, and that question matters before anyone treats it as a measure of brain maturity.

## What we did

We used structural MRI from the Adolescent Brain Cognitive Development (ABCD) Study. The baseline sample had 11,402 children aged 9 to 11, and the two-year follow-up had 7,696 children aged 10 to 13. We estimated BrainAGE with an existing model trained on ages 9 to 19, and we trained two new models on early adolescents from ABCD itself. We then asked how BrainAGE relates to puberty (reported by the child and by a parent) and to a composite score from the NIH Toolbox cognition battery. We also asked how stable BrainAGE is from one visit to the next.

## What we found

Older BrainAGE was associated with more advanced pubertal development, whether the child or the parent reported it, in both age bands and with all the models. In other words, children who looked further along in puberty also tended to have brains that looked older. With the existing model, the association was stronger at the follow-up visit than at baseline. Cognition was less clear. With the existing model, older BrainAGE went with slightly lower cognition scores, and with our new model the direction reversed. BrainAGE was moderately to highly stable across the two visits, and more stable when the same model produced both estimates.

## What it means

This is initial evidence that BrainAGE tracks some markers of maturation. We do not know what to make of the cognition results, and composite scores may hide differences among specific abilities. Because brain maturity has come up in legal and policy debates, we urge researchers to be careful about what they claim BrainAGE shows. Our new models and code are available for others to use.

BrainAGE tracks puberty, and what else it tracks is still open.
