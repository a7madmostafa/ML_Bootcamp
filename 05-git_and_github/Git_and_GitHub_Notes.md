# Tutorial: Git & GitHub

## Table of Contents

1. [Versions Problem](#0-versions-problem)
2. [What Is Git?](#1-what-is-git)
3. [Why Use Git?](#2-why-use-git)
4. [What Is GitHub?](#3-what-is-github)
5. [Git Terminology](#4-git-terminology)
6. [Git Commands](#5-git-commands)
7. [More Terminology](#6-more-terminology)
8. [More Commands](#7-more-commands)

> **Image note:** The images are embedded using their original online URLs, so an internet connection is required to display them.

---

## 0- Versions Problem

<table>
  <tr>
    <td align="center">
      <img src="https://miro.medium.com/max/640/1*oCJb90-FMEYfcULslRr3Iw.webp" width="390" alt="Versions problem illustration from Medium">
    </td>
    <td align="center">
      <img src="https://pbs.twimg.com/media/FIrhW0ZXMA0U3PX?format=jpg&amp;name=900x900" width="370" alt="Versions problem illustration from OpenAcademics">
    </td>
  </tr>
  <tr>
    <td align="center">
      Credit: <a href="https://matvenn.medium.com/">Medium</a>
    </td>
    <td align="center">
      Credit: <a href="https://twitter.com/openacademics">OpenAcademics</a>
    </td>
  </tr>
</table>

<p align="center">
  <img src="https://www.insperity.com/wp-content/uploads/Remote_work_1200x630.png" width="600" alt="Remote work illustration">
</p>

<p align="center">
  Credit: <a href="https://www.insperity.com/blog/remote-work-policy/">insperity.com</a>
</p>

---

## 1. What Is Git?

- Git is a version control system.
- It is a tool used to manage source-code history.
- It allows you to track changes in files and revert to a previous version when needed.
- It allows developers to collaborate on the same project.

---

## 2. Why Use Git?

- Git is a distributed version control system.
- The full history of a project is stored locally on each developer's machine.
- This allows developers to work offline and commit changes whenever they want.
- Developers can work on the same project from multiple locations.
- Git is fast.
- Git is free and open source.

<p align="center">
  <img src="https://media.geeksforgeeks.org/wp-content/uploads/20190624140224/cvcss.png" width="500" height="300" alt="Centralized version control system">
  <img src="https://media.geeksforgeeks.org/wp-content/uploads/20190624140226/distvcs.png" width="500" height="300" alt="Distributed version control system">
</p>

<p align="center">
  Credit: <a href="https://www.geeksforgeeks.org/version-control-systems/">GeeksforGeeks</a>
</p>

---

## 3. What Is GitHub?

GitHub is a cloud-based hosting service that lets you manage Git repositories.

---

## 4. Git Terminology

### Repository

A repository is a directory or storage space where a project can live.

- It can be local, on your computer.
- It can be remote, on a server such as GitHub.
- It contains the project files, including documentation.
- It stores the revision history of each file.

### Clone

A clone is:

- A copy of a repository that lives on your computer instead of a website's server.
- The act of creating that copy.

### Commit

A commit is an individual change to a file or a set of files.

- It is similar to saving a file, but within Git.
- Each commit creates a unique ID called a **hash**.
- The hash helps record what changes were made, when they were made, and who made them.
- Commits usually contain a short commit message describing the changes.

### Push

Pushing means sending committed changes to a remote repository, such as a repository hosted on GitHub.

### Pull

When collaborating with others, it is important to keep the local repository up to date with the current project state.

- Pulling brings remote changes into the local repository.
- When a local copy is behind the remote copy, you may need to pull before pushing successfully.

---

## 5. Git Commands

### `git init`

Starts a new Git repository.

```bash
git init
```

### `git clone`

Obtains a repository from an existing URL.

```bash
git clone <repository-url>
```

### `git add`

Adds a change from the working directory to the staging area.

It tells Git to include updates to a particular file in the next commit.

```bash
git add <file>
```

### `git status`

Displays the state of the working directory and staging area.

It shows:

- Which changes have been staged.
- Which files are not being tracked by Git.

```bash
git status
```

### `git commit`

Stores all changes that have been staged with `git add` in the repository.

```bash
git commit -m "Commit message"
```

### `git push`

Uploads local repository content to a remote repository.

```bash
git push
```

### `git pull`

Fetches and downloads content from a remote repository, then immediately updates the local repository to match that content.

```bash
git pull
```

---

## 6. More Terminology

### Fork

A fork is a personal copy of another user's repository that lives in your account.

- It allows you to make changes without affecting the original project.
- It remains connected to the original repository.
- You can submit a pull request to the original repository's author.
- You can keep the fork up to date by pulling updates from the original repository.

### Branch

A branch is a parallel version of a repository.

- It exists within the repository.
- It does not affect the primary or master branch.
- It allows you to work without disrupting the live version.
- After completing changes, you can merge the branch back into the master branch.

<p align="center">
  <img src="https://gitbookdown.dallasdatascience.com/img/git_branch_merge.png" width="600" alt="Git branch and merge diagram">
</p>

<p align="center">
  Credit: <a href="https://www.nobledesktop.com">nobledesktop.com</a>
</p>

<p align="center">
  <img src="https://tedu.com.vn/uploaded/images/012021/gitflow.png" width="700" alt="Git workflow diagram">
</p>

<p align="center">
  Credit: <a href="https://tedu.com.vn">tedu.com</a>
</p>

---

## 7. More Commands

### `git log`

Lists the version history for the current branch.

It shows commits in reverse chronological order.

```bash
git log
```

### `git diff`

Shows the difference between changes in the working directory and changes that have been staged.

```bash
git diff
```

### `git checkout`

Switches between branches or restores working-tree files.

```bash
git checkout <branch-name>
```

### `git branch`

Lists, creates, or deletes branches.

```bash
git branch
```

### `git merge`

Joins two or more development histories.

```bash
git merge <branch-name>
```

