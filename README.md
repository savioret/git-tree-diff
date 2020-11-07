# git-tree-diff
Python command line script to show a tree-form view of modified files in a branch or within a range of revisions

## Requirements
  * git : get it at https://git-scm.com/
  * python 3.x: https://www.python.org/

## Usage

```bash
git-tree-diff.py [-h] [-s] [-u] [-n num] [-b BRANCH] [-f rev] [-r rev [rev ...]]
```

```
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
  -f rev, --from rev    Revision from which to obtain the changes. If not provided, uses the HEAD of the current branch. Must be used in conjunction with --branch

Revision diff:
  Show modified files between two arbitrary revisions

  -r rev [rev ...], --rev rev [rev ...]
                        Revisions to compare with. If only one revision is specified then that revision is compared to the working directory, and, when no revisions are specified, the working directory files are compared to its first parent
```

The script works in two different modes. Using `--branch` or `--from` shows diff between branches (using the oldest common ancestor approach), whilst `--rev` allows to just diff revisions or tags and should not be combined with `--branch` nor `--from`.
The `--from` must be used in cunjunction with `--branch`, and it defaults to `HEAD`
Note that showing differences between branches is a little tricky as the script will try to find out the *oldest* common ancestor of both branches.


#### Example: Show branch changes between curren branch and `master`
```
git-tree-diff --branch master
```

#### Example: Show branch changes between the changeset C and `master`
```
git-tree-diff --branch master --from C
```

#### Example: Show changes between HEAD and revision X
```
git-tree-diff --rev X
```

#### Example: Show changes between revision X and Y
```
git-tree-diff -r X Y
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
