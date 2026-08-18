#include <cm/cm_controller_photo.h>

void cmPhotoController::addCallBack(utListNode* cb) {
    m_callbacks.addTail(cb);
}

void cmPhotoController::removeCallBack(utListNode* cb) {
    if (cb != NULL) {
        m_callbacks.removeExist(cb);
    }
}
