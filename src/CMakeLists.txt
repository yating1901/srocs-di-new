#
# Set minimum required version
#
cmake_minimum_required(VERSION 3.1)

project(argos3-di CXX)

#set argos3-srocs path
set(ARGOS_SROCS_PATH /home/yating/Workspace/argos3-srocs-hurry)

#
# Set the path additional cmake files must be searched for
#
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_SOURCE_DIR}/cmake)

#
# Set build options, set flags, check libraries
#
include(${CMAKE_SOURCE_DIR}/cmake/ARGoSBuildOptions.cmake)
include(${CMAKE_SOURCE_DIR}/cmake/ARGoSBuildFlags.cmake)
include(${CMAKE_SOURCE_DIR}/cmake/ARGoSBuildChecks.cmake)

# Set up ARGoS compilation information
include_directories(BEFORE ${CMAKE_SOURCE_DIR})

#
# Compile loop function
#
add_subdirectory(loop_functions)

#
# Configure examples
#

configure_file(
  ${CMAKE_SOURCE_DIR}/experiment/example_builderbot_advance.argos.in
  ${CMAKE_BINARY_DIR}/experiment/example_builderbot_advance.argos
  )

configure_file(
  ${CMAKE_SOURCE_DIR}/experiment/example_builderbot_advance.lua.in
  ${CMAKE_BINARY_DIR}/experiment/example_builderbot_advance.lua
  )

configure_file(
  ${CMAKE_SOURCE_DIR}/experiment/srocs.argos.in
  ${CMAKE_BINARY_DIR}/experiment/srocs.argos
  )

configure_file(
  ${CMAKE_SOURCE_DIR}/experiment/template.argos.in
  ${CMAKE_BINARY_DIR}/experiment/template.argos
  )


configure_file(
  ${CMAKE_SOURCE_DIR}/experiment/example_block.lua
  ${CMAKE_BINARY_DIR}/experiment/example_block.lua
  COPYONLY)

configure_file(
  ${CMAKE_SOURCE_DIR}/experiment/test_sample_rules.lua
  ${CMAKE_BINARY_DIR}/experiment/test_sample_rules.lua
  COPYONLY)

configure_file(
  ${CMAKE_SOURCE_DIR}/experiment/block_usercode.lua
  ${CMAKE_BINARY_DIR}/experiment/block_usercode.lua
  COPYONLY)

