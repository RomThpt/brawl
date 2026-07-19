void* fn_27_D9638(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 14) idx -= 14;
    return (char*)p + idx * 48 + 12;
}
