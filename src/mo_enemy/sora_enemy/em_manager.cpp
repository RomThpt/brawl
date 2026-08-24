#include <em/em_manager.h>

emManager* emManager::getInstance() {
    return s_instance;
}
