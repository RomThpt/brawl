#include <ms/ms_char_writer.h>

namespace ms {

void CharWriter::SetCursor(float x, float y) {
    m_xPos = x;
    m_yPos = y;
}

void CharWriter::SetCursor(float x, float y, float z) {
    m_xPos = x;
    m_yPos = y;
    m_zPos = z;
}

void CharWriter::SetCursorX(float x) {
    m_xPos = x;
}

void CharWriter::SetCursorY(float y) {
    m_yPos = y;
}

void CharWriter::SetCursorZ(float z) {
    m_zPos = z;
}

void CharWriter::MoveCursorX(float x) {
    m_xPos += x;
}

void CharWriter::MoveCursorY(float y) {
    m_yPos += y;
}

float CharWriter::GetCursorX() const {
    return m_xPos;
}

float CharWriter::GetCursorY() const {
    return m_yPos;
}

float CharWriter::GetCursorZ() const {
    return m_zPos;
}

} // namespace ms
