Abstract—Mutation testing is a powerful methodology for
evaluating the quality of tests. As the cost of mutation testing is
usually very expensive, selective mutation testing was proposed to
choose a subset of mutants to represent the whole set of mutants.
To measure the representativeness of the selected mutants, two
measurement metrics (i.e., adequate-test-based metric and nonadequate-based
metric) are widely used. Although for different
projects, the metric values may be different under different
factors (e.g., number of mutants, number of tests, SLOC), existing
work usually use one or both metrics directly with out further
analysis. To date, none of the previous work has systematically
studied how experimental factors would affect the metric values
as well as how the two metrics differ from each other. Therefore,
this paper presents the first study to investigate the association
between the possible experimental factors and the two mutant
selection metrics as well as the comparison between the two
metrics. The experimental results reveal various interesting finds:
(1) ?? factors impact the adequate test based metric most while
?? factors impact the non-adequate test based metric most; (2)
non-adequate test based metric using R^2
is stable for mutant
sampling strategies while non-adequate-test-based metric using
Kendall τ is not; and (3) the value of one metric can be used to
predict the value of the other one.
