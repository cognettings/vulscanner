---
id: format
title: Format
sidebar_label: Format
slug: /tech/scanner/standalone/format
---

You can specify your routes in three ways.

1. Directly use the absolute path to the file or directory.

  ```yaml
    namespace: namespace
    sast:
      include:
        - /absolute/path/to/file/or/dir
  ```

1. Use a path relative to the working directory,
  only works if the key `working_dir` is defined.

  ```yaml
    namespace: namespace
    working_dir: /test/folder
    sast:
      include:
        - src/main/java/org/test/Test.java
  ```

1. Use [Unix-style globs](https://docs.python.org/3/library/glob.html)

  ```yaml
    namespace: namespace
    sast:
      include:
        - glob(*)
      exclude:
        - glob(**.java)
        - glob(src/**/test*.py)
  ```
