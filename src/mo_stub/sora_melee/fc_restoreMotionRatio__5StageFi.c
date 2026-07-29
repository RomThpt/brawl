void restoreMotionRatio__5StageFi(void* dst, void* src) {
    *(float*)((char*)dst + 200) = *(float*)((char*)src + 0);
    *(float*)((char*)dst + 204) = *(float*)((char*)src + 4);
    *(float*)((char*)dst + 208) = *(float*)((char*)src + 8);
    *(float*)((char*)dst + 212) = *(float*)((char*)src + 12);
}
