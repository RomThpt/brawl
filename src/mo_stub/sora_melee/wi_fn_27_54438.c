void* fn_27_54438(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 23) + i;
    if (idx >= 255) idx -= 255;
    return (char*)p + idx * 8 + 12;
}
