---
id: onboarding
title: Onboarding
sidebar_label: Onboarding
slug: /talent/engineering/onboarding
---

Before setting up your development environment,
make sure you have completed
the initial [onboarding](/talent/everyone/onboarding)
for every talent at Fluid Attacks.

## Basic machine configuration

This is the minimum configuration required for your machine

1. [Install Linux](https://www.youtube.com/watch?v=ycTh_x-hzro&t=159s).
1. Run TimeDoctor on Linux using the following command:

   ```bash
   export QTWEBENGINE_DISABLE_SANDBOX=1 && ~/timedoctor2/timedoctor2
   ```

1. [Install nix](https://nixos.org/download.html).
   Choose single user installation.
   If you encounter the error:

   ```bash
   error: cannot connect to socket on 'nix/var/nix/daemon-socket/socket': Permission denied
   ```

   choose the multi-user installation option.
   But before [remove nix folders](https://docs.fluidattacks.com/development/stack/nix#uninstalling-nix).
1. [Install makes](https://makes.fluidattacks.com/getting-started/).
1. [Install VScode](/talent/engineering/onboarding/#editor).
   Only the first command for now. If required install nix-env.
1. [Install Git](https://docs.gitlab.com/ee/topics/git/how_to_install_git/index.html).
1. Create a GitLab account. The username must follow the convention: `usernameatfluid`,
   where the username is the one before @fluidattacks in your credentials.
1. [Create SSH key](https://docs.gitlab.com/ee/user/ssh.html).
1. Configure key in your Gitlab.
1. [Configure Git to sign commits using SSH](https://docs.gitlab.com/ee/user/project/repository/ssh_signed_commits/).
1. Write and email to help@fluidattacks.com with your GitLab username
   requesting access to our repository.
1. [Read the guide to do a local test with makes](https://docs.fluidattacks.com/development/stack/makes/).
1. Browse through the [Products](/development/products) section
   to learn about the particular product
   you are going to start working on.

## Environment

This section will guide you through setting up
a terminal
with AWS credentials
and a code editor
in an automated way
every time you enter
your local checkout
of the Universe repository.

After this section you will have:

- A terminal with AWS credentials
  for the specific product you are developing.
- An editor with:
  - The source code of the Universe repository.
  - Recommended development extensions.
  - Automatic code formatters on save.
  - Auto completion and go to definition.
  - OS libraries required.

### Terminal

We'll configure the terminal first.
Once the terminal is configured,
all of the applications you open from it
will inherit the development environment
and credentials.

At this point you should have Nix and Makes
already installed in your system,
so we won't go into those details.

For maximum compatibility,
we suggest you use [GNU Bash](https://www.gnu.org/software/bash/)
as the command interpreter of your terminal.

Please follow the following steps:

1. Make sure you have the following tools installed in your system:

   - [Nix](/development/stack/nix)
   - [Makes](/development/stack/makes)
   - [Git](https://git-scm.com): `$ nix-env -iA nixpkgs.git`.
   - [Direnv](https://direnv.net): `$ nix-env -iA nixpkgs.direnv`.

1. Access to your `~/.bashrc`:

   ```bash
   code ~/.bashrc
   ```

1. Add the following variables to your `~/.bashrc`
   or to a file at `$universe/.envrc.config`:

   ```bash
   # Automatically fill Okta login form to retrieve AWS credentials
   export OKTA_EMAIL=<username>@fluidattacks.com
   export OKTA_PASS=<your-password>

   # Define your remote branch for processes like git hooks
   export CI_COMMIT_REF_NAME=<username>atfluid
   ```

   You can optionally omit the OKTA_PASS. In that case,
   it will be asked interactively on the terminal.

1. Add the following to the end of your `~/.bashrc`:

   ```bash
   export DIRENV_WARN_TIMEOUT=1h
   source <(direnv hook bash)
   ```

1. run the changes in your `~/.bashrc`:

   ```bash
   source ~/.bashrc
   ```

Reload your terminal for changes to be loaded.

1. Clone with SSH the
   [universe repository](https://gitlab.com/fluidattacks/universe)
   into the path of your preference.

1. Change directory to the universe repository:

   ```bash
   $ cd $universe
   ```

1. [Configure Git Username and Email](https://linuxize.com/post/how-to-configure-git-username-and-email/).
1. **Note:** The Email must be the corporate email.
   The username must only contain the first name started
   in capitals and the last name started in capitals.

```sh
Example: Aureliano Buendia
```

1. Pick the AWS role you want to load AWS credentials for.
   The options may change depending on your assigned permissions:

   ```bash
   Select AWS Role:
   Account: fluidsignal (205810638802)
     [ 1 ] dev
     [ 2 ] prod_airs
     [ 3 ] prod_docs
     [ 4 ] prod_integrates
     [ 5 ] prod_melts
     [ 6 ] prod_observes
     [ 7 ] prod_skims
     [ 8 ] prod_sorts
   Selection: <type a number here>
   ```

   - This prompt will be shown only if you have multiple roles assigned.
   - If you see an authentication error,
     make sure your email and password are correct.
   - If you see the following error:

     ```
     Error: Status Code: 404
     Error: Summary: Not Found: Resource not found: me (Session)
     ERROR: SAMLResponse tag was not found!
     ```

     Please remove your [AWS Okta processor](https://github.com/godaddy/aws-okta-processor)
     configuration directory by running:

     ```bash
     $ rm -rf ~/.aws-okta-processor/
     $
     ```

     And then try again.
     This error happens when
     [AWS Okta processor](https://github.com/godaddy/aws-okta-processor)
     tries to reuse a cached expired session.

1. Pick the Development environment you want to load:

   ```text
   Select the development environment you want to load:

   Once the environment has finished loading,
   please close your code editor if it is open,
   and then open it by invoking it from this terminal.

   You can reload the environment at any moment with: $ direnv allow

   1) airs       4) integratesBack    7) reviews
   2) common     5) integratesForces  8) skims
   3) docs       6) melts             9) sorts
   Selection: <type a number here>
   ```

1. AWS commands run from this terminal
   will be authenticated to AWS now.

   If you need to get the value of the secrets explicitly,
   you can echo any of the AWS variables exported,
   namely:
   _AWS_ACCESS_KEY_ID_,
   _AWS_SECRET_ACCESS_KEY_,
   _AWS_SESSION_TOKEN_, and
   _AWS_DEFAULT_REGION_.

1. (optional) Some tools are used occasionally,
   so they are not part of the development environment,
   for instance: `kubectl`, `jq`, `awscli`, among others.

   If you require any extra tools,
   you can search them [here](https://search.nixos.org/packages)
   and install them with Nix.
   If you happen to use them very frequently,
   you can add them to the development environment.
   The development environment is yours and for your benefit,
   help us take care of it.

At this point,
you can open a new terminal,
and all of the applications you open
by calling them from this terminal
will inherit the development environment
and credentials.
This works because every command
that you execute on the terminal
(like `awscli`, `kubectl`, or your code editor)
is spawned as a child process,
and environment variables like _PATH_, _AWS\_\*_, among others,
are inherited by the child process
from the parent process.

For specific last steps to have each product running in local
please refer to products section.

### Configuration

You have almost finished the configuration.

1. [Install sops](https://docs.fluidattacks.com/development/stack/sops).

1. Create your branch. Branch name must be equal to gitlab username.

1. All changes that you are going to upload must be with your branch.

1. Configure the mailmap, adding your name to the file.

1. Look file in the root folder of the repository as
   `.mailmap`.

1. add yourself in alphabetical order like this:

   ```bash
   Nombre Apellido <user@fluidattacks.com> useratfluid <user@fluidattacks.com>
   ```

With these steps you have finished the configuration.

Go to [First Commit](https://docs.fluidattacks.com/talent/engineering/onboarding/#first-commit)
to push your changes.

### Editor

We highly recommend you use Visual Studio Code
because most of the team uses it,
and it works very well for our purpose.

You can install it with:

```bash
$ NIXPKGS_ALLOW_UNFREE=1 nix-env --install --attr vscode --file https://github.com/nixos/nixpkgs/archive/b42e50fe36242b1b205a7d501b7911d698218086.tar.gz
```

Now, from within a terminal
that was setup as explained in the previous tutorial,
open the [VS Code workspace][workspace]:

```bash
universe $ code universe.code-workspace
```

You will probably see a popup
to install the recommended extensions,
please install them:

![](https://res.cloudinary.com/fluid-attacks/image/upload/v1664733557/docs/development/setup/recommended-popup.png)

If you didn't see the popup,
please go to the extensions tab (`Ctrl+Shift+X`),
type `@recommended`,
and install the recommended extensions for the workspace.
You can click on the small cloud button
to the right of "WORKSPACE RECOMMENDATIONS"
and to the left of the pencil
to download them all at the same time:

![](https://res.cloudinary.com/fluid-attacks/image/upload/v1664733557/docs/development/setup/recommended-extensions.png)

You can test if everything works correctly by opening a JSON file,
adding empty lines between elements,
and then saving the file.
The empty lines should be removed,
and the keys sorted alphabetically.
In other words, the file should be automatically formatted on save.

For further customization,
you can add install other extensions
or open the settings with `Ctrl+,`
to configure things like the font, font size, or theme.
If you think an extension or setting can be useful
to other developers,
please add it to the [workspace][workspace] configuration.

Finally, take into account that certain extensions
or settings can prevent the environment from working.
Feel free to ask for help
in the _Development_ space on Google Workspace
if something doesn't work.

### First commit

The last step is loading change to the repository.

1. Add your changes in git.

1. Create a commit following the [syntax](https://docs.fluidattacks.com/development/stack/commitlint/syntax/commit).

Read the
[Contributing](https://docs.fluidattacks.com/development/contributing)
section carefully.

Check if the commit message is valid:

```bash
m . /lintGitCommitMsg
```

Create a new
[issue](https://gitlab.com/fluidattacks/universe/-/issues/new)
and assign it to you.

1. Remember step number 1 for the issue title.

1. Type remains issue and in description choose no-template.

1. Assign it to you and create de issue.

1. Push your commit to the repository.

1. If the pipeline fails, you must enter the job that failed and fix it.

1. If the pipeline is correct, you can make a merge request.

1. You must approve the merge request when it passes the pipeline.

1. If all goes well, you can now close the issue.

[workspace]: https://gitlab.com/fluidattacks/universe/-/blob/trunk/universe.code-workspace
