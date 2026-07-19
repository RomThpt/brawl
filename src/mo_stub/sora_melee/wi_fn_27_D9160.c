void* fn_27_D9160(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 24) + i;
    if (idx >= 92) idx -= 92;
    return (char*)p + idx * 48 + 12;
}
