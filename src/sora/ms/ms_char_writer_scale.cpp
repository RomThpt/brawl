#include <ms/ms_char_writer.h>

namespace ms {

void CharWriter::SetScale(float x, float y) {
    m_fontScaleX = x;
    m_fontScaleY = y;
}

void CharWriter::SetScale(float scale) {
    m_fontScaleX = scale;
    m_fontScaleY = scale;
}

float CharWriter::GetScaleH() const {
    return m_fontScaleX;
}

float CharWriter::GetScaleV() const {
    return m_fontScaleY;
}

float CharWriter::getAdjustFontScale() const {
    return m_104;
}

} // namespace ms
