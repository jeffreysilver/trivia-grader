# trivia-grader
helper to grade quarantine trivia more accurately and efficiently. outputs each teams score, and their wrong answers. all wrong answers will be reviewed to calculate the actual score for a team


## Usage
- Update the sample `answers.json` file with the correct answers to each round 
- `python grader.py --round ROUND`
- Copy and paste the responses from a round into responses.csv. Here's an example of the form that we use: [https://docs.google.com/forms/d/1WHiZ4Me8GSjVDjilt5EHQ7Lh8YitVVLYcsAGnuDfScI](https://docs.google.com/forms/d/1WHiZ4Me8GSjVDjilt5EHQ7Lh8YitVVLYcsAGnuDfScI/edit)
- Follow the CLI prompts to grade a round
