# Task: does a clinical note ask for an action?

60 one-line clinical notes, written for this receipt, 27 labelled YES (the note asks the care team to do something not yet done, conditional plans included) and 33 NO (done already, a decision not to act, an observation, or a patient or family wish with no clinician plan). Committed and pinned by SHA-256 before the keyword baseline or any model run on it.

This task was chosen because a keyword rule should struggle on it: many NO lines contain action words in the past tense or under a negation ("Amoxicillin was started yesterday", "No need to repeat the chest X-ray"), and several YES lines carry no obvious verb ("Needs an echocardiogram as an outpatient"). I wrote the lines knowing that, so the gap between the model and the keyword rule partly measures how I wrote them. The numbers are agreement with my labels, not clinical accuracy.

Judgement calls a reasonable reader could label the other way:
- `c05` "Patient asked whether she could stop her statin; discussed, she will continue it": NO, the outcome is no change.
- `c29` "I would not stop the beta blocker at this stage": NO, a decision not to act.
- `c37` "He should not drive until reviewed...; please give the written advice": YES, it asks staff to hand over advice.
- `c45` "Safe for discharge today with a district nurse visit on Thursday": YES, it sets up a discharge and a visit.
