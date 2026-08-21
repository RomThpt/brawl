#include <gr/gr_tengan_event.h>

bool grTenganEvent::isEvent() const {
    return m_state != NoEvent;
}

bool grTenganEvent::isReadyEnd() const {
    return m_state == ReadyEnd;
}

s32 grTenganEvent::getPhase() const {
    return m_phase;
}

void grTenganEvent::setPhase(s32 phase) {
    m_phase = phase;
}
