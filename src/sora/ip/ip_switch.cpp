#include <ip/ip_switch.h>
#include <sr/sr_common.h>
#include <types.h>

ipSwitch* ipSwitch::getInstance() {
    if (!g_ipSwitch) {
        g_ipSwitch = new (Heaps::SystemFW) ipSwitch;
    }
    return g_ipSwitch;
}
