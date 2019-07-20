# DESCRIPTION
A work sample I did as an evaluation. Thought I'd share for the sake of extra coding samples recruiters might want to see!

Reads orders from the file 'orders.txt' and dependencies from the file 'dependencies.txt'.
Dependencies are orders that require other orders.
The program will then output a diagram to 'output.txt', 
that shows all the base orders and the orders that rely on them.

# INSTRUCTIONS TO RUN 
 In order to run the program, use Python 3 to run the following command:
 python process_work_orders.py

# IMPLEMENTATION DETAILS 
I tried to show off by modularizing the code into nice reusable chunks- though it honestly
would have been easier to read and understand if I didn't, just longer.
I also tried to catch some edge cases such as terminating possible cycles. This might want to be
disabled if the dataset has very complex trees!

