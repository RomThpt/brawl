#include <gf/gf_error_manager.h>
#include <sr/sr_common.h>
#include <types.h>

gfErrorManager* gfErrorManager::getInstance() {
    if (!s_instance) {
        s_instance = new (Heaps::SystemFW) gfErrorManager;
    }
    return s_instance;
}
