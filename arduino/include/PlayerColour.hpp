#pragma once
#include <cstdint>

/// @brief The colour of a player.
enum PlayerColour { RED, YELLOW, EMPTY };

/// @brief Convert a PlayerColour to a neopixel colour.
/// @param colour The PlayerColour to convert.
/// @return The neopixel colour.
uint32_t playerColourToNeopixelColour(PlayerColour colour);
