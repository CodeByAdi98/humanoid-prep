# Week 01 — Git & GitHub (29 Aug – 5 Sep 2026)

## Hours
Build: __ / Learn: __ / Read: __ / Log: __

## What I built

- `humanoid-prep` repository, initialised locally and pushed to GitHub
- README describing the 20-week scope
- `setup/ubuntu-git-setup.md` — a full runbook for configuring Git and SSH on a fresh
  Ubuntu machine, written immediately after doing it, so the next machine is a
  copy-paste job
- Five commits on a branch, merged into `main` via a pull request

## What I learned

**A commit is a snapshot, not a diff.** It stores the complete state of the project, plus
a pointer to its parent. Git computes diffs on demand for display, but it stores states.

**A branch is a movable label.** Not a container of commits — a file holding one commit
ID. Committing moves the label forward automatically. Creating a branch is writing a new
40-byte file, which is why it's instant.

**HEAD marks where I'm standing.** It normally points at a label, which points at a
commit. It can also point straight at a commit, which is "detached".

**Commit IDs are computed from content**, including the parent's ID. So altering an old
commit changes the ID of everything downstream. That single fact explains rebase and
amend: they don't edit history, they build a replacement and abandon the original.

**My laptop and GitHub are independent peers.** Neither is authoritative except by
convention. `origin/main` is a *local* record of where I last saw GitHub's main — a
written-down gauge reading, not a live wire. It updates when I fetch, not when someone
else pushes.

**SSH keys.** A key pair where the public half is a padlock I hand out freely and the
private half is the only thing that opens it. GitHub challenges my laptop to prove it
holds the private key; the secret never crosses the network.

**Creating a branch copies nothing.** After `git switch -c week-01-git`, `git log
--oneline` showed one commit with three labels on it: `week-01-git`, `main`, and
`origin/main`. All pointing at the same place. The branch was a new 40-byte file, not a
copy of anything. They only separated once I committed.

**Committing sends nothing anywhere.** I looked for `git-commands.md` on GitHub and it
wasn't there — because it was committed to a local branch I'd never pushed. Git writes to
my machine; only `push` crosses the network.

## What broke, and how I fixed it

**Detached HEAD stranded `main`.** In the first sandbox level I ran `git checkout C1`,
which pointed HEAD directly at a commit rather than at a label. I then committed twice.
Both commits were created correctly, but `main` never moved — committing drags forward
whatever label HEAD is attached to, and there was none. The level failed even though the
commit graph looked right. Fix: reset the level and commit without the checkout detour.

Lesson: detached HEAD isn't an error, it's a mode where commits aren't named by anything.
Real-world consequence — those commits are reachable only by their hash and look lost.

**`git branch -f bugFix~3` was rejected.** The command needs two separate arguments: the
label to move, and where to put it. I'd glued them into one word, so Git read the whole
thing as a branch name and refused, since `~` isn't legal in a name. Correct form was
`git branch -f bugFix HEAD~3`.

**`git rebase C6` said "Fast forwarding" instead of replaying commits.** Rebase moves the
commits that are on my current position but *not* on the target. I was standing on C1,
which is already an ancestor of C6, so there was nothing to move. Rebase didn't error —
it just walked HEAD forward to the target, undoing a correct step I'd taken earlier.

**Confused about which drawing was local and which was the remote.** Position on screen
isn't the clue. The reliable rule: `HEAD` and `o/main` exist only on my machine — GitHub
keeps no record of where I'm standing, or of my memory of its state. The drawing
containing those labels is always the local one.

**`git revert HEAD^` cancelled the wrong commit.** Revert takes the commit to *cancel*,
not a destination to move to. `HEAD^` is the parent — one too far back. Correct form for
cancelling the current commit is `git revert HEAD`. Reset takes a destination, revert
takes a victim; they read similarly and mean opposite things.

## Open questions

- Merge conflicts — haven't hit one yet. Expecting the first when two changes touch the
  same lines.
- `.gitignore` — will need it at week 4 when ROS 2 generates `build/`, `install/`, and
  `log/` folders that shouldn't be committed.
- `git stash` — for parking uncommitted work when switching branches. Learn it when it
  bites.
- Reset's three modes (`--soft`, `--mixed`, `--hard`) and exactly what each does to the
  working tree, staging area, and repository. Read the table properly.

## Next week

Week 2 — Python: core language. Variables, collections, comprehensions, functions,
imports, `pathlib`, exceptions. No NumPy or pytest until week 10. Plus two MIT
*Missing Semester* shell lectures.

Deliverable: a CLI script that reads a file, transforms it, writes output, handles
arguments, and catches at least one exception.