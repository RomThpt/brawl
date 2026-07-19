void* fn_27_122C54(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 16) idx -= 16;
    return (char*)p + idx * 8 + 12;
}
