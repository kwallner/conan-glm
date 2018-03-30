#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os

class GlmConan(ConanFile):
    name = "glm"
    version = "0.9.8.5"
    description="OpenGL Mathematics (GLM)"
    url="https://github.com/bincrafters/conan-glm"
    homepage="https://github.com/g-truc/glm"
    license = "MIT"
    exports = "lib_licenses/*"
    exports_sources = ["FindGLM.cmake"]
    generators = "txt"
    source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://github.com/g-truc/glm"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url,
                                                          self.version))
        extracted_dir = "glm-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        # Hack that fixes bug that crashes gcc 7.3 - check if still necessary
        # after glm 0.9.8.5
        tools.replace_in_file(os.path.join(self.source_subfolder, "glm", "simd",\
                                           "platform.h"),\
                                           """#	elif (__GNUC__ == 7) && (__GNUC_MINOR__ == 2)
#		define GLM_COMPILER (GLM_COMPILER_GCC72)""",\
                                           """
#	elif (__GNUC__ == 7) && (__GNUC_MINOR__ == 2)
#		define GLM_COMPILER (GLM_COMPILER_GCC72)
#	elif (__GNUC__ == 7) && (__GNUC_MINOR__ == 3)
#		define GLM_COMPILER (GLM_COMPILER_GCC72)
                                           """)
        self.output.info("No compilation necessary for GLM")

    def package(self):
        self.copy("FindGLM.cmake", ".", ".")
        self.copy("*",src=os.path.join(self.source_subfolder, "glm"),\
                  dst=os.sep.join([".", "include", "glm"]))
        self.copy(os.path.join("lib_licenses", "license*"), dst="licenses",
                  ignore_case=True, keep_path=False)
