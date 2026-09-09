# Git commands — personal reference

My own notes. Written while working through Week 1 of the prep plan.

**Danger column:** ⚠️ means this command can lose work or rewrite history. Read the note
before running it, especially on a machine that costs money by the hour.

---

## Mental model, in four lines

- A **commit** is a complete snapshot of the project, plus a pointer to its parent. Not a
  diff. Git stores states and calculates diffs on demand.
- A **branch** is a sticky note holding one commit ID. Committing peels the note off the
  old commit and sticks it on the new one. That's the only reason branches seem to
  "advance".
- **HEAD** marks where I'm standing. Normally it points at a note, which points at a
  commit. It can also point straight at a commit — that's *detached*, and commits made
  there get no note.
- My **laptop and GitHub are independent peers.** Neither is authoritative except by
  convention. They sync only when I tell them to.

---

## Setup — once per machine

| Command | Effect | ⚠️ |
|---|---|---|
| `git --version` | Print the installed version. Need 2.28+ for `init.defaultBranch`. | |
| `git config --list --show-origin` | Show every setting in effect and which file it came from. | |
| `git config --global user.name "<name>"` | Set the name stamped on my commits. | |
| `git config --global user.email "<email>"` | Set the email stamped on my commits. Must match GitHub, or commits won't link to my profile. | |
| `git config --global init.defaultBranch main` | Name the first branch `main` instead of `master`, matching GitHub. | |
| `git config --global core.editor "code --wait"` | Use VS Code for commit messages. `--wait` is essential — without it, Git commits an empty message immediately. | |
| `git config --global pull.rebase true` | Answer the merge-or-rebase question for `git pull` in advance, so it doesn't stop and ask. | |
| `ssh-keygen -t ed25519 -C "<email>"` | Generate an SSH key pair. `-t` = type, `-C` = a plain-text label (no cryptographic role). | |
| `ssh-add -l` | List keys currently held by ssh-agent, which caches the decrypted key so I only type the passphrase once per session. | |
| `ssh -T git@github.com` | Test the GitHub connection. Success = greeted by username, then "does not provide shell access". **That second half is not an error.** | |

**Settings live at three levels:** system (`/etc/gitconfig`), global (`~/.gitconfig`),
local (`.git/config` in one repo). Lower wins. "Global" means *my user account on this
machine*, not "everywhere" — badly named.

---

## Starting a repository — once per project

| Command | Effect | ⚠️ |
|---|---|---|
| `git init` | Create a repository in the current folder. Makes a hidden `.git` folder holding all history. Delete that folder and only plain files remain. | |
| `git clone <url>` | Make a complete copy of an existing repository — full history, not just current files. Also sets up the `origin` remote and branch tracking automatically. | |
| `git clone --depth 1 <url>` | Clone only the latest commit. Worth it for huge repos I want to run, not study. | |
| `git remote add origin <url>` | Save GitHub's address under the nickname `origin`. **Writes one line to a config file — no network activity.** Format: `git@github.com:<username>/<repo>.git` | |
| `git remote -v` | Show saved remote addresses. A "show me what I saved" command. | |

**Git and GitHub are separate things.** Git is a program from 2005; GitHub is a website
from 2008 that hosts Git repositories. Git has no idea GitHub is special. My config
identity is a *label* on commits; my SSH key is an *ID card* shown at the door; the
remote is the *address*. Three different things.

**Use the SSH URL** (`git@github.com:...`), not HTTPS. HTTPS asks for credentials every
time.

---

## Everyday cycle

| Command | Effect | ⚠️ |
|---|---|---|
| `git status` | Which branch I'm on, whether HEAD is detached, what's changed. **Run constantly** — it's the answer whenever I feel lost. | |
| `git add <file>` | Stage a file for the next commit. Copies its current contents into the staging area. Not "add to repo" — it's *select for the next commit*. | |
| `git add .` | Stage everything in this folder and below. Convenient, but stages whatever is lying around — how people accidentally commit large files or secrets. | |
| `git commit -m "<message>"` | Seal staged changes into history. Without `-m`, Git opens the configured editor and waits. | |
| `git commit` | Same, but writes the message in the editor. Useful for longer messages. | |
| `git log` | Full history — hash, author, date, message per commit. | |
| `git log --oneline` | Compact history: short hash + message, one line each. | |
| `git log --oneline --graph --all --decorate` | Draws the commit graph in the terminal with branch labels. The real-Git version of the sandbox picture. Worth aliasing. | |
| `git branch` | List branches; asterisk marks the one I'm on. | |
| `git diff` | Show unstaged changes — working tree vs staging area. | |
| `git diff --staged` | Show staged changes — what would go into the next commit. | |

