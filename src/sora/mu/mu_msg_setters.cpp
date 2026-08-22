#include <mu/mu_msg.h>

void MuMsg::setWindowRectVisible(u32 msgIndex, bool isVisible) {
    m_windowSettings[msgIndex].m_isVisible = isVisible;
}

void MuMsg::setFontColor(u32 msgIndex, u8 r, u8 g, u8 b, u8 a) {
    WindowSetting& ws = m_windowSettings[msgIndex];
    ws.m_colorR = r;
    ws.m_colorG = g;
    ws.m_colorB = b;
    ws.m_colorA = a;
}

void MuMsg::setAlignMode(u32 msgIndex, AlignMode alignMode) {
    m_windowSettings[msgIndex].m_alignMode = alignMode;
}
