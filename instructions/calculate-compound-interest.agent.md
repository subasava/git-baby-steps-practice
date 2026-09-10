# Calculate Compound Interest

Use this instruction when the user asks to calculate compound interest for a principal amount, annual rate, compounding frequency, and investment duration.

When to use the tool:
- The user wants the final amount after compound interest is applied.
- The user wants the total interest earned over a period of time.
- The user provides principal, annual rate, compounding frequency, and years as inputs.

Tool to use:
- `compound_interest.py`

How to invoke it:
- Run:
  `python compound_interest.py <principal> <annual_rate> <compounds_per_year> <total_years>`
- Example:
  `python compound_interest.py 15847 7.34 12 8.583333`

Input notes:
- `principal` is the starting amount.
- `annual_rate` can be entered as a percentage like `7.34` or as a decimal like `0.0734`.
- `compounds_per_year` is the number of compounding periods per year, such as `12` for monthly.
- `total_years` is the full duration in years; for 8 years and 7 months, use `8.583333`.

How to present results:
- Report the final amount and total interest earned.
- Format amounts in dollars with two decimal places.
- Include the command used and the output values when helpful.
- Keep the response concise and clear.
