# seccomp-ci-demo
***WARNING: vulnerable service -- for demonstration purposes only***

### What is this?
This is a simple flask app that is purposely vulnerable to demonstrate how applying seccomp filters to containers can help limit the syscalls that can be made from within the container by any process.

This repository demonstrates how to set up a CI workflow that automatically generates a seccomp filter for your container.

### Further details

Further explanation of this project's purpose and directions for how to try this yourself can be found in this repository's Wiki.
