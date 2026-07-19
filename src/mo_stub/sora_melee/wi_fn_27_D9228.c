void* fn_27_D9228(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 61) idx -= 61;
    return (char*)p + idx * 48 + 12;
}
