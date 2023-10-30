# Branches and Pull Requests

## COMP423 / COMP590 Branching Conventions

For coursework, the `stage` branch is deployed to your team's cloud infrastructure. The `stage` branch serves as your team's "main" branch, in the sense that when you merge work to it your work will be deployed. The `stage` branch is also what your individual branches should be based on and merged back into.

Common team workflow scenarios include:

* Beginning work on a new Issue Branch
* Beginning work on a subtask of an Issue Branch
* Pushing your branch to GitHub
* Collaborating on a branch on GitHub
* Creating a Pull Request and Code Review
* Catching your Issue Branch up-to-date with `stage` for Merging
* Continuing work after creating a Pull Request
* Switching Issues/Tasks to Make Requested Changes / Improvements
* Switching Issues/Tasks to Review a Teammate's Code
* Catching your team's `stage` branch up with [csxl.unc.edu](https://csxl.unc.edu) production's `main` branch

Each of these scenarios is discussed step-by-step below.

### Beginning Work on a New Issue Branch

When using GitHub Issues to organize your team's tasks and work, you can and should link relevant `git` branches in development to the Issue. This will cause pushes to the branch to be added to the issue's history to create a single, coherent narrative around updates to the branch.The names of your branches should, ideally, contain the issue's number. There are two strategies for getting started on a new Issue branch:

#### Creating the Branch via GitHub's UI

1. Use GitHub's Issues UI to open the Issue
2. Look for "Development" in the right-hand sidebar, click "Create a branch" for the issue.
3. Review the suggested branch name
4. Click "Change branch source" and verify the source is `stage`
5. Under What's next? Click "Checkout locally"
6. Copy or retype the commands to `fetch` from `origin` and then `checkout` or `switch` to the branch established

#### Creating the Branch via `git` Locally

1. In your DevContainer, switch to the `stage` branch.
2. Create and switch to your branch `git switch --create NN-[descriptive-branch-name]` where `NN` is the issue number on GitHub and the `[descriptive-branch-name]` adds explanatory context of what the purpose of the branch is.
3. Push your branch ref to GitHub: `git push origin [your branch's name]` 
4. From the GitHub UI, open the Issue, look for "Development" in the right-hand sidebar. Click the gear icon.
5. Search for your branch name and link it to the issue.

### Beginning Work on a Subtask of a Medium-sized Issue Branch

Medium-sized issues, which involve subtasks, should certainly have their own Issues and respective branches established as described above. Toward the end of following a best practice of "small, incremental pull requests (PRs) and code reviews (CRs)", we encourage branching subtasks off of your issue branch. Then, for each subtask, request a PR and CR before merging the task branch back into the issue branch. When all subtasks are complete, the final PR and CR to merge back into `stage` is much less daunting because all code has previously been reviewed.

After establishing an Issue Branch, here's how to begin working on a subtask branch:

1. Confirm you are working on your issue branch: `git branch --show-current`
    * If you are not on the correct branch, switch to it and `git pull origin --rebase` first
2. Create the subtask branch `git switch --create NN-subtask-[descriptive-branch-name]` where `NN` is the issue number and `[descriptive-branch-name]` describes the subtask.
3. Once commits/progress has been made, push the subtask branch to GitHub as below

### Pushing a Branch to GitHub

When you reach a stopping point on a branch, whether it is complete or not, it's a good practice to form a commit with an update on what you have completed and what remains and pushing it to GitHub.

1. Confirm you are working on the branch you expect:
    * In our DevContainer terminal's shell prompt, you should see the current branch in the yellow, parenthetical text of your prompt string.
    * Or, use the git command: `git branch --show-current`
2. Check status of changes `git status` and be sure any untracked files or changes not staged for commit, that should be, have been `get add`'ed to your staging area.
3. Make a commit and give it a meaningful title and body per best practice of writing git commit messages.
4. Push your branch: `git push origin [branch-name]`

### Collaborating on a Branch

When collaborating on a branch, it is important to pull changes your collaborator(s) may have pushed regularly. A good habbit is before you resume work on a shared branch, go ahead and pull each time. Additionally, if you attempt to push and are rejected because your branch is out of date, you will need to pull and this workflow also addresses this need.

When collaborating on a shared branch, we recommend pulling with rebasing such that your changes are linear and follow commits your team may have pushed:

1. Confirm you are working on the branch you expect:
    * In our DevContainer terminal's shell prompt, you should see the current branch in the yellow, parenthetical text of your prompt string.
    * Or, use the git command: `git branch --show-current`
2. Pull any progress on the branch your collaborator(s) may have pushed:
    * `get pull origin --rebase [branch-name]`

As per the above section, when you reach progress points large and small, you are encouraged to push to collaborative branches so that you and your partners on the branch do not diverge to significantly.

### Pull Requests and Code Review

There are three scenarios in which you will encounter Pull Requests and Code Reviews:

1. Before merging a small Issue Branch into `stage`
2. Before merging a subtask into an Issue Branch
3. Before merging a medium Issue Branch (whose subtasks were reviewed) into `stage`

The process is largely the same, however it is important to be careful to properly establish the branch that the Pull Request will be merged into (the "base ref").

After successfully pushing to a branch on GitHub, you will see a link to create a pull request for the branch. Alternatively, if you go to GitHub's Pull Requests tab and select "New Pull Request", the first selection is the base and the second is the branch you are creating the PR for.