cmake_minimum_required(VERSION 3.12)
project(cipher_patcher)

set(CMAKE_CXX_STANDARD 14)

SET(CMAKE_CXX_FLAGS "-O0")
SET(CMAKE_C_FLAGS "-O0")

add_executable(cipher_patcher main.cpp)