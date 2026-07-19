void* fn_27_3958B4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 4) idx -= 4;
    return (char*)p + idx * 52 + 12;
}
