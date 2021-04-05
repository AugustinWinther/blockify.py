# Commit Guidelines
A basic guide on how the commits should be done in this repo. 
The guidelines are based on [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) 
and [Angluar's Commit Message Guidelines](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md).

## Commit Message Format
Every commit should consist of a **header**, a **body** and a **footer**. And it would be structured like this:

```
<type>(<scope>): <Subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```
The **header is ALWAYS mandatory**, you should always use both _type_ and _subject_ in the header. _Scope_ is optional.
_Body_ and _footer_ are optional, but should be used when needed.

#### Type:
Must be one of the following:

- **build**: Changes that affect the build system or external dependencies
- **docs**: Documentation only changes
- **feat**: A new feature
- **fix**: A bug fix
- **perf**: A code change that improves performance
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **revert**: Reverting a previois commit. Hash of the commit that is reverted needs to be inn the subject

#### Scope:
The scope should be the name of the the section of the codebase that is beeing changed. This is optional. Use if needed.  
  
Allowed scopes:
- **indexer**: Changes related to the texture-indexer code
- **block**: Changes related to block textures and block lists
- **main**: Changes related to the main part of the codebase (blockify.py)

#### Subject:
The subject contains a succinct description of the change:

- use the imperative, present tense: "change" not "changed" nor "changes"
- **Capitalize** the first letter
- no dot (.) at the end

#### Body:
Just as in the **subject**, use the imperative, present tense: "change" not "changed" nor "changes".
The body should include the motivation for the change and contrast this with previous behavior.
Keep it very simple

#### Footer:
The footer should contain any information about **Breaking Changes** and is also the place to
reference issues that this commit **Closes**.

**Breaking Changes** should start with the word `BREAKING CHANGE:` with a space or two newlines. The rest of the commit message is then used for this.
