# Task: personal-identifier check

60 short lines from health, banking, logistics and support settings, written for this receipt. 28 are labelled YES (contain a direct personal identifier) and 32 NO. The labels and the prompt were committed and pinned by SHA-256 before the harness or any model run existed.

This is a toy task. It exists so the receipt has a checkable number to carry, not to rank models. I wrote both the lines and the labels, so the score measures agreement with my reading.

Judgement calls a reasonable reader could label the other way:
- `p24` "Card ending 4417 belongs to the customer": labelled NO, four card digits alone do not single a person out.
- `p55` "The building at 100 Main Street hosts our regional office": labelled NO, a business address.
- `p59` "Note from Gareth": labelled YES, a first name counts as a partial personal name under the prompt's definition.

Cheap baselines reported next to the model: always answering the majority class (NO, 32/60), and a regular-expression rule written without looking at model output.
