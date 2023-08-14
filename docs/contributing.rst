.. _contributing:

*************
Contributing 
*************

This project follows the `all contributors specification <https://allcontributors.org/>`_. Contributions in many different ways are welcome!

Contribution Types
------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/HBPMedical/mip-dmp/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

`mip_dmp` could always use more documentation, whether as part of the official `mip_dmp` docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to create an issue at https://github.com/HBPMedical/mip-dmp/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `mip_dmp` for local development.

1. Fork the repository of `mip_dmp` on GitHub.

2. Clone your fork locally::

    git clone git@github.com:your_name_here/mip-dmp.git
    cd mip-dmp

3. Create a branch for local development::

    git checkout -b name-of-your-bug-fix-or-feature

4. Now you can make your changes locally.

.. important::
	Please keep your commit the most specific to a change it describes. It is highly advice to track unstaged files with ``git status``, add a file involved in the change to the stage one by one with ``git add <file>``. The use of ``git add .`` is highly disencouraged. When all the files for a given change are staged, commit the files with a brieg message using ``git commit -m "<type>[optional scope]: <description>"`` that describes your change and where ``<type>`` can be ``fix`` for a bug fix, ``feat`` for a new feature, ``refactor`` for a code change that neither fixes a bug nor adds a feature, ``docs`` for documentation, ``ci`` for continuous integration testing, and ``test`` for adding missing tests or correcting existing tests. This follows the Angular conventional commits, please see https://www.conventionalcommits.org/en/v1.0.0-beta.4/ for more details.

5. When you're done making changes, push your branch to GitHub::

    git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

   .. important::
       Please make sure that the pull request is made against the ``dev`` branch. The ``master`` branch is used for the stable version releases of `mip_dmp`.

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you submit a pull request, check that it meets these guidelines:

1. If the pull request adds functionality, the docs should be updated (See :ref:`documentation build instructions <instructions_docs_build>`). 

2. Make sure that the GitHub Action workflow that runs CI/CD passes

CI/CD Pipeline: Under the Hood
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The pipeline, described by the file `.github/workflows/python-app.yml <https://github.com/HBPMedical/mip-dmp/blob/master/.github/workflows/python-app.yml>`_, consists of the following stages:

    1. Setup a Python 3.9 environment using the `actions/setup-python@v3 <https://github.com/actions/setup-python>`_ action.
    2. Install with `pip` the dependencies listed by the file `requirements.txt <https://github.com/HBPMedical/mip-dmp/blob/master/requirements.txt>`_ along with the `flake8`, `pytest`, `wheel`, `setuptools` packages.
    3. Run the `flake8 <https://flake8.pycqa.org/en/latest/>`_ linter to check the code style.
    4. Test to create and install the distribution wheel of `mip_dmp` using `setuptools <https://setuptools.readthedocs.io/en/latest/>`_ and `pip <https://pip.pypa.io/en/stable/>`_.

Not listed as a contributor?
----------------------------

This is easy, `mip_dmp` has the `all contributors bot <https://allcontributors.org/docs/en/bot/usage>`_ installed.

Just comment on Issue or Pull Request (PR), asking `@all-contributors` to add you as contributor::

    @all-contributors please add <github_username> for <contributions>

`<contribution>`: See the `Emoji Key Contribution Types Reference <https://github.com/all-contributors/all-contributors/blob/master/docs/emoji-key.md>`_ for a list of valid `contribution` types.

The all-contributors bot will create a PR to add you in the README and reply with the pull request details.

When the PR is merged you will have to make an extra Pull Request where you have to:

    1. add your entry in the `.zenodo.json` (for that you will need an ORCID ID - https://orcid.org/). Doing so, you will appear as a contributor on Zenodo in the future version releases of mip_dmp. Zenodo is used by mip_dmp to publish and archive each of the version release with a unique Digital Object Identifier (DOI), which can then be used for citation.

    2. update the content of the table in `documentation/contributors.rst` with the new content generated by the bot in the README. Doing so, you will appear in the :ref:`Contributing Page <contributing>`.

------------

This document has been inspired and adapted from `these great contributing guidelines <https://github.com/dPys/PyNets/edit/master/docs/contributing.rst>`_.
