# Branches and Pull Requests

## COMP423 / COMP590 Branching Conventions

For coursework, the `stage` branch is deployed to your team's cloud infrastructure. The `stage` branch serves as your team's "main" branch, in the sense that when you merge work to it your work will be deployed. The `stage` branch is also what your individual branches should be based on and merged back into.

Common team workflow scenarios include:

* Beginning work on a new Issue Branch
* Beginning work on a subtask of an Issue Branch
* Pushing your branch to GitHub
* Collaborating on a branch on GitHub
* Creating a Pull Request (PR) and Code Review (CR)
* Continuing work after on PR after creation / CR changes requested
* Catching a PR branch up with its base branch before merging
* Merging a PR via Squash and Merge
* Switching Issues/Tasks to Work on the "Next Thing"
* Switching Issues/Tasks to Review a Teammate's Code
* Catching your team's `stage` branch up with [csxl.unc.edu](https://csxl.unc.edu) production's `main` branch

Each of these scenarios is discussed step-by-step below.

### Beginning Work on a New Issue Branch

When using GitHub Project Board and Issues to organize your team's tasks and work, you can and should link relevant `git` branches in development to the Issue. This will cause pushes to the branch to be added to the issue's history to create a single, coherent narrative around updates to the branch. Additionally, when the time comes to merge this branch via a pull request, the merge of the pull request will automatically close the issue and transition it to the merged/done column of your Project Board. The names of your branches should, ideally, contain the issue's number. There are two strategies for getting started on a new Issue branch:

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
3. Reset your development database with fresh data:
    * `python3 -m backend.script.reset_demo` (if this fails, see the [database documentation](docs/database.md))

As per the above section, when you reach progress points large and small, you are encouraged to push to collaborative branches so that you and your partners on the branch do not diverge to significantly.

### Pull Requests and Code Review

There are three scenarios in which you will encounter Pull Requests and Code Reviews:

1. Before merging a small Issue Branch into `stage`
2. Before merging a subtask into an Issue Branch
3. Before merging a medium Issue Branch (whose subtasks were reviewed) into `stage`

The process is largely the same, however it is important to be careful to properly establish the branch that the Pull Request will be merged into (the "base ref").

After successfully pushing to a branch on GitHub, you will see a link to create a pull request for the branch printed in the terminal output. 

Alternatively, if you go to GitHub's Pull Requests tab and select "New Pull Request", the first selection is the base and the second is the branch you are creating the PR for. **This is where to be careful!** If you are working on a subtask of an Issue Branch, the `base` should be the Issue Branch. However, if you believe the current branch is ready to be merged back into `stage`, select `stage` here (it _should_ be the default selection due to how your team configured the repository). Then, for the **compare** branch, select the branch you are creating the Pull Request for. Below, you should see an overview of how many commits, file changes, and so on, differentiate the base branch from the comparison branch. Assuming this looks correct, press the Green "Create Pull Request" button.

Name your Pull Request more meaningfully than just the default branch name. Additionally, make an effortful attempt to write a solid description of what is going on in this PR at a high-level, in English. It is important that your PR highlights all of the changes made so that your code reviewer is able to understand the motivation behind the PR. Below is a good format for items to include in your PR.

**Pull Request Template**:
> - Short description of the pull request and what it accomplishes.
> - Major Changes Section: Include a list of major changes and provide important points for your Code Reviewer if necessary.
> - Testing Section: It is useful to verify that you have tested your feature and that it works. Explain what you did to test your feature to your Code Reviewer.
> - Future Considerations Section: Your PR will often either leave some features / fixes to be worked on later, or create the need for new features / fixes. Include these in this section.
*In addition, if there is anything important to point out to a Code Reviewer, you can do so here.*

