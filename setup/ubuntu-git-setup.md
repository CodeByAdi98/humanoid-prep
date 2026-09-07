# Git & GitHub setup on a fresh Ubuntu machine

My own runbook. Written 4 September 2026 after doing it once on the Alienware M16 R2
(Ubuntu 24.04). Follow it top to bottom on any new machine — laptop reinstall, cloud GPU
instance, anything.

**Read the "why" lines.** They're the reason this file exists rather than a bare list of
commands. If something errors, the why is what lets me work out the fix.

Time: about 15 minutes, most of it waiting on the browser.

---

## What this achieves

By the end: Git installed and configured with my identity, an SSH key pair generated,
the public half registered with GitHub, and a verified connection. After this, `git push`
and `git clone` work without passwords.

---

## Step 1 — Check what's already there

Establish the baseline before changing anything.

```bash
git --version
```

Need 2.28 or newer for the `init.defaultBranch` setting in step 2. Ubuntu 24.04 ships
2.43. If this says "command not found":

```bash
sudo apt update && sudo apt install git
```

```bash
git config --list --show-origin
```

`--list` dumps every setting in effect. `--show-origin` prefixes each line with the file
it came from.

**Settings live at three levels:**

| Level | File | Applies to |
|---|---|---|
| System | `/etc/gitconfig` | Every user on the machine |
| Global | `~/.gitconfig` | Me, in all my repos |
| Local | `.git/config` inside a repo | That one repo |

Lower in the list wins. **"Global" means "my user account on this machine"** — not
"everywhere in the world". Badly named. It's the level I want 99% of the time, and it's
what `--global` writes to.

Expect either nothing back, or leftovers from a previous setup.

---

## Step 2 — Configure

### Identity

```bash
git config --global user.name "CodeByAdi98"
git config --global user.email "adityababurajan@gmail.com"
```

**Why:** every commit permanently records who made it. Git refuses to commit without
these. The email must match the one on my GitHub account, or GitHub won't link the
commits to my profile.

### Default branch name

```bash
git config --global init.defaultBranch main
```

**Why:** `git init` has to create a first branch and name it. Git's built-in default is
`master`; GitHub's is `main`. Leaving the mismatch means my first push creates two
branches where I wanted one. This lines them up.

### Editor

```bash
which code
git config --global core.editor "code --wait"
```

**Why:** when I commit without a message on the command line, Git opens a text editor.
Ubuntu's default is often `vim`, which has no menus and no obvious way to quit. This
points Git at VS Code instead.

`--wait` is not optional. Without it, `code` opens the window and instantly reports
"done" to the terminal, so Git commits with an empty message before I've typed anything.

`which code` must print a path first (mine: `/snap/bin/code`). If it prints nothing,
VS Code isn't on the PATH — use `nano` instead:
`git config --global core.editor "nano"`.

### Pull strategy

```bash
git config --global pull.rebase true
```

**Why:** `git pull` is two operations — fetch (download their commits) then combine.
When my branch and the remote's have diverged, "combine" can mean merge (keep both
lines, add a joining commit) or rebase (replay my commits on top of theirs, rewriting
them). Since Git 2.34, a bare `pull` refuses to guess and stops with an error.

`true` = rebase. Right default for solo repos: keeps history a straight line, and I'll
never have a divergence I didn't cause myself.

Override per command with `git pull --no-rebase` when on a shared branch —
**rebasing rewrites commits, so never rebase work others have already pulled.**

### Confirm

```bash
git config --list --show-origin
```

Should show five lines, all from `~/.gitconfig`.

Note: Git normalises setting names to lowercase when listing, so `init.defaultBranch`
prints as `init.defaultbranch`. Not an error.

**Shortcut for next time:** `~/.gitconfig` is plain text. Instead of retyping all of the
above, copy that one file from an existing machine and everything comes with it.

---

## Step 3 — Generate an SSH key pair

### The idea first

GitHub needs to know it's really me. A password would be a shared secret — I know it,
GitHub knows it, anything that reads it can impersonate me.

SSH keys work differently. I generate **two linked files**:

- **Private key** — never leaves this machine, ever
- **Public key** — handed out freely

