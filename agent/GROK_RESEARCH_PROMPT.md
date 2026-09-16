# Paste to Grok Bot (agent1 Research / Analysis / Hypothesis)

Enable skill **`casmi26-grok-research`**, connect GitHub, then send:

---

Run `/casmi26-grok-research` for the next CASMI competition-day cycle on
`ilakkmanoharan/casmi26-structure-prediction`.

Do agent1 steps 1–3 only:

1. Web + paper research → `Research/YYYY-MM-DD_cycleNN_methods.md`
2. Prior submission logs/scores → `Analysis/YYYY-MM-DD_cycleNN_submission.md`
3. Hypotheses → `Hypothesis analysis/YYYY-MM-DD_cycleNN_hypotheses.md`

Also write `Specs/YYYY-MM-DD_cycleNN_next_submission_spec.md` with one
`config_patch` using existing `casmi26/config.py` constants only.

Commit and push those folders, then:
`python3 scripts/casmi_loop/check_and_dispatch.py --dispatch`

Never print secrets. If quota is already 5/5 for the Chicago day, stop after a status note.

---

## Suggested routine

> Every 90 minutes between 01:00 and 10:00 America/Chicago, if submissions
> today &lt; 5 and no casmi-loop run is in progress: run casmi26-grok-research
> for the next cycle, push docs, dispatch casmi-loop. Otherwise post status only.