[Here is an example of a PR from the CSXL Site that follows this template](https://github.com/unc-csxl/csxl.unc.edu/pull/107). 

Add your Code Reviewer(s) in the right-hand column to request a Code Review. Also, assign the members who contributed code to the PR.

Create the Pull Request!


### Continuing work after on PR after creation / changes requested

Creating a Pull Request does not prohibit you from making additional commits and pushes to the PR branch, in fact this is common and required when a Code Review (CR) requests changes before giving approval to merge.

To continue work on a branch with an open PR, just switch to the branch in your development environment and follow the steps of "Collaborating on a Branch" above. Namely: give the branch a pull with rebase in the event that one of your partners made some progress. From this point, you can make additional progress, commits, and push to the branch of the PR. These changes will show up in the PR history.

If changes to your PR were requested by a Code Reviewer, after you've fixed them it's best to ask for a final review pass for sign-off from the Code Reviewer.

### Merging a PR via Squash and Merge

Once a PR has an approving CR and is ready to be merged, you should see a green check in the PR interface and a comment that "This branch has no conflicts with the base branch" so that merging can be performed automatically. If you see a message about a merge conflict preventing automatic merging, see the next section below.

**Important**: to maintain a clean, linear `git` history we recommend selecting the merge strategy of "Squash and merge". This strategy will enable GitHub to combine all of the commits of this branch into a single commit that gets merged back into the base branch. Click the down arrow on the green button if you do not see "Squash and merge" and select it.

After merging in the PR, best practice is to go ahead and delete the branch. If this PR was for an Issue Branch and you linked it to an Issue on your project board, as described above, not only will the Issue automatically be closed, but the card on your Project Board will be moved to **Done**.

Finally, back in your local dev container, if you were working in this branch you can go ahead and switch back to the base branch, pull, and delete your local branch with the work that was merged in:

~~~
git switch [base-branch]
git pull origin [base-branch]
git branch -d [merged-in-branch-name]
~~~

### Catching a PR branch up with its base branch before merging

When a PR targets a base branch to be merged into that has progressed since the original branch was established, and merging cannot be performed automatically, it is requisite to "catch up" the branch of the PR. There are many ways of doing this, but our recommended strategy is tied to the convention of ultimately merging by squashing into a single commit. With this strategy, our recommendation for catching up a branch is to simply create a merge commit on your Issue/PR branch by pulling from the base branch and resolving any conflicts. Remember, your base branch may either be `stage` or, if you are working on a subtask branch, the issue branch your subtask targets.

1. Confirm you are currently working on the PR/Issue branch in your DevContainer
2. Pull the latest changes on your PR/Issue branch (see Collaborating on a Branch Above)
3. Fetch latest changes on the base branch: `get fetch origin base-branch-name`
4. Merge the base branch with your issue branch: `git merge base-branch-name`
5. Resolve any merge conflicts and follow `git` instructions (read `git status`) to navigate
6. Push resulting merge commit to your PR/Issue branch: `git push origin issue-branch-name`

After completing these steps, you should be able to "Squash and Merge" your PR.

### Switching Issues/Tasks to Work on the "Next Thing"

When working in a highly collaborative `git` environment, it is common to jump around between working branches. Getting comfortable with this will be a huge productivity boon!

Before changing branches, you need to be considerate of any uncommitted changes. To avoid loss of work, `git` will generally prevent you from doing anything that may overwrite changes, however if you are working on new files that are not staged, you may not receive a warning because they do not risk being overwritten. There is a risk in creating a mess of your work or accidentally committing files you meant for one branch to another, unrelated, branch. Therefore, as a general rule of thumb, **always check your current branch status before switching branches with `git status`.**

Once you have confirmed everything you are working on is committed appropriately, it is generally wise to go ahead and push your branch. This makes it possible to collaborate, if it comes up, it also serves as a backup of your work in the event your computer malfunctioned or you wanted to resume your own work from another machine.

(Advanced `git` note: the `git stash` command can be useful in very quick context switches, but because we are making use of a highly granular git branching strategy, the benefits of `stash` are somewhat outweighed by the benefits of granular git branches for collaboration.)

Finally, fetch latest changes and switch to the branch you are looking to work on and reset the database:

1. `git fetch origin && git switch [branch-name]`
2. `python3 -m backend.script.reset_demo`

If you're looking to take on a new Issue or Subtask, you'll switch to `main` or the issue branch, respectively, and create a new branch as discussed in the beginning work sections above.

### Catching your team's `stage` branch up with [csxl.unc.edu](https://csxl.unc.edu) production's `main` branch

While you are working on your projects, improvements, features, and functionality continue to happen on the `main` branch of the CSXL.unc.edu web site! Your repository is connected to the upstream, production repository via a `git remote` named `upstream`. Ultimately, for your work to be mergable into the production's `main` branch, you'll need to catch your `stage` branch up with production periodically. This is not a hard requirement, but it is a good practice, and we are being mindful not to make significant changes for the duration of the semester in the areas which you all are working on, so conflicts should be minimal.

The most straightforward process for catching your team's `stage` branch up with production's `main` branch is conceptually the same as the section "Catching a PR branch up with its base branch before merging", however you'll need to do this from the `upstream` remote repository, <https://github.com/unc-csxl/csxl.unc.edu> rather than your team's repository:

~~~
git switch stage
git pull origin stage
git switch --create merge/upstream/main
git fetch upstream
git merge upstream/main
# Resolve any conflicts and create merge commit
git push origin merge/upstream/main
~~~

At this point, create a PR for a team member to approve to merge in upstream changes and catch your stage branch up. When merging this PR, you are encouraged to use the strategy of creating a merge commit rather than squashing and merging.
