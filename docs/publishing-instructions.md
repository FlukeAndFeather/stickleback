1. Update the version number in setup.py.
2. In the shell, build package with `python3 setup.py sdist bdist_wheel`
3. Then check package with `twine check dist/*`
4. Publish to Test PyPI with `twine upload --repository testpypi dist/*`
5. If everything looks good, publish with `twine upload dist/*`
