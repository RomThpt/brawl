#include <cm/cm_camera_controller.h>

CameraController* CameraController::getInstance() {
    return s_instance;
}
