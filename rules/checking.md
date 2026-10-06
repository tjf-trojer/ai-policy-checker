# Checking: the tally, the script, the check by hand

_Last updated: 2026-10-06_

Step 7. A register is finished when it passes.

## Count

Fill the tally from the rows: rules, controls, intentions, owners named and not collective,
evidence named, moments named and not unspecified, not rules, and the not rules filed outside the
policy.

## Run the checker

```bash
python3 scripts/verify.py <register.md> --input <policy.txt>
```

Deliver only a register that passes. The script's own docstring lists its checks and what none
of them can see.

## Without a shell

A Claude project has none. Before you deliver:

1. Confirm the input is in the lexicon's language. If it is not, deliver the refusal line of
   [posture.md](posture.md) and no register.
2. Open each cited line and find the quotation on it, character for character.
3. Confirm every sentence of the input sits in the Register or in Not rules, never in both, that
   no lead-in stands alone, and that every entry outside the Policy text is filed
   `outside the policy` and no entry inside it is.
4. Recount each status and the tally.

Say in your reply that the register was checked by hand, not by the script.
