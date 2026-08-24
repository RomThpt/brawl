#include <em/em_weapon_manager.h>

emWeaponManager* emWeaponManager::getInstance() {
    return s_instance;
}
