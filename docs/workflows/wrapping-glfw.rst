Wrapping GLFW
=============

This will be a walkthrough of using wrapdevtools to wrap glfw. And a
demonstration of what will hopefully be an ergonomic wrapping
workflow.

First things first, install the tools with ``pip3 install --user -e .`` from
the wrapdevtools repo.

Create The Wrap file
----------------------------

First make a new directory to work in:

::
   mkdir glfw-wrapping
   cd glfw-wrapping

Now find the upstream source tarball.  I know glfw is at
`<http://www.glfw.org>`_. And I've found that the link to the latest
version (3.2.1 as of writing) is
`<https://github.com/glfw/glfw/releases/download/3.2.1/glfw-3.2.1.zip>`_.

To start off I run:

::
   wrapdev-newwrap https://github.com/glfw/glfw/releases/download/3.2.1/glfw-3.2.1.zip glfw

This will create a subprojects directory (within the current working
directory), download the referenced file to the packagecache, extract it,
and then generate a subprojects/glfw.wrap for it. This wrap file will
become the contents of upstream.wrap on wrapdb


Writing the meson build files
---------------------------------------

Next I go through and read the native build files to find what goes
into the targets I want, usually it's a list of sources + some config
dependeny sources. In the case of glfw the list of sources is quite
small, so I'll just write them out myself. However for a larger
library I could use ``wrapdev-listsrc`` to help generate parts of my meson build file


When I'm done I get the following meson.build file

.. code-block:: meson

	project('glfw', 'c', version: '3.2.1')

	cc = meson.get_compiler('c')


	glfw_core_src = files(
	'src/context.c',
	'src/init.c',
	'src/input.c',
	'src/monitor.c',
	'src/vulkan.c',
	'src/window.c'
	)
	glfw_platform_src = []
	glfw_deps = []
	glfw_deps += cc.find_library('m', required: false)
	glfw_deps += cc.find_library('dl', required: false)
	glfw_deps += dependency('threads')
	if get_option('windowing_backend') == 'x11'
	x11_dep = dependency('x11')
	xrandr_dep = dependency('xrandr')
	xinerama_dep = dependency('xinerama')
	xkb_dep = dependency('xkbcommon')
	xcursor_dep = dependency('xcursor')
	glfw_deps += [x11_dep, xrandr_dep, xinerama_dep, xkb_dep, xcursor_dep]
	glfw_platform_src += files(
	    'src/x11_init.c',
	    'src/x11_monitor.c',
	    'src/x11_window.c',
	    'src/xkb_unicode.c',
	    'src/linux_joystick.c',
	    'src/posix_time.c',
	    'src/posix_tls.c',
	    'src/glx_context.c',
	    'src/egl_context.c'
	)

	else
	error('backend not supported')
	endif

	conf_data = configuration_data()
	if get_option('windowing_backend') == 'x11'
	conf_data.set('_GLFW_X11', 1)
	endif
	conf_file = configure_file(configuration: conf_data, output: 'glfw_config.h')


	glfw_lib = library('glfw', glfw_core_src + glfw_platform_src,
			include_directories: include_directories('src'),
			dependencies: glfw_deps,
			c_args: ['-D_GLFW_USE_CONFIG_H'])

	glfw_dep = declare_dependency(
	include_directories: include_directories('src'),
	link_with: glfw_lib)

and the following meson_options.txt file

.. code-block:: meson

	option('windowing_backend', type: 'combo',
	    choices: ['x11', 'wayland', 'win32', 'cocoa'],
	    description: 'windowing backend to use',
	    value: 'x11')


Testing the wrap
----------------------

To test the wrap I add a simple meson.build file to the root of my project tree (the one with subprojects in it), that looks like this:

.. code-block:: meson

		project('test')
		subproject('glfw')

I then test this file with meson.


Exporting the wrap
---------------------------

Next I use ``wrapdev-extractpatch`` to copy my build files over to a directory sutable for the wrapdb. This tool does the following:

1. Extracts the upstream tarball to a temporary directory.
2. Compares the extracted directory with the directory referenced by the wrap file
3. Copies any files that only exist in the second directory to the output directory
4. Copies the wrapfile to ``<output directory>/upstream.wrap``

for GLFW I would use
::
   wrapdev-extractpatch subprojects/glfw.wrap --output glfw-patch

I get a patch filetree in the glfw-patch directory
   
