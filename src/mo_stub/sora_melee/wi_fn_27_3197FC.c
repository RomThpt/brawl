void* fn_27_3197FC(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 28) + i;
    if (idx >= 7) idx -= 7;
    return (char*)p + idx * 16 + 28;
}
