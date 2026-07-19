void* fn_27_D91B0(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 24) + i;
    if (idx >= 76) idx -= 76;
    return (char*)p + idx * 48 + 12;
}
