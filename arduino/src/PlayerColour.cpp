#include "PlayerColour.hpp"
uint32_t playerColourToNeopixelColour(PlayerColour colour) {
  switch (colour) {
  case RED:
    return 0xFF0000;
  case YELLOW:
    return 0xFFFF00;
  default:
    return 0x000000;
  }
}
