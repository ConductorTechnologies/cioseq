## Version:0.5.1 -- 01 Nov 2023

Adds a method, cap_chunk_count(), to limit the number of chunks. Chunk size is adjusted accordingly.

## Version:0.4.1 -- 28 Aug 2023

* Adds a boolean difference method to the Sequence class.

## Version:0.4.0 -- 26 Aug 2023

* adds the abilliity to build a sequence from files on disk

## Version:0.3.0 -- 10 Jul 2023

* the `to()` function now handles an empty string for step separator, which enables frame spec strings compatible with Katana's command-line.

### Version:0.2.2 -- 25 May 2023

* Simple edit to remove circle test release. [b92a2c9]


### Version:0.2.0 -- 25 May 2023

* Implemented a feature to calculate first, middle, and last frames.

### Version:0.1.16 -- 24 May 2023

* Added tests for step and irregular sequences. [742d4c4]

### Version:0.1.15 -- 07 Aug 2021

* Use range without importing builtins. [f148290]

### Version:0.1.14 -- 27 Jun 2021

* Removed builtins module to avoid py2/3 errors. [f148290]

### Version:0.1.13 -- 26 Mar 2021

* CICD tweaks and readme. [b9d05ac]

### Version:0.1.12 -- 11 Mar 2021

* Universal flag. [958ef56]
* Adds pip-dependency-file key. [719ec31]

### Version:0.1.10 -- 10 Mar 2021

* Adds ssh key so we can push the tag in circleci. [60360af]
* Use skulk context. [3459bc0]

### Version:0.1.9 -- 09 Mar 2021

* Fixed wrong pypi registry. [a3d82e1]

### Version:0.1.6 -- 09 Mar 2021

* Adds release flow to circleci. [71bbca2]
* Add .circleci/config.yml. [30fd9d9]
* Adds tox for py 2.7 and 3.8. [7ce0970]

### Version:0.1.5 -- 21 Sep 2020

* Bad test name and $f4 token support. [f3c1923]

### Version:0.1.3 -- 20 Sep 2020

* Added several examples to the README and implemented and indexing. [fdec3b4]
 
### Version:0.1.2 -- 19 Sep 2020

* Python 2 and 3 compatibility. [4aba985]

### Version:0.1.1 -- 19 Sep 2020

* Transfer from core. As such, this is the first changelog entry. [54f9132]
* Sequence consumers must use factory. [a9fd08a]
* Adds cycle_progressions chunk strategy. [37075c9]
* Expander path list enhancements (#5)
* Lib enhancements (#4)
* adds sequence intersection check
* allows uppercase characters in angle-bracket template.. [255f61f]
* Initial commit. [7cf8fd3]


--