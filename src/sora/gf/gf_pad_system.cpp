#include <gf/gf_pad_queue.h>
#include <gf/gf_pad_system.h>

void gfPadSystem::clearPadQueue() {
    if (m_padQueue) {
        m_padQueue->clear();
    }
}
