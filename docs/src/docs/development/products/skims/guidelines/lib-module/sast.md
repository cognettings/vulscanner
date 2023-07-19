---
id: sast
title: SAST Vulnerabilities
sidebar_label: SAST
slug: /development/products/skims/guidelines/lib-module/sast
---

SAST refers to "Static Application Security Testing", and it is performed
by searching for deterministic vulnerabilities in code files.

In skims' repository, the methods that perform this analysis are
grouped in two modules, named apk and sast.

## APK

As the name implies, this module checks vulnerabilities by reversing
Android APK files.

## SAST

Methods included here are subdivided in two modules: root and path,
and the SCA sub-model, whose methods are divided between both.

### Path

The methods in this library perform vulnerability analysis by parsing a file
into iterable objects and performing search algorithms. This is specially
useful in configuration files that do not use complex control structures or
variable definitions.

Among the languages/extensions supported are:

- Bash scripts
- Dockerfiles
- Config files such as .xml, .jmx, .config, .properties

The following two-step procedure is used:

1. Parse the file using external libraries, regex or other methods.
  For example, the BeautifulSoup library is used to parse HTML files.
1. Search vulnerabilities looking for miss configured values or properties
  in the parsed file.

When developing new methods, it is recommended that the skims' developer
checks for existing helper functions and methodologies already used.

For most methods, the vulnerability search consists of searching special keys
and comparing the set values to any possible vulnerable configuration.

### Root

The methods in this library use graph algorithms to search vulnerabilities in
code or configuration files written in the following languages:

- C#
- Dart
- Go
- Java
- JavaScript
- Kotlin
- TypeScript
- Python
- HCL (Terraform files)
- YAML and JSON (Configuration files)

Since the methods in this library have a steeper learning curve, they have a
specific [here](./root) in this documentation.

### SCA

Source Composition Analysis (SCA) is a part of skims in charge of
finding vulnerabilities in the supply chain of software.

Methods may be divided in path and root modules, but they rely on
external sources and have associated cloud infrastructure.

A detailed explanation can be found on the development guideline [here](./sca)
