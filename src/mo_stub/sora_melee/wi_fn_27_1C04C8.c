void* fn_27_1C04C8(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 27) + i;
    if (idx >= 11) idx -= 11;
    return (char*)p + idx * 12 + 28;
}
