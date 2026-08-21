#include <ms/ms_char_writer.h>

namespace ms {

void CharWriter::EnableFixedWidth(bool enabled) {
    m_isFixedWidth = enabled;
}

float CharWriter::GetFixedWidth() const {
    return m_fixedWidth;
}

void CharWriter::SetFixedWidth(float fixedWidth) {
    m_fixedWidth = fixedWidth;
}

} // namespace ms
