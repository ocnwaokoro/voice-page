# Rules (read at the start of every milestone)

1. Milestones strictly in order; at most 3 builders.
2. Done = named tests pass + a real audio round-trip observed with a number. Evidence in voice-page-work/evidence/Mx/.
3. Owner talks to it after every ticket that changes behaviour, not only at milestone end.
4. Every status claim carries proof I actually saw; say what is unchecked.
5. After every merge, check main CI is green. Same red twice: find the root cause, don't rerun.
6. One batch PR per milestone for walk findings. `Closes #n` repeated per issue.
7. Heavy model tests run locally (`make verify-local`), output pasted in the PR. CI stays under 3 minutes.
8. Never commit the saved reference page or any third-party branding.
9. No Co-Authored-By trailers in commits.
10. Write running scripts as x.new then mv; never edit in place.
