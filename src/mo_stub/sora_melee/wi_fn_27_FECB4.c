void* fn_27_FECB4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 25) + i;
    if (idx >= 37) idx -= 37;
    return (char*)p + idx * 12 + 12;
}
