#include <cm/cm_controller_anm.h>

void cmAnimationController::releaseScnAnmRes() {
    if (unk10) {
        unk10->Destroy();
    }
    if (unkC) {
        unkC->Destroy();
    }
    unkC = nullptr;
    unk10 = nullptr;
}