Anything scrambled with the public key can only be unscrambled with the private one. So
GitHub sends a challenge that only the private-key holder can answer. My secret never
crosses the network.

**The public key is a padlock I hand to anyone. The private key is the only thing that
opens it.** Distributing padlocks is safe.

### The command

```bash
ssh-keygen -t ed25519 -C "adityababurajan@gmail.com"
```

- `ssh-keygen` — part of Linux's SSH toolkit, not a Git command. Git just borrows it.
- `-t ed25519` — `-t` is *type*. Ed25519 is the modern algorithm: shorter, faster,
  stronger than the older RSA default.
- `-C` — a plain-text **comment** appended to the public key. Zero cryptographic role.
  It's a label so I can tell which machine a key came from when several are listed on
  GitHub. `aditya@alienware-ubuntu` would arguably be more useful than the email.

### What it asks

**"Enter file in which to save the key"** → press Enter. Default is
`~/.ssh/id_ed25519`, which is where SSH looks automatically.

**"Enter passphrase"** → type a real one. This encrypts the private key file *on disk*.
Without it, anyone with my laptop or a backup of it can push to GitHub as me.

**Nothing appears as I type.** No dots, no asterisks, no cursor movement. Deliberate — it
hides the length from anyone watching. Feels broken. It isn't.

**"Enter same passphrase again"** → retype.

Then it prints a fingerprint (a short hash of the key) and some ASCII "randomart".
The art is decorative; ignore it. **Save the fingerprint** — it's used to verify in
step 5.

### Forgot the passphrase, or left it empty?

```bash
ssh-keygen -p -f ~/.ssh/id_ed25519
```

`-p` = change passphrase, `-f` = which file. Asks for the old one (just Enter if none),
then the new one twice. The key itself is unchanged; only the file's encryption changes.

Size tells: an unencrypted ed25519 private key is ~399 bytes, encrypted ~464.

---

## Step 4 — Inspect what was made

```bash
ls -l ~/.ssh
```

`ls` lists a directory, `-l` = long format (permissions, owner, size, date).
`~` = my home directory.

Two new files, same base name:

- `id_ed25519` — private. Permissions must be `-rw-------`, meaning only I can read it.
  **SSH refuses to use a private key with looser permissions than that.**
- `id_ed25519.pub` — public. `-rw-r--r--` is fine.

```bash
cat ~/.ssh/id_ed25519.pub
```

`cat` prints a file to the terminal. One line, starts `ssh-ed25519`, ends with my
comment. ~107 bytes. Completely safe to share.

```bash
cat ~/.ssh/id_ed25519
```

Several lines, wrapped in `BEGIN OPENSSH PRIVATE KEY` / `END`. **Look once to learn the
difference on sight, then never move, copy, or paste it anywhere.**

If it ever leaks: delete both files, generate a new pair, remove the old public key from
GitHub.

An empty `authorized_keys` file may already exist. Unrelated — that's the reverse
direction, listing keys allowed to SSH *into* this machine. Ignore it.

---

## Step 5 — Register the public key with GitHub

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the entire line — from `ssh-ed25519` through the email, no line breaks, no leading
or trailing spaces.

Then in the browser:

1. https://github.com/settings/keys (or avatar → Settings → sidebar → Access →
   SSH and GPG keys)
2. **New SSH key**
3. **Title:** the machine name, e.g. "Alienware Ubuntu". This is for me — it's how I know
   which key to revoke when I retire a machine.
4. **Key type:** Authentication Key
5. **Key:** paste
6. **Add SSH key**

**Verify:** the fingerprint GitHub displays must match the one `ssh-keygen` printed in
step 3. Same string, character for character. That proves GitHub received exactly what I
sent, uncorrupted.

Keys are per-account, not per-repo — one key covers personal repos and any organisation
I belong to.

---

## Step 6 — Test the connection

```bash
ssh -T git@github.com
```

- `-T` = don't give me an interactive terminal, I only want to connect
- `git@github.com` = the user `git` at host `github.com`. GitHub runs one shared account
  called `git`; it works out who I am from the key.

### First run asks about the host

