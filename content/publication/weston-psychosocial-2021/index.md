---

title: Psychosocial factors associated with preventive pediatric care during the COVID-19
  pandemic
authors:
- Sara J. Weston
- David M. Condon
- Philip A. Fisher
date: '2021-01-01'
publishDate: '2025-08-08T04:41:45.242454Z'
publication_types:
- article-journal
publication: '*Social Science & Medicine*'
doi: 10.1016/j.socscimed.2021.114356
summary: In a survey of 1,875 parents of young children in fall 2020, structural factors such as insurance and household size, and parent traits such as industriousness, were associated with missed well-child visits and flu vaccination.
tags:
- pediatric care
- vaccination
- parent personality
- COVID-19
- machine learning
featured: false
url_pdf: https://pmc.ncbi.nlm.nih.gov/articles/PMC8516410/
url_preregistration: https://osf.io/79hxq/
url_code: https://osf.io/r348d/
url_dataset: ''
url_project: https://osf.io/r348d/
url_poster: ''
url_slides: ''
url_video: ''

---

## Why we asked

Well-child visits and vaccinations are a cornerstone of children's health, and both dropped during the COVID-19 pandemic. Most work on why families skip them has looked at insurance, income, and other structural barriers. We wanted to know whether parents' psychology adds anything once those barriers are accounted for. If it does, it could help clinics reach the families who most need a nudge.

## What we did

We used data from RAPID-EC, a survey of parents of children age five and younger. In fall 2020, 1,875 parents (96% mothers) told us whether they had missed a well-child visit since the pandemic began and whether their child had already had a flu shot. We paired those answers with demographics, child temperament, parent anxiety, depression, loneliness, and stress, and 27 parent personality traits. We used lasso logistic regression with cross-validation and a held-out test set, which guards against overfitting. In other words, we checked how well the model worked on parents it had never seen. The analysis was preregistered.

## What we found

Prediction of missed well-child visits was 62.8% accurate in the test data. That is certainly better than guessing, but not especially impressive. Having fewer children in the household, lower parent depression, and less conservatism were among the strongest correlates of attending. Prediction of flu vaccination was better, at 74.4%. The strongest correlate was whether the child was vaccinated the year before, followed by private insurance and parent education.

Parent psychology was associated with both outcomes above and beyond demographics. More industrious parents were more likely to attend visits and vaccinate. The effects for personality were modest, around a Cohen's d of 0.2, though small differences can compound over years of visits.

## What it means

These data are observational, so we cannot say why industriousness matters. One possibility, which is speculation, is that the system asks a great deal of parents, and clinics could ask less by offering care in the places parents already go. We recommend testing that.
