# git-tree-diff
Python command line script to show a tree-form view of modified files in a branch or within a range of revisions

## Requirements
  * git : get it at https://git-scm.com/
  * python 3.x: https://www.python.org/

## Usage

```bash
git-tree-diff.py [-h] [-s] [-u] [-n num] [-b BRANCH] [-f rev] [-r rev [rev ...]]
```


```bash
optional arguments:
  -h, --help            show this help message and exit
  -s, --status          Include file status occured in the diff
  -u, --utf8            Use utf8 characters for tree nodes
  -n num, --nspaces num
                        Number of spaces in each depth level

Ancestor mode:
  Show modified files in the current branch

  -b BRANCH, --branch BRANCH
                        Base branch or revision, must be an ancestor of <from>. It finds the oldest common ancestor between the branch and the HEAD of current branch
  -f rev, --from rev    Revision from which to obtain the changes. If not provided, uses the HEAD of the current branch.

Revision diff:
  Show modified files between two arbitrary revisions

  -r rev [rev ...], --rev rev [rev ...]
                        Revisions to compare with. If only one revision is specified then that revision is compared to the working directory, and, when no revisions are specified, the working directory files are compared to its first parent
```

#### Example: Show changes between curren branch and `master`
```
git-tree-diff -b dev
```

Note that showing differences between branches is a little tricky as the script will try to find out the common ancestor of both branches. If the two branches have already been merged at any moment, that common changeset will be taken as the first one for the diff.


#### Example: Show changes between HEAD and revision X
```
git-tree-diff -r X
```

#### Example: Show changes between HEAD and revision X and Y
```
git-tree-diff -f X -r Y
```

### Formatting the tree
#### Example: apply 2 spaces in each depth level
```
git-tree-diff -b master -n 2
```
```
.gitignore
.htaccess
app/
  |- config.py
  |- classes/
  |   \- MyController.py
  \- session.py
```

#### Example: show tree with diff status using utf8 tree characters with 1 space 

```
git-tree-diff -b dev -n 1 --utf8 --status
```
```
app/
 ├─Extensions/
 │  └─Ads/
 │   ├─ads_load.js[A]
 │   ├─AdsExtra.py[M]
 │   ├─AdsInjector.py[M]
 │   ├─AdsGoogleNative.py[M]
 │   └─AdsSenseSearch.py[M]
 └─lib/
    ├─config/
    │  ├─ConfigSession.py[A]
    │  ├─ConfigServer.py[M]
    │  └─extensions/
    │   ├─cfg-ads.py[M]
    │   └─cfg-users.py[M]
    ├─Routing.py[M]
    └─Response.py[M]
 ```

 The status tags appearing at after the file names are provided by the `--name-status` option of `git`
More info in the [git diff documentation page](https://git-scm.com/docs/git-diff#Documentation/git-diff.txt---diff-filterACDMRTUXB82308203)
