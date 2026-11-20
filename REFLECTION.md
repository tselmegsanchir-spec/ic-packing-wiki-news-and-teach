# Reflection (after one real execution; details in RUN-LOG.md)

## 1. Which node most often made errors?
The render step (render gate). It produced 4 of the problems in the log: tier-count tiles showing 0, a diagram label that overflowed, a phone header unreadable on a bright background, and a selector in my own check that miscounted after I added the lesson. The extract step had 1 (a wrong count, 83 instead of 82), clean had 1 (the e-mail footer), lint had 1 (2 orphan pages), and my two text checks each raised 1 false alarm. The biggest single error was not in a node: I misunderstood what the reader wanted and built a method deck instead of the daily briefing.

## 2. At which step did I find the problem, and where did I move the check?
- The tier-count bug was found by looking at a screenshot after the render gate said "0 failures". The gate only measured layout, not values. I moved the check earlier and closer to the data: the gate now computes the expected numbers from `items.json` and compares them with the page.
- The wrong count of 83 was found while reading the extract output; I moved ID assignment into the script so it cannot differ by hand.
- The footer with the e-mail address was found by a grep after cleaning; the cleaning step now cuts at the footer and the grep is part of the routine.
- The misread product was found at the human outline, but the outline only showed slide titles of a method deck. I moved the check upstream: the outline step now shows the reader's card headlines, and AGENTS.md describes the reader format.
- The two false alarms in the text checks were found when a failure listed words that were in fact present; I fixed the normalisation instead of loosening the rule.

## 3. Did I change the workflow? Why?
Yes, five changes: (a) a numeric assertion in the render gate, because layout checks pass on wrong numbers; (b) checks at two widths, 390 px and 1280 px, because the phone view broke where the desktop did not; (c) a lesson part before the news, so the page teaches the terms first and the news second, which gives it a clear instructional structure; (d) a consistency gate for the Mongolian version, so translation cannot change a number or a name; (e) a no-Gmail fallback in AGENTS.md (the owner saves each issue as text) so another AI can repeat the run.

## What I would check in advance next time
Run the render gate on the data first and look at one screenshot before trusting a pass; show the owner a sample card, not only headlines, at the outline; and read the original linked articles when they become reachable, because the faithfulness check only compares my text to the newsletter blurb.