**Commit message convention:** imperative mood ("Add", not "Added"), first line under
~50 characters, describing *what changed*.

**Git tracks files, not folders.** An empty directory is invisible to Git and won't
appear in a commit.

---

## Branching

| Command | Effect | ⚠️ |
|---|---|---|
| `git switch <branch>` | Move to an existing branch. **Safer than `checkout` — cannot detach HEAD.** Prefer this. | |
| `git switch -c <branch>` | Create a branch at the current commit and move onto it. Nothing is copied — it writes a new label. | |
| `git branch <name>` | Create a branch at the current commit but **stay where I am**. HEAD doesn't move. | |
| `git branch -d <name>` | Delete a branch that's already merged. Refuses if it isn't. | |
| `git branch -D <name>` | Force-delete a branch even if unmerged. Can orphan commits. | ⚠️ |
| `git checkout <branch name>` | Move to a branch. Older command; does several unrelated jobs. Use `switch`. | |
| `git checkout <commit ID>` | Point HEAD **directly at a commit** — detached HEAD. New commits get no label and look lost when I leave. | ⚠️ |
| `git branch -f <branch> <destination>` | Force-move a branch label to any commit. Format: *what to move*, then *where to put it* — **two separate arguments.** Ex: `git branch -f main HEAD~3` | ⚠️ |

**Detached HEAD is not an error.** It's a mode where commits aren't named by anything.
Committing drags forward whatever label HEAD is attached to — if there's none, nothing
moves and the work looks stranded.

Git refuses to force-move the branch I'm currently standing on. Either switch away first,
or use `git reset`.

---

## Relative references

| Command | Effect | ⚠️ |
|---|---|---|
| `<ref>^` | One commit back along the parent chain. Ex: `main^`, `HEAD^` | |
| `<ref>~n` | `n` commits back. `HEAD~1` and `HEAD^` are identical. | |
| `HEAD` | The commit I'm standing on right now. Usable anywhere a command wants a commit. | |
| `<ref>^2` | On a **merge** commit only: the *second* parent. Different mechanism from `~2` — easy to confuse. | |

Relative refs only walk **backwards** through parents. Anything off to the side needs a
commit ID. In real Git that's the first seven characters of the hash from `git log`.

---

## Combining work

| Command | Effect | ⚠️ |
|---|---|---|
| `git merge <branch>` | Bring that branch's work **into where I'm standing**. Creates a commit with two parents. **Stand on the receiving branch first.** The merged-*from* branch does not move. | |
| `git rebase <target>` | Take the commits on my branch that aren't on the target, and **rebuild them on top of the target**. New commit IDs; the originals are abandoned. Result is one straight line, no merge commit. | ⚠️ |
| `git rebase <target> <branch>` | Same, but checks out `<branch>` first — saves a `git switch`. | ⚠️ |

**Merge vs rebase, in one line:** merge keeps both lines and joins them honestly; rebase
rewrites my line to look as though it always came after theirs.

**⚠️ Never rebase commits already pushed and pulled by others.** I'd be replacing commits
they still have; the two histories then disagree and it's unpleasant to fix. Rebase local
work freely before sharing; merge when combining shared branches.

If rebase says **"Fast forwarding"** instead of replaying, there was nothing to move —
my current position was already an ancestor of the target, so it just walked HEAD
forward.

---

## Undoing

