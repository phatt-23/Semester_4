# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.30

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/phatt/School/sem4/URO/qt/Form/Form

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/phatt/School/sem4/URO/qt/Form/Form/cmake

# Include any dependencies generated for this target.
include CMakeFiles/Form.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/Form.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/Form.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/Form.dir/flags.make

Form_autogen/timestamp: /usr/lib64/qt6/libexec/moc
Form_autogen/timestamp: /usr/lib64/qt6/libexec/uic
Form_autogen/timestamp: CMakeFiles/Form.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --blue --bold --progress-dir=/home/phatt/School/sem4/URO/qt/Form/Form/cmake/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Automatic MOC and UIC for target Form"
	/usr/bin/cmake -E cmake_autogen /home/phatt/School/sem4/URO/qt/Form/Form/cmake/CMakeFiles/Form_autogen.dir/AutogenInfo.json ""
	/usr/bin/cmake -E touch /home/phatt/School/sem4/URO/qt/Form/Form/cmake/Form_autogen/timestamp

CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o: CMakeFiles/Form.dir/flags.make
CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o: Form_autogen/mocs_compilation.cpp
CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o: CMakeFiles/Form.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/phatt/School/sem4/URO/qt/Form/Form/cmake/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o -MF CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o.d -o CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o -c /home/phatt/School/sem4/URO/qt/Form/Form/cmake/Form_autogen/mocs_compilation.cpp

CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/phatt/School/sem4/URO/qt/Form/Form/cmake/Form_autogen/mocs_compilation.cpp > CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.i

CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/phatt/School/sem4/URO/qt/Form/Form/cmake/Form_autogen/mocs_compilation.cpp -o CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.s

CMakeFiles/Form.dir/main.cpp.o: CMakeFiles/Form.dir/flags.make
CMakeFiles/Form.dir/main.cpp.o: /home/phatt/School/sem4/URO/qt/Form/Form/main.cpp
CMakeFiles/Form.dir/main.cpp.o: CMakeFiles/Form.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/phatt/School/sem4/URO/qt/Form/Form/cmake/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object CMakeFiles/Form.dir/main.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/Form.dir/main.cpp.o -MF CMakeFiles/Form.dir/main.cpp.o.d -o CMakeFiles/Form.dir/main.cpp.o -c /home/phatt/School/sem4/URO/qt/Form/Form/main.cpp

CMakeFiles/Form.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/Form.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/phatt/School/sem4/URO/qt/Form/Form/main.cpp > CMakeFiles/Form.dir/main.cpp.i

CMakeFiles/Form.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/Form.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/phatt/School/sem4/URO/qt/Form/Form/main.cpp -o CMakeFiles/Form.dir/main.cpp.s

CMakeFiles/Form.dir/mainwindow.cpp.o: CMakeFiles/Form.dir/flags.make
CMakeFiles/Form.dir/mainwindow.cpp.o: /home/phatt/School/sem4/URO/qt/Form/Form/mainwindow.cpp
CMakeFiles/Form.dir/mainwindow.cpp.o: CMakeFiles/Form.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/phatt/School/sem4/URO/qt/Form/Form/cmake/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object CMakeFiles/Form.dir/mainwindow.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/Form.dir/mainwindow.cpp.o -MF CMakeFiles/Form.dir/mainwindow.cpp.o.d -o CMakeFiles/Form.dir/mainwindow.cpp.o -c /home/phatt/School/sem4/URO/qt/Form/Form/mainwindow.cpp

CMakeFiles/Form.dir/mainwindow.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/Form.dir/mainwindow.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/phatt/School/sem4/URO/qt/Form/Form/mainwindow.cpp > CMakeFiles/Form.dir/mainwindow.cpp.i

CMakeFiles/Form.dir/mainwindow.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/Form.dir/mainwindow.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/phatt/School/sem4/URO/qt/Form/Form/mainwindow.cpp -o CMakeFiles/Form.dir/mainwindow.cpp.s

# Object files for target Form
Form_OBJECTS = \
"CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o" \
"CMakeFiles/Form.dir/main.cpp.o" \
"CMakeFiles/Form.dir/mainwindow.cpp.o"

# External object files for target Form
Form_EXTERNAL_OBJECTS =

Form: CMakeFiles/Form.dir/Form_autogen/mocs_compilation.cpp.o
Form: CMakeFiles/Form.dir/main.cpp.o
Form: CMakeFiles/Form.dir/mainwindow.cpp.o
Form: CMakeFiles/Form.dir/build.make
Form: /usr/lib64/libQt6Widgets.so.6.8.2
Form: /usr/lib64/libQt6Gui.so.6.8.2
Form: /usr/lib64/libGLX.so
Form: /usr/lib64/libOpenGL.so
Form: /usr/lib64/libQt6Core.so.6.8.2
Form: CMakeFiles/Form.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/phatt/School/sem4/URO/qt/Form/Form/cmake/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking CXX executable Form"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/Form.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/Form.dir/build: Form
.PHONY : CMakeFiles/Form.dir/build

CMakeFiles/Form.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/Form.dir/cmake_clean.cmake
.PHONY : CMakeFiles/Form.dir/clean

CMakeFiles/Form.dir/depend: Form_autogen/timestamp
	cd /home/phatt/School/sem4/URO/qt/Form/Form/cmake && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/phatt/School/sem4/URO/qt/Form/Form /home/phatt/School/sem4/URO/qt/Form/Form /home/phatt/School/sem4/URO/qt/Form/Form/cmake /home/phatt/School/sem4/URO/qt/Form/Form/cmake /home/phatt/School/sem4/URO/qt/Form/Form/cmake/CMakeFiles/Form.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/Form.dir/depend

