void* fn_27_1CF200(void* p, int i) {
    int idx = (*(int*)((char*)p + 24) >> 26) + i;
    if (idx >= 16) idx -= 16;
    return (char*)p + idx * 12 + 28;
}