| Command | Effect | ⚠️ |
|---|---|---|
| `git commit --amend` | Replace the most recent commit instead of adding a new one. For fixing a message or a forgotten file. Only before pushing. | ⚠️ |
| `git reset <destination>` | **Move the branch label backwards.** Takes a *destination*. Default keeps file changes in the working tree, so the work reappears as uncommitted edits. Ex: `git reset HEAD~1` | ⚠️ |
| `git reset --soft <dest>` | Move the label; keep changes **staged**. | ⚠️ |
| `git reset --mixed <dest>` | Move the label; keep changes **unstaged**. This is the default. | ⚠️ |
| `git reset --hard <dest>` | Move the label; **throw the changes away entirely.** The only command here that destroys uncommitted work permanently. | ⚠️⚠️ |
| `git revert <commit>` | Create a **new** commit whose content is the exact inverse of the named one. Takes a *victim*, not a destination. Ex: `git revert HEAD` cancels the current commit. | |
| `git reflog` | Every position HEAD has held, for ~90 days. **Committed work is almost never truly lost.** First thing to reach for after a mistake. | |

**Reset vs revert:**
- **Reset** rewrites history — the commit is gone from the record. Use on **local,
  unpushed** work only.
- **Revert** keeps history honest — original stays visible, an inverse commit is added on
  top. Use on **anything already pushed**, so the undo travels to others as an ordinary
  commit.

**Mistake I made:** `git revert HEAD^` cancels the *parent* of where I'm standing — one
commit too far back. To cancel the current commit, name it directly: `git revert HEAD`.

**Uncommitted work is the only thing Git can't recover.** That's the argument for
committing often.

---

## Working with GitHub

| Command | Effect | ⚠️ |
|---|---|---|
| `git push -u origin main` | Upload commits from local `main` to remote `origin`. `-u` links the two branches so plain `git push` works afterwards; only needed on a branch's first push. | |
| `git push` | Upload commits to the linked remote branch. | |
| `git push -u origin <branch>` | Push a new branch to GitHub. **GitHub doesn't know a local branch exists until I push it.** | |
| `git fetch` | Download GitHub's commits into my repo and update `origin/main`. **Touches nothing I'm working on — completely safe.** | |
| `git pull` | `fetch` + combine. Downloads, then merges or rebases into my current branch. | |
| `git pull --no-rebase` | Pull and **merge** — keeps both lines, adds a joining commit. Safer on shared branches. | |
| `git pull --rebase` | Pull and **rebase** — replays my commits on top of theirs. Straight-line history. Good default for solo repos. | ⚠️ |
| `git push --force` | Overwrite the remote branch with mine. **Can destroy other people's work.** | ⚠️⚠️ |

**`origin/main` is a local label**, not a live connection. It records where I *last saw*
GitHub's main — a written-down gauge reading, not a wire. It updates when I fetch, never
because someone else pushed.

**I can't work on `origin/main`.** Checking it out detaches HEAD, and committing there
creates a commit no label names. To build on what GitHub has: fetch, then merge or rebase
into a real branch of mine.

**Push rejected, "non-fast-forward"** means the remote has commits I don't. Git is
refusing to lose someone's work. Fetch and combine first.

---

## Pull requests

A **pull request is a GitHub feature, not a Git one.** It's a request to merge one branch
into another, with a page showing the changes so they can be reviewed before merging.
Standard practice on every team.

Rough flow:

1. `git switch -c <branch>` — new branch locally
2. Work, commit, repeat
3. `git push -u origin <branch>` — branch now exists on GitHub
4. On GitHub: **Compare & pull request** → describe the change → **Create pull request**
5. Review the diff → **Merge pull request**
6. `git switch main` then `git pull` — bring the merge back down locally

---

## Not learned yet

- **`.gitignore`** — tells Git to ignore files. Needed at Week 4 when ROS 2 generates
  `build/`, `install/`, and `log/` folders that shouldn't be committed.
- **Merge conflicts** — when two changes touch the same lines. Learn when it first
  happens.
- **`git stash`** — park uncommitted work to switch branches without committing.
- **`git cherry-pick`** — copy one specific commit onto the current branch.
- **`git bisect`** — binary search through history to find which commit broke something.

---

## When it goes wrong

- https://ohshitgit.com — short recipes for "I did X, how do I undo it"
- `git reflog` — the safety net
- `git help <command>` — installed locally, works offline