#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os

class GlmConan(ConanFile):
    name = "glm"
    version = "0.9.8.5"
    description = "OpenGL Mathematics (GLM)"
    url = "https://github.com/bincrafters/conan-glm"
    homepage = "https://github.com/g-truc/glm"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["FindGLM.cmake", "LICENSE.md"]
    source_subfolder = "source_subfolder"
    no_copy_source = True

    def source(self):
        source_url = "https://github.com/g-truc/glm"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = "glm-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        self.patch_gcc()

    def patch_gcc(self):
        header_file = os.path.join(self.source_subfolder, "glm", "simd", "platform.h")
        tools.replace_in_file(header_file, """#	elif (__GNUC__ == 7) && (__GNUC_MINOR__ == 2)
#		define GLM_COMPILER (GLM_COMPILER_GCC72)""",\
                                           """
#	elif (__GNUC__ == 7) && (__GNUC_MINOR__ == 2)
#		define GLM_COMPILER (GLM_COMPILER_GCC72)
#	elif (__GNUC__ == 7) && (__GNUC_MINOR__ == 3)
#		define GLM_COMPILER (GLM_COMPILER_GCC72)
                                           """)

    def package(self):
        self.copy("FindGLM.cmake")
        self.copy("*", src=os.path.join(self.source_subfolder, "glm"), dst=os.path.join("include", "glm"))
        self.copy("copying.txt", dst="licenses", src=self.source_subfolder)

    def package_id(self):
        self.info.header_only()
