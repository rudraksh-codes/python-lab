This is normal. It means your local `main` branch isn't yet linked to the remote `main` branch.

Run:

```bash
git push --set-upstream origin main
```

or the shorter equivalent:

```bash
git push -u origin main
```

The `-u` (`--set-upstream`) does two things:

1. Pushes your local `main` branch to the remote repository (`origin`).
2. Records that `origin/main` is the tracking branch for your local `main`.

After that, future pushes are simply:

```bash
git push
```

and future pulls are:

```bash
git pull
```

without needing to specify `origin main` again.

If you want Git to automatically set the upstream for new branches the first time you push them, run this once:

```bash
git config --global push.autoSetupRemote true
```

Then `git push` will automatically establish the tracking relationship for newly created branches.
