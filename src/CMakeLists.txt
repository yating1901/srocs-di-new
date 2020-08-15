#
# Set minimum required version
#
cmake_minimum_required(VERSION 3.1)

project(argos3-di CXX)

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
# Compile loop functions
#
add_library(di_srocs_loop_functions MODULE
   loop_functions/di_srocs_loop_functions.h
   loop_functions/di_srocs_loop_functions.cpp)
target_link_libraries(di_srocs_loop_functions
   ${SROCS_ENTITIES_LIBRARY})

#
# Compile qtopengl user functions
#
if(ARGOS_COMPILE_QTOPENGL)
   add_library(builderbot_qtopengl_user_functions MODULE
      qtopengl_user_functions/builderbot_qtopengl_user_functions.h
      qtopengl_user_functions/builderbot_qtopengl_user_functions_widget.h
      qtopengl_user_functions/builderbot_qtopengl_user_functions.cpp
      qtopengl_user_functions/builderbot_qtopengl_user_functions_widget.cpp)
   target_link_libraries(builderbot_qtopengl_user_functions
      ${ARGOS_QTOPENGL_LIBRARY}
      ${SROCS_ENTITIES_LIBRARY}
      ${SROCS_BUILDERBOT_LIBRARY})
endif(ARGOS_COMPILE_QTOPENGL)

#
# Configure examples
#
configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_template.argos.in
               ${CMAKE_BINARY_DIR}/experiment/dcp_template.argos)

configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_generate_data.py
               ${CMAKE_BINARY_DIR}/experiment/dcp_generate_data.py)
               
configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_process_data.py
               ${CMAKE_BINARY_DIR}/experiment/dcp_process_data.py)

configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_builderbot.lua.in
               ${CMAKE_BINARY_DIR}/experiment/dcp_builderbot.lua)

configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_builderbot_rules.lua
               ${CMAKE_BINARY_DIR}/experiment/dcp_builderbot_rules.lua
               COPYONLY)

configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_search_block.lua
               ${CMAKE_BINARY_DIR}/experiment/dcp_search_block.lua
               COPYONLY)

configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_block.lua
               ${CMAKE_BINARY_DIR}/experiment/dcp_block.lua
               COPYONLY)

configure_file(${CMAKE_SOURCE_DIR}/experiment/dcp_block_usercode.lua
               ${CMAKE_BINARY_DIR}/experiment/dcp_block_usercode.lua
               COPYONLY)

