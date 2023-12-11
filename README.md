# Outil-de-visualisation-evolution-des-traces-execution

## Objective
 The objective is to allow users to follow the evolution of the logging instructions in their projects.
 This allows to easily see the information related to a log instruction weather it be when it was added,
 when it's edited or when it is removed from the code.

## Requirements

- Git
- Python 3.6 or higher

## Installation

1. Clone the repository using Git:

```shell
git clone https://github.com/Projet-de-fin-etudes/Outil-de-visualisation-evolution-des-traces-execution
```


2. Execute the program:

- **Windows**
  - Open the `dist` folder.
  - Double-click on the `myscript_windows.exe` file.

- **macOS & Linux**
  - Open a terminal window.
  - Navigate to the `dist` folder:
    ```shell
    cd dist
    ```
  - Execute the program:
    ```shell
    ./myscript_linux
    ```

Note: Ensure that you have the necessary permissions to execute the program. The provided instructions are applicable to the respective operating systems: Windows, macOS, and Linux

## Usage
1. Add a repository either by pulling it from a git repository or by opening a local repository or choose one that was already added to the application. 
2. You will then have to choose which branch you want to analyse. 
3. The app will automatically select the frameworks that would work with the repository. You and add or remove some of the selected.
4. You will then have to choose the dates you would like the analysis to be held between.
5. Once that is done click on the search button.
6. The app will then display the log instructions and the relevant information to these logs. 

## How to Contribute

1. **Familiarize Yourself with the Project**: Start by exploring the project's repository, reading through the codebase, and getting acquainted with the existing issues and pull requests. Understand the project's coding standards and guidelines.
   
2. **Install Dependencies**: Before you start contributing, make sure you have all the required dependencies installed. You can do this by running the following command:
    ```
    pip install -r requirements.txt
    ```
    This will install all the necessary packages and libraries needed to work on the project.

2. **Create a Fork**: If you plan to contribute to the project, fork the repository. This will create a copy of the project under your GitHub account, allowing you to work on changes without affecting the original repository.

3. **Branching Strategy**: For each new feature or bug fix, create a new branch from the `main` branch. Use descriptive names for branches, and avoid working directly on the `main` branch.

4. **Commit Guidelines**: Make well-structured commits with clear and concise messages. Reference related issues or pull requests where applicable.

5. **Pull Requests (PR)**: When you are ready to submit your contribution, create a pull request from your forked repository to the original repository's `main` branch. Ensure that your pull request description explains the changes made and why they are valuable.

6. **Code Review Process**: All PRs will undergo a code review process. Be open to feedback and be prepared to make necessary changes to your code as suggested by the reviewers.

7. **Continuous Integration (CI)**: The project have CI configured to run automated tests on each PR. Ensure that your changes pass the tests. To merge in the main branch, your PR must pass the CI checks.You also have to have at least 80% of code coverage for the tests.

8.  **Merge Approval**: Once a pull request is approved by at least one maintainer or core contributor, it will be merged into the `main` branch.

9.  **Issue Tracking**: If you encounter a bug or have a feature request, open a GitHub issue. Provide a clear and detailed description to help others understand and address the problem.

10. **Collaborative Discussion**: Engage in discussions on GitHub issues, pull requests, and other communication channels. Be respectful of others' opinions and ideas.

## Communication Channels

To facilitate collaboration and communication, we use the following channels:

1. **GitHub Issues**: For bug reports, feature requests, and general project-related discussions.

2. **Pull Requests**: Discuss code changes and improvements directly on pull requests.

3. **Discussions**: For more extended or open-ended conversations, use GitHub Discussions.

## Conclusion

Thank you for contributing to our open-source project! Your participation is invaluable to the success of this community-driven effort. Let's collaborate, learn from each other, and build something amazing together. Happy coding!