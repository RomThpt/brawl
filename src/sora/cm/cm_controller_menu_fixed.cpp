#include <StaticAssert.h>
#include <gf/gf_camera.h>
#include <gf/gf_camera_controller.h>
#include <types.h>

class cmMenuFixedController : public gfCameraController {
    bool unk8 : 1;
    float unkC;
    Vec3f unk10;
    float unk1C;
public:
    cmMenuFixedController();
    void storeDefault();
    void init();
    virtual void update(float);
};
static_assert(sizeof(cmMenuFixedController) == 0x20, "Class is wrong size!");

cmMenuFixedController::cmMenuFixedController() : gfCameraController() {
    unkC = 68.0f;
    unk1C = 0.69813f;
    unk8 = false;
    unk10.m_x = 0.0f;
    unk10.m_y = 0.0f;
    unk10.m_z = 0.0f;
}

void cmMenuFixedController::storeDefault() {
    unkC = m_cameraManager->m_cameras[0].unkCC;
    unk10.m_x = m_cameraManager->m_cameras[0].m_targetPos.m_x;
    unk10.m_y = m_cameraManager->m_cameras[0].m_targetPos.m_y;
    unk10.m_z = m_cameraManager->m_cameras[0].m_targetPos.m_z;
    unk1C = m_cameraManager->m_cameras[0].unkD0;
    unk8 = true;
}

void cmMenuFixedController::init() {
    gfCamera& cam = m_cameraManager->m_cameras[0];
    Vec2f rot;
    cam.unkCC = unkC;
    cam.unkFA.m_mask |= 0x80;
    cam.m_targetPos.m_x = unk10.m_x;
    cam.m_targetPos.m_y = unk10.m_y;
    cam.m_targetPos.m_z = unk10.m_z;
    cam.unkFA.m_mask |= 0x2;
    cam.unkD0 = unk1C;
    rot.m_x = 0.0f;
    rot.m_y = 0.0f;
    cam.m_rot.m_x = rot.m_x;
    cam.m_rot.m_y = rot.m_y;
    cam.m_rot.m_z = 0.0f;
    cam.unkFA.m_mask |= 0x40;
}

// TODO: cmMenuFixedController::update
