void* fn_27_1AFEF4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 22) + i;
    if (idx >= 280) idx -= 280;
    return (char*)p + idx * 4 + 12;
}
