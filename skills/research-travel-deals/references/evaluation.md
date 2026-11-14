# Evaluation

Evaluate research and planning separately. This is a proposed evaluation design; no live cheapest-fare superiority is claimed.

## Frozen evidence tasks

Give an agent a user brief and fixed source responses, without showing expected answers. Include cases with:

1. A lower airfare that loses after access, bags and an overnight hotel.
2. A cheap room invalid for the children's ages, occupancy or bedding.
3. A full-party fare differing from one-passenger price in either direction.
4. Partial initial API results, with a better valid offer arriving on poll.
5. A synthetic sandbox fare, expired offer, cached calendar and source timeout.
6. A ferry/airport bus that does not operate on the chosen date or after arrival.
7. A regional/direct property omitted by the broad discovery channel.
8. A longer allowed stay that reduces total trip cost at a pricing threshold.
9. A package covering transfers that would otherwise be double counted.
10. An unknown mandatory cost or refundable deposit; no free substitution.
11. Cross-currency quotes without a supplied payment/FX basis.
12. No feasible trip under hard constraints; require a supported limitation, not fabricated availability.

Measure hard-constraint failures, invented facts, evidence fidelity, cost arithmetic, correct quote matching, gap disclosure and useful next query. Use the comparison script for arithmetic gates; separately check schedules, occupancy and evidence assertions.

## Contemporaneous live audits

Compare a generic planning prompt, this research skill, and an experienced human using the same brief, tools, research time and date window. Randomize run order or run in parallel to limit fare drift. Archive observations and reprice the pooled finalists in a close common time window. Do not compare an old screenshot to a live checkout.

Track cheapest feasible verified full-trip cash total; completeness of mandatory cost evidence; independent inventory coverage; relevant local/direct discoveries; quote repricing success; hours/API cost; usability; and constraint violations. Define verified regret as `(agent_total - pooled_best_verified_total) / pooled_best_verified_total` only on genuinely comparable feasible bundles. It measures this audit, not the global optimum.

Include family/holiday, long-haul solo, rural stay, island/ferry, rail/open-jaw, flexible destination and restricted-access cases. Use multiple repetitions before reporting superiority. Distinguish discovery leads from reproducible savings.

## Benchmark references

- TravelPlanner separates information gathering and constraint-sensitive planning: https://github.com/OSU-NLP-Group/TravelPlanner and https://proceedings.mlr.press/v235/xie24j.html . Useful for constraint testing; not proof of the cheapest live market offer.
- ATLAS studies constraint-aware collaboration and critique: https://research.google/pubs/atlas-constraints-aware-multi-agent-collaboration-for-real-world-travel-planning/ . Use a critic to request targeted evidence, not merely concatenate specialist answers.

Refresh benchmark documentation before adopting evaluation code. Test with raw prompts/evidence without leaking intended outputs to the agent.
