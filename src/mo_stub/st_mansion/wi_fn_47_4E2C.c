void* fn_47_4E2C(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 30) + i;
    if (idx >= 1) idx -= 1;
    return (char*)p + idx * 120 + 12;
}
