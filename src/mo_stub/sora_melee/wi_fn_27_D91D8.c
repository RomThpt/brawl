void* fn_27_D91D8(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 24) + i;
    if (idx >= 65) idx -= 65;
    return (char*)p + idx * 48 + 12;
}
