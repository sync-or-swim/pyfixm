About
=====
pyfixm is a library that contains Python wrappers for the FIXM_ XML Schemas,
plus the `US NAS extension`_ for the FAA. Currently the library is built for
FIXM v3.0, as this is what the FAA uses to publish data through SWIM_.

Usage
=====

.. code-block:: python3

    import pyfixm
    xml = pyfixm.parse("./fixm_file.xml")

Building pyfixm manually
========================
To build ``pyfixm`` either use the suppled ``build-pyfixm`` PyCharm run
configuration or by manually running ``scripts/build.py``. Both methods build
the library within a Docker image and then extract the built library to
``./pyfixm`` on the host computer. Reminder to install Docker if you haven't
already.

License
=======
This project has two licenses. Because really what this repository creates is a
transpilation of the FIXM XSD files, the generated library is treated as a
distribution of the upstream and not a novel codebase and assumes no further
copyright with the built library. Both components are licensed under the BSD
3-Clause, but the copyright holder is different.

Source Repo
-----------
The ``pyfixm`` library-generating source code is licensed under the BSD 3-Clause
license.

Generated Library
-----------------
The generated library (the part that gets published to PyPI) is licensed under
the same license as the upstream FIXM XSD files. Note that the copyright is
attributed to the FIXM copyright holders to avoid any copyright complexities.

.. _SWIM: https://www.faa.gov/air_traffic/technology/swim/overview/
.. _US NAS extension: https://www.fixm.aero/content/extensions.pl
.. _FIXM: https://www.fixm.aero/
