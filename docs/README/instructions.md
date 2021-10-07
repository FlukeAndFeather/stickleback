Instructions for updating the README.

1) Cells with plotly outputs (e.g. using plot_predictions()) should not be rendered to the README because they won't render in markdown. Add an 'nbconvert-skip' tag to the cell so the code appears but the outputs won't (see step 3). Then, add a new markdown cell with a GIF of the plot in action. You'll need to use something like Quicktime or Windows Game Bar to create a screen recording. Then convert to GIF, save it to docs/resources, and commit+push to GitHub. In the markdown cell, include the GIF with `![description of gif](https://github.com/FlukeAndFeather/stickleback/raw/main/docs/resources/name-of-gif.gif)`.

2) In Jupyter, restart the kernel and run all.

3) From the command line, run `jupyter nbconvert --to markdown --output-dir='.' docs/README/README.ipynb --TagRemovePreprocessor.remove_all_outputs_tags="{'nbconvert-skip'}"`.

4) Back in Jupyter, restart the kernel and clear all outputs. This keeps the file size small enough for GitHub.

5) Commit and push to GitHub.

You did it! Thanks for keeping the documentation up to date.
