void* fn_27_C4504(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 26) + i;
    if (idx >= 20) idx -= 20;
    return (char*)p + idx * 4 + 12;
}
