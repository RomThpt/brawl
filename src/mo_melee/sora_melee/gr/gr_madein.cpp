#include <gr/gr_madein.h>

grMadein::~grMadein() {
    if (m_stageHitData) {
        delete m_stageHitData;
    }
    if (m_overwriteAttackData) {
        if (m_overwriteAttackData) {
            delete m_overwriteAttackData;
        }
    }
    if (m_attackInfo) {
        delete m_attackInfo;
    }
    if (m_hitPointInfo) {
        delete m_hitPointInfo;
    }
}
