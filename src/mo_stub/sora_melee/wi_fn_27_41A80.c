void* fn_27_41A80(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 28) + i;
    if (idx >= 6) idx -= 6;
    return (char*)p + idx * 8 + 12;
}
