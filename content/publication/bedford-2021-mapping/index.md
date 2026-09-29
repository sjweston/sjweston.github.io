---
title: 'Mapping individual differences on the internet: Case study of the type 1 diabetes
  community'
authors:
- Cianna Bedford-Petersen
- Sara J Weston
- ' others'
date: '2021-01-01'
publishDate: '2025-08-08T04:41:45.236503Z'
publication_types:
- article-journal
publication: '*JMIR Diabetes*'
doi: "10.2196/30756"
summary: 'We used natural language processing on nearly 700,000 tweets from the type 1 diabetes community to find its main topics, and network analysis to see whether accounts sit in topic-specific echo chambers.'
tags:
- type 1 diabetes
- social media
- topic modeling
- natural language processing
- social network analysis
featured: false
url_pdf: /publication/bedford-2021-mapping/paper.pdf
url_preregistration: 'https://osf.io/w67yb'
url_code: 'https://osf.io/h7fq4/'
url_dataset: 'https://osf.io/h7fq4/'
image: 
  caption: 'Network of the 100 most-followed accounts in the type 1 diabetes tweet sample. Each node is an account, colored by its dominant topic in a 6-topic Latent Dirichlet Allocation model; edges are follows.'
  focal_point: ""
  preview_only: false
---

## Why we asked

People with type 1 diabetes (T1D), their caregivers, and clinicians talk to each other on Twitter, and earlier work suggests that this online community offers emotional support and practical advice. Most of that work reads and codes posts by hand, which is slow and cannot keep up with millions of posts. We wanted to know whether topic modeling could show us what the community talks about, and whether people in it hear about a mix of topics or mostly their own.

## What we did

We collected 691,691 tweets from 8,557 accounts, posted between 2008 and 2020, starting from T1D hashtags and expanding to the followers of those accounts. We kept all of an account's recent tweets, not only the diabetes ones, so we could see the rest of people's lives too. First, we scored the sentiment of each account's tweets. Second, we fit Latent Dirichlet Allocation (LDA) topic models. LDA finds clusters of words that tend to appear together, and each cluster is a topic. We chose six topics because that number balanced model fit against topics we could interpret. A 30-topic model fit better, but we could not make sense of it. Third, we mapped who follows whom among the 100 most-followed accounts and colored each account by its dominant topic. We preregistered the analyses.

## What we found

Tweets were slightly positive on average (Cohen's d = 0.32), which is a small difference from neutral. The six topics were insulin prices, clinical research, day-to-day blood sugar management, technology such as closed-loop insulin systems, awareness and fundraising, and positive emotion and life outside diabetes. Daily management was the most common, at 23% of words, followed by the insulin price crisis at 19%.

In the network, the colors were mixed together rather than sorted into clusters. In other words, even the most-followed accounts see a range of topics in their feeds instead of an echo of their own.

## What it means

Twitter users are not representative of everyone with T1D, and LDA ignores word order, so we treat these as descriptions of one online community. The approach is cheap and can be pointed at other health communities by changing the hashtags. Twitter does not allow sharing tweet text, so our OSF page holds tweet and user IDs and the code.
