---
id: nix
title: Nix
sidebar_label: Nix
slug: /development/stack/nix
---

## Rationale

We use the [Nix ecosystem](https://nixos.org/)
for building and deploying all of our [Products](/development/products).

## Alternatives

## Usage

### Installing Nix

Please follow the steps
in the [official Nix Download Page](https://nixos.org/download.html).

If everything goes well,
you should be able to run:

```bash
$ nix --version
```

### Troubleshooting

If, during the installation, you get an error along the following lines:

```bash
It seems the build group nixbld already exists, but
with the UID 998. This script can’t really handle
that right now, so I’m going to give up.

You can fix this by editing this script and changing the
NIX_BUILD_GROUP_ID variable near the top to from 30000
to 998 and re-run.
```

You may have a conflicting previous install.
In order to fix this:

1. Remove the Nix directories
   as per the [Nix uninstall step](/development/stack/nix#uninstalling-nix)

1. Delete the users created by Nix.
   In Bash, you can use the command,

   ```bash
   $ compgen -u
   ```

   to list all users.
   The ones you are interested in
   are named along the lines of `nixbld${number}`.
   You can delete them, in Linux, using,

   ```bash
   $ sudo userdel ${nixUser}
   ```

1. Then, when all users are deleted, you can delete the Nix group,

   ```bash
   $ sudo groupdel nixbld
   ```

1. Finally, attempt to install Nix once again,
   using the `multi-user` configuration

### Uninstalling Nix

Run the command with root privileges if needed:

```sh
$ rm -fr /nix ~/.nix* ~/.cache/nix ~/.config/nix
```

## Guidelines

Please refer to the official manuals:

- The [Nix Package Manager](https://nixos.org/manual/nix/stable/).
- The [Nix Packages collection](https://nixos.org/manual/nixpkgs/stable/).
- The [NixOS Operative System](https://nixos.org/manual/nixos/stable/).