```
The authenticity of host 'github.com' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

**This is the reverse of step 5.** I proved my identity to GitHub with my key; now GitHub
proves its identity to me with its key. My machine has never seen this host, so it asks
me to confirm I trust it.

The fingerprint above is GitHub's genuine one (verifiable on their docs). If it matches,
type the full word `yes` — not `y`.

That writes it into `~/.ssh/known_hosts`. Future connections are checked silently, and it
warns loudly if the fingerprint ever changes — which would mean something is
impersonating GitHub.

### Success

```
Hi CodeByAdi98! You've successfully authenticated, but GitHub does not provide shell access.
```

**The second half is not a failure.** I asked to connect to a machine; GitHub confirmed
who I am and then declined to give me a command prompt, because it's a Git host, not a
server I log into. Being greeted by username = the key worked.

### Failure

`Permission denied (publickey)` → the key didn't register. Re-check step 5, confirm the
whole line was pasted, confirm the fingerprints match.

---

## Step 7 — Passphrase handling (ssh-agent)

If it asked for the passphrase, that's the encryption working. To avoid retyping it
constantly:

```bash
ssh-add -l
```

`ssh-add` manages keys held by **ssh-agent** — a background program that keeps decrypted
keys in memory for the login session.

| Output | Meaning | Action |
|---|---|---|
| A line with my fingerprint | Agent has the key | Nothing. Ubuntu desktop loads it automatically. |
| "The agent has no identities" | Agent running, empty | `ssh-add ~/.ssh/id_ed25519` |
| "Could not open a connection..." | No agent | `eval "$(ssh-agent -s)"` then `ssh-add ~/.ssh/id_ed25519` |

The agent forgets everything on reboot, by design. Typing the passphrase once per boot is
the normal cost of an encrypted key. Fair trade.

---

## Connecting a local repo to GitHub

Once per repo, not per machine.

**Manual route** — when the local repo exists first:

```bash
git init
git remote add origin git@github.com:CodeByAdi98/<repo-name>.git
git push -u origin main
```

- `git init` creates the repository (a hidden `.git` folder holding all the history)
- `git remote add` maps a nickname to a URL. `origin` is convention, not magic.
- `-u` on the first push records the pairing, so plain `git push` works afterwards

**Use the SSH URL** (`git@github.com:...`), not the HTTPS one. HTTPS asks for credentials
every time; SSH uses the key.

**Create the GitHub repo empty** — no README, no .gitignore, no licence. Those options
put a commit in the remote before I push, giving two histories with no shared ancestor,
and the push gets rejected.

**Clone route** — when the remote exists first:

```bash
git clone git@github.com:owner/repo.git
```

Does four jobs at once: downloads the full history, adds the `origin` remote, sets up
branch tracking, and checks out the files. Everything in the manual route, automatically.

Add `--depth 1` to download only the latest commit instead of full history — worth it for
huge repos I only want to run, not study. (Relevant for `genie_sim`, Isaac Lab.)

---

## Quick reference

Setup is once per machine. These are the ones I'll actually run daily and won't need to
look up after a few weeks:

| Command | Does |
|---|---|
| `git status` | Where am I, what's changed. **Run constantly.** |
| `git add <file>` | Stage a change for the next commit |
| `git commit -m "msg"` | Seal staged changes into history |
| `git log --oneline --graph --all --decorate` | Draw the commit graph. Worth aliasing. |
| `git switch <branch>` | Move to another branch (safer than `checkout`) |
| `git switch -c <branch>` | Create a branch and move to it |
| `git push` | Send my commits to GitHub |
| `git pull` | Fetch GitHub's commits and combine |

---

## When it goes wrong

- https://ohshitgit.com — short recipes for "I did X, how do I undo it"
- `git reflog` — every position HEAD has held. **Committed work is almost never truly
  lost.** Uncommitted work is the only thing Git can't recover, which is the argument for
  committing often.
- `git help <command>` or `man ssh-keygen` — already installed, no internet needed

---

## Next machine

1. Copy `~/.gitconfig` across — skips all of step 2
2. Generate a **new** key pair (step 3) and register it separately. Never copy private
   keys between machines; one key per machine means revoking one doesn't affect the rest.
3. Steps 5 and 6 unchanged