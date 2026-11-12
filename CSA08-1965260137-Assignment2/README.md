# CSA08-1965260137-Assignment2

**Name:** M Ayaan  **Register Number:** 1965260137  
**Course:** CSA0809 Python Programming — Assignment 2 (CO2: control flow, strings, functions)  
**Python version:** 3.12  
**Libraries:** standard library only (see `requirements.txt`)

## How to run
Run from inside each task folder (Q4 and Q7 write a CSV file next to the script):

| Task | Command | Result note |
|------|---------|-------------|
| Q1 | `cd Q1 && python q1_subsidy.py` | if-elif gives exactly one decision; separate ifs gave two results for 202 of 1604 inputs (units ≤ 100 with a ration card). |
| Q2 | `cd Q2 && python q2_otp.py` | while, for+inner-while and recursion agree; a mis-placed counter wrongly locks the account when blanks are entered. |
| Q3 | `cd Q3 && python q3_vehicle.py` | Matches the expected output; slicing and regex agree on all test inputs. |
| Q4 | `cd Q4 && python q4_string_build.py` | join is fastest at 200,000 lines; += is near-linear in CPython only because of an in-place optimisation. |
| Q5 | `cd Q5 && python q5_functions.py` | Mutable default list is shared across calls; `order=None` fixes it. |
| Q6 | `cd Q6 && python q6_recursion.py` | naive 242785 calls vs memo 26 calls for n=25; n=1000 needs a higher recursion limit or a loop. |
| Q7 | `cd Q7 && python q7_redesign.py` | Redesign of Q6 naive recursion: 29,860,703 calls → 34 additions at n=35. |

Run everything: `./run_all.sh`. Each folder holds `output.txt` (captured console output) in place of screenshots.

> Timings depend on the computer. Re-run the programs on your own machine and update the numbers in the report if they differ.
