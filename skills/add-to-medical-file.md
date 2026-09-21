---


name: add-to-medical-file

uuid: 32d24dc8-ccd9-81b8-ad99-fc50c420112c

version: 7

description: "Add to Medical File"

thinking: "High"

temperature: 0.2


---


# Add to Medical File

Every check-in gets logged — minor or major, resolved or ongoing. This builds the full complaint history that future Dr. Alder sessions, preventative plans, and consult reports draw from. Log the record as a new row in Section 9 (Complaint Log) of the patient's health file.

## Steps

Copy these steps verbatim into the task list before starting. A skipped step stays in the list marked `skip: <reason>` — never dropped silently.

1. **Retrieve the T-LICC summary** from the current session. If called outside of a `/medical-checkin`, ask the patient to describe the complaint and complete a brief T-LICC intake before proceeding.

1. **Confirm the record before writing.** Present the proposed log entry and ask for confirmation or corrections. The entry must include:

  - Date

  - Chief complaint (1 sentence)

  - T-LICC summary (compact: 1 line per dimension, or omit N/A dimensions)

  - Action taken (home remedies, medication used, rest, etc.)

  - Outcome (resolved / ongoing / referred / unknown at time of logging)

1. **Write the record** to Section 9 (Complaint Log) of the patient's health file. (The target health file is supplied at invocation — defaults to @Richard-Health-File if patient context is Richard. Resolve handle location via @global-instructions.) Append — never overwrite existing entries.

1. **Flag if follow-up is pending.** If the complaint was referred to a GP or is ongoing, note it clearly.

## Examples

- After a `/medical-checkin` about a headache: Dr. Alder presents the log entry, Richard confirms, row is appended: `| 2026-03-25 | Dull bilateral headache | T: 1 day; L: behind eyes; I: 4/10; C: pressure; C: worse in afternoon | Hydration, rest, nasal rinse | Resolved next day |`

- Called standalone: Dr. Alder asks for a brief T-LICC summary, confirms the record, appends.

## Boundaries

- Never overwrite existing complaint log entries — append only

- Never log without patient confirmation of the record

- Never omit the date, complaint, or action taken — these three fields are mandatory

- Never log vague entries — ask for detail if insufficient

## Output

- **Format:** Table row in markdown

- **Target:** Section 9 (Complaint Log) of the patient's personal health file

- **On completion:** Confirm the log entry was written and show the final row

## Next steps

1. Present the proposed log entry

1. Confirm with patient

1. Append to health file