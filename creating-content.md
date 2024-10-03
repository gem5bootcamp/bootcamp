---
title: Guidelines for creating content
author: Jason Lowe-Power
---

This file describes how to create content for the bootcamp.

## Requirements

- Use markdownlint. We can ignore MD013 (line length) and MD026 (punctuation at end of headers).
- Install pre-commit and use that when using git.
- Use yaml frontmatter for title and always include an author

## Suggestions for creating content

- Keep code snippets short
  - Each snippet should fit on a slide
  - A good rule of thumb is about 10 lines at most
  - You can have an example that spans multiple snippets
  - Talk about each code snippet on its own
- Keep the theory part short
- Think about ways to keep things interactive

Inspiration:

- [Learning gem5](https://www.gem5.org/documentation/learning_gem5/introduction/) and the [old version](http://learning.gem5.org/).
- [Standard library docs](https://www.gem5.org/documentation/gem5-stdlib/overview)

## How to provide/use code

- We are planning on using github codespaces.
- Put boilerplate in the template repo under `materials/`.

## Things that were effective at teaching

- Lots of template code and just leave empty the main point that you were trying to learn.
- Copying code from a book into the terminal and make minor modifications to see what happens.
- Small short code snippets to write.
- It's helpful to have a site map for the directory structure.
- Youtube videos writing the code live line-by-line and explaining things.
- Having a big project with a specific goal in mind which touches the things you want to learn.
- Listening to someone else's thought process while they are working on the problem
- Take working code and then break it to see what errors happen.
- Someone provides a library with APIs and you have to implement the APIs and it's tested heavily outside.
- Extend someone else's (simple) code with some specific goal in mind.
- Code under very specific constraints so that you don't get lost in the forest.
- Pair programming
- Taking the code and then pulling out the state machine / structure.
  - Build your own callgraphs
  - Use gdb in a working example
- The socratic method. Have them try something and then help them move toward the "best" solution.
- Make sure to point out how gem5 differs from real hardware. Gap between theory and model.
- Keywords: repeat many times and have a glossary.
- Focus on one module. Ignore the others except for the interfaces. **Write detailed comments/notes**
- Make sure that c-scope/c-tags are enabled.
- Practice and do "it" yourself.

## Creating slides

Slides go in the `slides/` directory. Each slide is a markdown file.
The first slide should be the title slide and should have the title and author in the yaml frontmatter.

In this directory, you will find the slides that we use during the gem5 bootcamp and gem5 tutorials.
They are written using [Marp](https://marp.app/), a Markdown-based slide design tool.

We chose to use Markdown for slides to make it easier for us to update the code in the slides as gem5 changes and for the participants to copy-paste code.

To use Marp, we encourage you to install the [VS Code extension](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode), which should be automatically installed if you're using the codespaces devcontainer.
With the VS Code extension installed, when you open one of the slide decks (e.g., [Getting started](02-Using gem5/00-getting-started.md)), you can click on the preview button in the upper right to view the slides.
Also, you can use the Marp extension to save the slides as HTML or PDF.

For using the Marp command line, you can use the following command (pass in the file to convert).
Note: The local paths for the css file and the markdown don't work great. YMMV.

```sh
docker run --rm -v $PWD:/home/marp/app/ -e MARP_USER=$UID:$GID -e LANG=$LANG marpteam/marp-cli <markdown file>
```

### Style rules

- INSTALL THE [MARKDOWN LINT EXTENSION IN VS CODE](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) TO HELP WITH FORMATTING.
- Use `---` to separate slides.
- The first slide should be a "title" slide `<!-- _class: title -->`.
- The titles of all slides should be heading 2 `##`
- Code should be at most 65 characters wide.
- Do not use inline HTML unless *absolutely* necessary.
- Images should use markdown syntax `![alt text](path/to/image.png)`
- Always put links to the resources when referencing.

#### Linking to materials and slides

When linking to materials, use the following format:

```md
[path relative to the root of the repo](path relative to the current file)
```

Use the relative path from the current file.

#### Layouts

To use a different layout, you specify a class in the markdown file.

```md
<!-- _class: <layout> -->
```

Here are some of the available layouts:

- `title`: Title slide
- `two-col`: Two columns. To split the slide into two columns, use `###` (heading 3) to create a new column.
- `center-image`: Centers images horizontally
- `code-XX-percent`: Reduces font-size in code blocks. Valid values for `XX` are any of `[50, 60, 70, 80]`.
- `no-logo`: Removes the bottom logo.
- `logo-left`: Positions the bottom logo further to the left. Useful when using `bg right` images that cover the logo.

### Adding diagrams

To add diagrams, you can use the [draw.io VS Code extension](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio).
**You are strongly encouraged to use svg images for diagrams.**

After installing the extension, create a file with the name "\<name\>.drawio.png" and open it in VS Code.
Make sure you create a directory for each slide deck with its images.
You can then embed the image in the slide with the following markdown.

```md
![<description of the image>](<current slide name>/<name>.drawio.png)
```

If you need to have images on the left or right use `[bg left]` and `[bg right]` respectively.
In this case, you cannot have a description of the image, unfortunately.

## Improvement to make

- [ ] Can we possibly make it so that there's a button to copy the code examples?

## To print the slides

```bash
find . -name "*.md" -exec pandoc {} -o {}.html --self-contained -c ../themes/print-style.css \;
```
