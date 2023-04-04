# seccomp-ci-demo
***WARNING: vulnerable service -- for demonstration purposes only***

### What is this?
This is a simple flask app that is purposely vulnerable to demonstrate how applying seccomp filters to containers can help limit the syscalls that can be made from within the container by any process.

This repository demonstrates how to set up a CI workflow that automatically generates a seccomp filter for your container.

### Further details

This project was made to bridge the gap between a low-level Linux kernel security feature called [Seccomp-BPF](https://www.kernel.org/doc/html/v4.16/userspace-api/seccomp_filter.html) and modern software development processes. You can use the knowledge gained from this project to help prevent your containerized applications from being successfully exploited.

### What is Seccomp-BPF?
The programs that we run on computers rely heavily on the underlying operating system to do anything. Tasks like opening files and spawning new processes are abstracted in modern programming languages, but under the hood the code is making kernel requests called system calls (or syscalls). How important are syscalls for a program to function? Well, there are around 400 syscalls available in the Linux kernel, and even a basic “Hello World” program written in C makes 2 of them: write and exit.

Code running in so-called “user space” can’t really do anything without going through the kernel to do it. Eventually, some smart Linux kernel developers decided to use that fact to create a powerful security feature. In July 2012, Linux version 3.5 was released which added support for something called Seccomp-BPF. Seccomp-BPF is a Linux kernel feature that allows you to restrict the syscalls that a process can make by creating a special filter.

In theory, you can create a Seccomp-BPF filter that only allows a process to make the exact syscalls that it needs to function and nothing more. This would be useful in cases where an app is accidentally exploitable in a way that allows an adversary to spawn additional processes. If seccomp isn’t allowing the process to make new syscalls, there’s a good chance it could thwart the attacker.

Seccomp is super cool, and it’s even integrated into container runtime and orchestration tools like Docker and Kubernetes. It begs the question: “Why isn’t seccomp widely used?” I think the answer is that there aren’t enough resources out there that bridge the gap between a low-level kernel feature like seccomp and modern software development processes. Not every organization has a low-level code developer who knows a ton about syscalls. There’s also the overhead of figuring out which syscalls your program needs and updating that with every new feature you implement in your code.

### Bridging the Gap
This project utilizes a tool created by Red Hat called [oci-seccomp-bpf-hook](https://github.com/containers/oci-seccomp-bpf-hook). The tool helps simplify the creation of seccomp filters by recording syscalls made by a container during runtime and pumping them into a filter that you can use with seccomp. The OCI hook dramatically reduces the knowledge about syscalls that you’d need to create a seccomp filter, but there’s still quite a bit of overhead involved in updating your seccomp filter with the tool every time you update your code.

To solve that problem, this repository serves as an example to show you how to automate the creation of a seccomp filter for your app every time your code gets updated. This is accomplished by creating a [GitHub Actions workflow](https://github.com/lawndoc/seccomp-ci-demo/tree/main/.github/workflows/seccomp.yml) that utilizes Red Hat’s oci-seccomp-bpf-hook to generate and commit a seccomp filter for your application.

### Requirements
Red Hat's oci-seccomp-bpf-hook was made to work with their container runtime, [Podman](https://podman.io/). Because of that, you need to use a self-hosted Fedora runner to use the example workflow provided in this repository. To use GitHub's default Action runners (Ubuntu), you need to build podman and oci-seccomp-bpf-hook from source when setting up the dependencies in your workflow. If you want to pursue that, I recommend trying to use GitHub's [cache action](https://github.com/actions/cache) to reduce the time required to build the dependencies every time your workflow runs.

To modify the provided GitHub workflow for your application, you just need to make sure that your ‘podman build’ and ‘podman run’ steps reflect the way you build your container image and run your tests.

Lastly, you NEED to have a very high percentage of your code getting executed in your automated unit and functional tests. If your application has some functionality that isn’t being executed when you are generating the seccomp filter, there’s a chance that you could be missing some syscalls in your filter. This means they will get blocked when your code tries to run with the seccomp filter applied.

Luckily, there’s a tip-off that will indicate that your application isn’t working because of seccomp. If seccomp is preventing your app from making a needed syscall, the error that your application throws will always include a message about not having permission to do something. In that case, you just need to figure out which part of your code you missed in your automated testing. Then you add a test for the missed case, and your new seccomp filter will be generated as soon as you push the new test to your repo. There are tools out there that help you monitor your test coverage, and I recommend you use them if you are generating seccomp filters for your app.
