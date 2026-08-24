#include <mu/menu.h>

struct MuStageKindEntry {
    u8 _0;
    u8 _1;
    u8 _2;
    u8 _3;
};

extern const MuStageKindEntry g_muStageKindTable[];
extern const u8 g_muStageInfoMsgIdTable[];

int muMenu::exchangeMuStageKindToGmHideStageKind(int id, int, int) {
    return g_muStageKindTable[id]._1;
}

int muMenu::getInfoMsgID(int id, int, int) {
    return g_muStageInfoMsgIdTable[id];
}
