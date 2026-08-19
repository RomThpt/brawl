#include <mu/mu_msg.h>

void MuMsg::setHSpace(u32 msgIndex, float value) {
    m_windowSettings[msgIndex].m_hSpace = value;
}

void MuMsg::setWScale(u32 msgIndex, float value) {
    m_windowSettings[msgIndex].m_wScale = value;
}

void MuMsg::getWScale(u32 msgIndex, float value) {
    m_windowSettings[msgIndex].m_wScale2 = value;
}

void MuMsg::setHScale(u32 msgIndex, float value) {
    m_windowSettings[msgIndex].m_hScale = value;
}

void MuMsg::getHScale(u32 msgIndex, float value) {
    m_windowSettings[msgIndex].m_hScale2 = value;
}
