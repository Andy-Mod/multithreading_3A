cmake_minimum_required(VERSION 3.14)
set(CMAKE_CXX_STANDARD 17)

set(PROJECT_NAME "low_level")
project(${PROJECT_NAME})

set(CMAKE_BUILD_TYPE Release)

option(CPR_ENABLE_SSL "" OFF)

include(FetchContent)

# Declare dependencies
FetchContent_Declare(
  json
  DOWNLOAD_EXTRACT_TIMESTAMP OFF
  URL "https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz")
FetchContent_Declare(
  cpr
  DOWNLOAD_EXTRACT_TIMESTAMP OFF
  URL "https://github.com/libcpr/cpr/archive/refs/tags/1.10.5.tar.gz")
FetchContent_Declare(
  eigen
  DOWNLOAD_EXTRACT_TIMESTAMP OFF
  URL "https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz")

FetchContent_MakeAvailable(json eigen cpr)

# Find OpenMP
find_package(OpenMP REQUIRED)

# Add executable
add_executable(${PROJECT_NAME} ${PROJECT_NAME}.cpp)

# Link libraries and OpenMP
target_link_libraries(${PROJECT_NAME} nlohmann_json::nlohmann_json cpr::cpr
                      Eigen3::Eigen OpenMP::OpenMP_CXX)

add_definitions(-DEIGEN_DONT_PARALLELIZE)
# Ensure OpenMP is enabled by adding the proper flags if OpenMP is found
if(OPENMP_FOUND)
  target_compile_options(${PROJECT_NAME} PRIVATE ${OpenMP_CXX_FLAGS})
  target_link_options(${PROJECT_NAME} PRIVATE ${OpenMP_EXE_LINKER_FLAGS})
endif()
