#include <ip/ip_padconfig.h>
#include <sr/sr_common.h>
#include <types.h>

ipPadConfig* ipPadConfig::getInstance() {
    if (!s_instance) {
        s_instance = new (Heaps::SystemFW) ipPadConfig;
    }
    return s_instance;
}
