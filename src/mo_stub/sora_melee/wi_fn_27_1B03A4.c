void* fn_27_1B03A4(void* p, int i) {
    int idx = (*(int*)((char*)p + 8) >> 27) + i;
    if (idx >= 12) idx -= 12;
    return (char*)p + idx * 96 + 12;
}
