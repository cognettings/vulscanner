---
id: installation
title: DevSecOps Installation
sidebar_label: Installation
slug: /tech/ci/installation
---

You can use the DevSeCops agent
on any [x86_64](https://en.wikipedia.org/wiki/X86-64)
machine in which [Docker](https://www.docker.com/) is installed.
You can also integrate the agent
into your `CI/CD` to ensure
that your software is built and shipped
without previously reported vulnerabilities
in our _Fluid Attacks' platform_.

In order to use The Agent,
there are some requirements:

1. Make sure you have
   a DevSecOps agent token.

   This token can be generated
   in our platform [scope](/tech/platform/groups/scope/other-sections/agent) section
   **(Organization>Groups>GroupName>Scope),**
   where you will find
   the DevSecOps Agent Token section.

![DevSevOps Generation Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1663687225/docs/machine/agent/installation/dev_token_section.png)

Click on the **Manage Token** button
and a pop-up will appear
where you can **Generate** the token
or click on **Reveal Token**
in case you already generated one.

![DevSevOps Generation Modal](https://res.cloudinary.com/fluid-attacks/image/upload/v1663687225/docs/machine/agent/installation/manage_toke.png)

> **Note:** The DevSecOps token is valid for **180 days**
> and each token is unique and different for each group.
> Also, keep in mind that the generation/renewal
> of the agent token is the **users' work.**
> The roles that can generate this token are:
> [user](/tech/platform/groups/roles#user-role),
> [user manager](/tech/platform/groups/roles#user-manager-role)
> and
> [vulnerability manager.](/tech/platform/groups/roles#vulnerability-manager-role)

1. If you want to run The Agent on your local machine,
   Docker MUST be installed.
   - Make sure your execution environment
     has the required dependencies:
     - Docker (>= 20.10.10)
   - Install docker by following
     the official guide:
     - <https://docs.docker.com/engine/install/>.

> **Note:** You can also run The Agent in one of
> your CI/CD Pipelines on a third-party repository,
> such as GitHub,
> GitLab,
> Azure,
> and others,
> without installing docker on your machine or premises.

## Arguments to run your Agent

When using the Agent,
consider the use of these arguments
according to your necessities,
keep in mind that you can use this in your
local or CI/CD executions.
The arguments are:

- `--token`: Your DevSecOps agent token (required).
- `--dynamic / --static`: Check for only DAST / SAST vulnerabilities
  respectively (optional).
- `--strict / --lax`: Run forces in either strict or lax mode (default `--lax`).
- `--verbose`: Set the level of detail of the report (default `-vv`).
  - `-v`: Show non-compliant, vulnerable locations that would break
    policy[^1][^2] and thus the build in Strict mode.
  - `-vv`: Show vulnerable finds regardless of policy compliance.
- `--repo-name`: Git repository name (optional).
- `--repo-path`: Git repository path (optional).
- `--breaking`: Strict mode severity customization.
  Vulnerable locations with a severity below this threshold
  will not break the pipeline. This option takes values
  between 0.0 (recommended) all the way up to 10.0 (optional).
- `--feature-preview`: Enables the feature preview mode (optional).

> **Note:** Strict mode customization like severity thresholds
> and grace periods for new locations can also be set in
> the platform organization's Policies tab.
> In the case of `--breaking`, the value set in platform, if set, **caps**
> the value passed to this CLI option.

:::tip
You can check the agent's arguments in your container by running the
following command:

```sh
  docker run --rm -ti fluidattacks/forces:new forces --help
```

:::

## Examples run the Agent on your local machine

Here you will find some examples running
the agent on your local machine;
remember that you can use different
arguments according to the need or
context to visualize the execution.

Once docker is successfully installed
on your local machine,
we need to Run the **Docker image**,
which will help us to download all
the dependencies of forces.
You do it with the following command:

```sh
   docker pull fluidattacks/forces:new
```

To run the container. Here you have some examples:

- To check `all` finds including static and dynamic:

  ```sh
  docker run --rm -ti fluidattacks/forces:new forces --token <your-token> -vv
  ```

- To check for `static` locations only:

  ```sh
  docker run --rm -ti fluidattacks/forces:new forces --static --strict --token <your-token>
  ```

- To check for `dynamic` locations only:

  ```sh
  docker run --rm -ti fluidattacks/forces:new forces --dynamic --strict --token <your-token>
  ```

- Verify the locations of a specific repository:

  ```sh
  docker run --rm -ti fluidattacks/forces:new forces --dynamic --strict --repo-name <nickname repo> --token <your-token>
  ```

- To break the pipeline only if vulnerable locations
  with a severity of and above 4.5 are found:

  ```sh
  docker run --rm -ti fluidattacks/forces:new forces --dynamic --strict --breaking 4.5 --token <your-token>
  ```

:::tip
The `--rm` and
`--ti` parameters are optional.
Thus, you can define the best way according to your context.
:::

## Examples run the Agent on your CI/CD

If you want to run forces from your
Repository's pipeline,
we present the following examples:

In `GitLab` add these lines to your `.gitlab-ci.yml`

```yaml
forces:
  image:
    name: fluidattacks/forces:new
  script:
    - forces --token <your-token> --strict --repo-name <repository name>
```

In `Azure DevOps` add these lines to you configuration file:

```yaml
jobs:
  - job: Fluidattacks Agent
    pool:
      vmImage: "ubuntu-latest"
    steps:
      - script: |
          docker pull fluidattacks/forces:new \
            && docker run fluidattacks/forces:new --token <your-token>
```

In `Jenkins`, the configuration file should look like this:

```groovy
pipeline {
  agent {
    label 'label'
  }
  environment {
    TOKEN = "test"
  }
  stages {
    stage('Forces') {
      steps {
        script {
          sh """
            docker pull fluidattacks/forces:new
            docker run fluidattacks/forces:new forces --token ${TOKEN} --repo-name <repository name>
          """
        }
      }
    }
  }
}
```

In `GitHub`, the configuration file should look like this:

```yaml
jobs:
  forces:
    runs-on: ubuntu-latest
    container:
      image: fluidattacks/forces:new
      env:
        TOKEN: <your-token>
        REPO_NAME: <repository name>
    steps:
      - name: Run Agent check
        run: forces --token ${TOKEN} --strict --repo-name ${REPO_NAME}
```

## Result of the execution of The Agent

After any execution of the Agent,
you can check out its logs on Fluid Attacks' platform as well,
on the **DevSecOps** tab.
Organization>Groups>GroupName>DevSecOps.
For more information about this section,
click [here](/tech/ci).

## Troubleshooting

1. Please make sure that your Docker engine version is >= 20.10.10.

   ```sh
   $ docker --version

   Docker version 20.10.10, build v20.10.10
   ```

   This is important because the agent
   uses a [GNU libc](https://www.gnu.org/software/libc/) version >= 2.34,
   and the
   default [seccomp](https://en.wikipedia.org/wiki/Seccomp) profile
   of Docker <= 20.10.9
   [is not adjusted to support the clone syscall](https://github.com/moby/moby/blob/v20.10.9/profiles/seccomp/default.json)
   of GNU libc
   [introduced in version 2.34](https://sourceware.org/git/?p=glibc.git;a=commit;h=d8ea0d0168b190bdf138a20358293c939509367f).

1. Please check that your Docker installation is working.

   If it is, you should be able to run a Hello World:

   ```sh
   $ docker run hello-world

   Hello from Docker!
   This message shows that your installation appears to be working correctly.
   ...
   ```

   Otherwise,
   please refer to the Docker documentation
   and the Docker installation steps.

1. If after following the steps above
   you still experience issues running the agent,
   feel free to contact us at [help@fluidattacks.com](mailto:help@fluidattacks.com)
   and we'll do our best to help.

   Please include in the report as much information as possible
   to help us reproduce the problem, for example:

   - The Docker Engine and Server version: `$ docker info`.
   - The host fingerprint: `$ uname -a`.
   - The value of `$ docker inspect fluidattacks/forces:new`.
   - The organization, group, and repository name you are executing the agent on.
