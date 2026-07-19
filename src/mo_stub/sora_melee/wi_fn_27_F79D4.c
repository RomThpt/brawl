void* fn_27_F79D4(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 25) + i;
    if (idx >= 37) idx -= 37;
    return (char*)p + idx * 12 + 28;
}
