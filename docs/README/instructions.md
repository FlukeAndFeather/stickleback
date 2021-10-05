Instructions for updating the README.

1) Cells with plotly outputs (e.g. using plot_predictions()) should not be rendered to the README. Create a GIF of the plot in action (e.g. using Quicktime or Windows Game Bar) and save it to docs/resources. Reference the GIF with `![alt text here](docs/resources/name-of-gif.gif)`. Note: the GIF will not show up properly in the notebook because the README will live in the root directory. Then add an 'nbconvert-skip' cell tag.

2) Restart the kernel and run all.

3) From the command line, run `jupyter nbconvert --to markdown --output-dir='.' docs\README\README.ipynb -TagRemovePreprocessor.remove_all_outputs_tags='{nbconvert-skip}'`.

4) Commit and push to GitHub.

You did it! Thanks for keeping the documentation up to date.
